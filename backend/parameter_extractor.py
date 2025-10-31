import re
from typing import List, Dict, Any, Optional, Tuple
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class ParameterExtractor:
    """Extract engineering parameters from PDF text"""
    
    def __init__(self, pdf_text: str, pdf_pages: List[Dict[str, Any]]):
        self.pdf_text = pdf_text
        self.pdf_pages = pdf_pages
        self.fuzzy_threshold = 80
    
    def extract_parameter(self, param_name: str) -> Dict[str, Any]:
        """Extract a single parameter from PDF"""
        
        # Try exact match first
        result = self._exact_match(param_name)
        if result:
            return result
        
        # Try fuzzy match
        result = self._fuzzy_match(param_name)
        if result:
            return result
        
        # Try pattern-based extraction
        result = self._pattern_match(param_name)
        if result:
            return result
        
        # Not found
        return {
            "name": param_name,
            "value": "NF",
            "unit": "",
            "source_page": None,
            "extraction_method": "not_found",
            "confidence": 0,
            "manually_edited": False,
            "source_text": "",
            "notes": "Not found in datasheet",
            "highlights": []
        }
    
    def _exact_match(self, param_name: str) -> Optional[Dict[str, Any]]:
        """Try exact parameter name match"""
        for page in self.pdf_pages:
            page_text = page["text"]
            
            # Search for parameter name (case-insensitive)
            pattern = re.escape(param_name)
            matches = list(re.finditer(pattern, page_text, re.IGNORECASE))
            
            if matches:
                # Try to extract value after the parameter name
                for match in matches:
                    value_info = self._extract_value_after_match(
                        page_text, match.end()
                    )
                    if value_info:
                        highlights = self._find_highlights(
                            page["blocks"], 
                            param_name, 
                            value_info["value"]
                        )
                        
                        return {
                            "name": param_name,
                            "value": value_info["value"],
                            "unit": value_info["unit"],
                            "source_page": page["page_number"],
                            "extraction_method": "exact_match",
                            "confidence": 95,
                            "manually_edited": False,
                            "source_text": value_info["context"],
                            "notes": "",
                            "highlights": highlights
                        }
        
        return None
    
    def _fuzzy_match(self, param_name: str) -> Optional[Dict[str, Any]]:
        """Try fuzzy matching for parameter name"""
        best_match = None
        best_score = 0
        
        for page in self.pdf_pages:
            page_text = page["text"]
            lines = page_text.split('\n')
            
            for line in lines:
                # Split line into potential parameter names
                parts = re.split(r'[:=\t]', line)
                if not parts:
                    continue
                
                potential_param = parts[0].strip()
                if not potential_param:
                    continue
                
                # Calculate fuzzy match score
                score = fuzz.ratio(param_name.lower(), potential_param.lower())
                
                if score >= self.fuzzy_threshold and score > best_score:
                    # Try to extract value
                    value_info = self._extract_value_from_line(line)
                    if value_info:
                        best_score = score
                        highlights = self._find_highlights(
                            page["blocks"], 
                            potential_param, 
                            value_info["value"]
                        )
                        
                        best_match = {
                            "name": param_name,
                            "value": value_info["value"],
                            "unit": value_info["unit"],
                            "source_page": page["page_number"],
                            "extraction_method": "fuzzy_match",
                            "confidence": min(score, 90),
                            "manually_edited": False,
                            "source_text": line.strip(),
                            "notes": f"Matched with: {potential_param}",
                            "highlights": highlights
                        }
        
        return best_match
    
    def _pattern_match(self, param_name: str) -> Optional[Dict[str, Any]]:
        """Try pattern-based extraction for common parameter types"""
        
        # Extract key words from parameter name
        keywords = self._extract_keywords(param_name)
        
        for page in self.pdf_pages:
            page_text = page["text"]
            lines = page_text.split('\n')
            
            for line in lines:
                # Check if line contains any keywords
                line_lower = line.lower()
                if any(kw.lower() in line_lower for kw in keywords):
                    value_info = self._extract_value_from_line(line)
                    if value_info:
                        highlights = self._find_highlights(
                            page["blocks"], 
                            keywords[0] if keywords else param_name, 
                            value_info["value"]
                        )
                        
                        return {
                            "name": param_name,
                            "value": value_info["value"],
                            "unit": value_info["unit"],
                            "source_page": page["page_number"],
                            "extraction_method": "pattern_match",
                            "confidence": 75,
                            "manually_edited": False,
                            "source_text": line.strip(),
                            "notes": "Extracted using pattern matching",
                            "highlights": highlights
                        }
        
        return None
    
    def _extract_value_after_match(self, text: str, start_pos: int) -> Optional[Dict[str, Any]]:
        """Extract value after a parameter name match"""
        # Get text after the match
        remaining_text = text[start_pos:start_pos + 200]
        
        # Look for value patterns
        # Pattern: optional separator + number + optional unit
        pattern = r'[:=\s]*([+-]?\d+\.?\d*\s*(?:to|-|–)\s*[+-]?\d+\.?\d*|[+-]?\d+\.?\d*)\s*([A-Za-z°%/]+)?'
        match = re.search(pattern, remaining_text)
        
        if match:
            value = match.group(1).strip()
            unit = match.group(2).strip() if match.group(2) else ""
            
            # Get context (surrounding text)
            context_start = max(0, start_pos - 50)
            context_end = min(len(text), start_pos + match.end() + 50)
            context = text[context_start:context_end].strip()
            
            return {
                "value": value,
                "unit": unit,
                "context": context
            }
        
        return None
    
    def _extract_value_from_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Extract value from a line of text"""
        # Pattern for value extraction
        patterns = [
            r'[:=]\s*([+-]?\d+\.?\d*\s*(?:to|-|–)\s*[+-]?\d+\.?\d*|[+-]?\d+\.?\d*)\s*([A-Za-z°%/]+)?',
            r'\s+([+-]?\d+\.?\d*\s*(?:to|-|–)\s*[+-]?\d+\.?\d*|[+-]?\d+\.?\d*)\s*([A-Za-z°%/]+)?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                value = match.group(1).strip()
                unit = match.group(2).strip() if match.group(2) else ""
                return {
                    "value": value,
                    "unit": unit,
                    "context": line.strip()
                }
        
        return None
    
    def _extract_keywords(self, param_name: str) -> List[str]:
        """Extract keywords from parameter name"""
        # Remove common words and split
        common_words = {'the', 'a', 'an', 'of', 'in', 'to', 'for'}
        words = re.findall(r'\w+', param_name)
        keywords = [w for w in words if w.lower() not in common_words]
        return keywords
    
    def _find_highlights(self, blocks: List[Dict], param_text: str, value_text: str) -> List[Dict[str, Any]]:
        """Find text positions for highlighting in PDF"""
        highlights = []
        
        # Search for parameter name
        for block in blocks:
            block_text = block.get("text", "")
            if param_text.lower() in block_text.lower():
                highlights.append({
                    "text": block_text,
                    "bbox": block.get("bbox", []),
                    "type": "parameter"
                })
        
        # Search for value
        for block in blocks:
            block_text = block.get("text", "")
            if value_text in block_text:
                highlights.append({
                    "text": block_text,
                    "bbox": block.get("bbox", []),
                    "type": "value"
                })
        
        return highlights

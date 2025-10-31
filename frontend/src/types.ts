export interface Parameter {
  id: string;
  name: string;
  value: string;
  unit: string;
  source_page: number | null;
  extraction_method: string;
  confidence: number;
  manually_edited: boolean;
  source_text: string;
  notes: string;
  highlights: Highlight[];
}

export interface Highlight {
  text: string;
  bbox: number[];
  type: 'parameter' | 'value';
}

export interface ExtractionMetadata {
  total_parameters: number;
  extracted_count: number;
  not_found_count: number;
}

export interface ExportData {
  metadata: {
    extraction_date: string;
    source_pdf: string;
    input_file: string;
    total_parameters: number;
    extracted_count: number;
    not_found_count: number;
    manually_edited_count: number;
  };
  parameters: Parameter[];
}

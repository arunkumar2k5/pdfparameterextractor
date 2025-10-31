import React, { useEffect, useState, useRef } from 'react';
import { Parameter } from '../types';
import { FileText } from 'lucide-react';

interface MarkdownViewerProps {
  markdownContent: string;
  selectedParameter: Parameter | null;
}

const MarkdownViewer: React.FC<MarkdownViewerProps> = ({ 
  markdownContent, 
  selectedParameter 
}) => {
  const [displayContent, setDisplayContent] = useState('');
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!markdownContent) {
      setDisplayContent('');
      return;
    }

    const lines = markdownContent.split('\n');
    let highlighted = lines.map((line, idx) => {
      const lineNum = idx;
      const isHighlighted = selectedParameter?.markdown_line === lineNum;
      
      if (isHighlighted) {
        return `<div class="bg-yellow-200 border-l-4 border-yellow-500 pl-2 py-1">${escapeHtml(line)}</div>`;
      }
      return `<div class="py-0.5">${escapeHtml(line)}</div>`;
    }).join('');

    setDisplayContent(highlighted);

    // Scroll to highlighted line
    if (selectedParameter?.markdown_line !== null && selectedParameter?.markdown_line !== undefined) {
      setTimeout(() => {
        const highlightedElement = contentRef.current?.querySelector('.bg-yellow-200');
        if (highlightedElement) {
          highlightedElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 100);
    }
  }, [markdownContent, selectedParameter]);

  const escapeHtml = (text: string) => {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  };

  if (!markdownContent) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <FileText className="mx-auto mb-4 text-gray-400" size={64} />
          <p className="text-gray-600 text-lg">No markdown available</p>
          <p className="text-gray-500 text-sm mt-2">Upload a PDF to see the markdown view</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Header */}
      <div className="bg-gray-100 border-b border-gray-200 px-4 py-2 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <FileText size={18} className="text-gray-600" />
          <span className="text-sm font-medium text-gray-700">Markdown View</span>
        </div>
        {selectedParameter && selectedParameter.markdown_line !== null && (
          <span className="text-xs text-blue-600">
            Line {selectedParameter.markdown_line}
          </span>
        )}
      </div>

      {/* Content */}
      <div 
        ref={contentRef}
        className="flex-1 overflow-auto p-4 bg-gray-50"
      >
        <div 
          className="font-mono text-xs leading-relaxed whitespace-pre-wrap"
          dangerouslySetInnerHTML={{ __html: displayContent }}
        />
      </div>

      {/* Footer info */}
      {selectedParameter && selectedParameter.markdown_context && (
        <div className="bg-blue-50 border-t border-blue-200 px-4 py-2">
          <div className="text-xs text-blue-800">
            <span className="font-medium">Context:</span> {selectedParameter.markdown_context.substring(0, 150)}...
          </div>
        </div>
      )}
    </div>
  );
};

export default MarkdownViewer;

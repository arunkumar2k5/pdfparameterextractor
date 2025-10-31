import React, { useState, useEffect } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import { ChevronLeft, ChevronRight, ZoomIn, ZoomOut, Maximize2 } from 'lucide-react';
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import { Parameter } from '../types';
import MarkdownViewer from './MarkdownViewer';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';

// Set up PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

interface PDFViewerProps {
  pdfUrl: string;
  markdownContent: string;
  selectedParameter: Parameter | null;
}

const PDFViewer: React.FC<PDFViewerProps> = ({ pdfUrl, markdownContent, selectedParameter }) => {
  const [numPages, setNumPages] = useState<number>(0);
  const [pageNumber, setPageNumber] = useState<number>(1);
  const [scale, setScale] = useState<number>(1.0);
  const [pageWidth, setPageWidth] = useState<number>(0);
  const [pageHeight, setPageHeight] = useState<number>(0);

  useEffect(() => {
    // Navigate to the page where the selected parameter was found
    if (selectedParameter?.source_page) {
      setPageNumber(selectedParameter.source_page);
    }
  }, [selectedParameter]);

  const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages);
  };

  const goToPrevPage = () => {
    setPageNumber(prev => Math.max(1, prev - 1));
  };

  const goToNextPage = () => {
    setPageNumber(prev => Math.min(numPages, prev + 1));
  };

  const zoomIn = () => {
    setScale(prev => Math.min(2.0, prev + 0.25));
  };

  const zoomOut = () => {
    setScale(prev => Math.max(0.5, prev - 0.25));
  };

  const resetZoom = () => {
    setScale(1.0);
  };

  if (!pdfUrl) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <Maximize2 className="mx-auto mb-4 text-gray-400" size={64} />
          <p className="text-gray-600 text-lg">No PDF loaded</p>
          <p className="text-gray-500 text-sm mt-2">Upload a PDF datasheet to view it here</p>
        </div>
      </div>
    );
  }

  return (
    <PanelGroup direction="vertical">
      {/* Top Panel - PDF Viewer */}
      <Panel defaultSize={50} minSize={30}>
        <div className="h-full flex flex-col bg-gray-100">
          {/* PDF Controls */}
          <div className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <button
            onClick={goToPrevPage}
            disabled={pageNumber <= 1}
            className="p-2 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            title="Previous page"
          >
            <ChevronLeft size={20} />
          </button>
          
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-600">Page</span>
            <input
              type="number"
              value={pageNumber}
              onChange={(e) => {
                const page = parseInt(e.target.value);
                if (page >= 1 && page <= numPages) {
                  setPageNumber(page);
                }
              }}
              className="w-16 px-2 py-1 text-sm border border-gray-300 rounded text-center"
              min={1}
              max={numPages}
            />
            <span className="text-sm text-gray-600">of {numPages}</span>
          </div>

          <button
            onClick={goToNextPage}
            disabled={pageNumber >= numPages}
            className="p-2 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            title="Next page"
          >
            <ChevronRight size={20} />
          </button>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={zoomOut}
            disabled={scale <= 0.5}
            className="p-2 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            title="Zoom out"
          >
            <ZoomOut size={20} />
          </button>
          
          <button
            onClick={resetZoom}
            className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-100"
          >
            {Math.round(scale * 100)}%
          </button>
          
          <button
            onClick={zoomIn}
            disabled={scale >= 2.0}
            className="p-2 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            title="Zoom in"
          >
            <ZoomIn size={20} />
          </button>
        </div>
      </div>

      {/* PDF Display */}
      <div className="flex-1 overflow-auto p-4">
        <div className="flex justify-center">
          <div className="bg-white shadow-lg relative">
            <Document
              file={pdfUrl}
              onLoadSuccess={onDocumentLoadSuccess}
              loading={
                <div className="flex items-center justify-center p-8">
                  <div className="text-gray-600">Loading PDF...</div>
                </div>
              }
              error={
                <div className="flex items-center justify-center p-8">
                  <div className="text-red-600">Failed to load PDF</div>
                </div>
              }
            >
              <Page
                pageNumber={pageNumber}
                scale={scale}
                renderTextLayer={true}
                renderAnnotationLayer={true}
                onLoadSuccess={(page) => {
                  setPageWidth(page.width);
                  setPageHeight(page.height);
                }}
              />
            </Document>
            
            {/* Highlight Overlays */}
            {selectedParameter && 
             selectedParameter.source_page === pageNumber && 
             selectedParameter.highlights && 
             selectedParameter.highlights.length > 0 && (
              <svg
                className="absolute top-0 left-0 pointer-events-none"
                style={{
                  width: pageWidth * scale,
                  height: pageHeight * scale,
                }}
              >
                {selectedParameter.highlights.map((highlight, index) => {
                  const [x0, y0, x1, y1] = highlight.bbox;
                  const color = highlight.type === 'parameter' ? 'rgba(59, 130, 246, 0.3)' : 'rgba(34, 197, 94, 0.3)';
                  const borderColor = highlight.type === 'parameter' ? 'rgb(59, 130, 246)' : 'rgb(34, 197, 94)';
                  
                  return (
                    <rect
                      key={index}
                      x={x0 * scale}
                      y={y0 * scale}
                      width={(x1 - x0) * scale}
                      height={(y1 - y0) * scale}
                      fill={color}
                      stroke={borderColor}
                      strokeWidth={2}
                    />
                  );
                })}
              </svg>
            )}
          </div>
        </div>
      </div>

          {/* Selected Parameter Info */}
          {selectedParameter && selectedParameter.value !== 'NF' && selectedParameter.value !== '' && (
            <div className="bg-blue-50 border-t border-blue-200 px-4 py-3">
              <div className="text-sm">
                <div className="font-medium text-blue-900 mb-1">
                  Selected: {selectedParameter.name}
                </div>
                <div className="text-blue-700">
                  <span className="font-medium">Value:</span> {selectedParameter.value} {selectedParameter.unit}
                </div>
                {selectedParameter.source_text && (
                  <div className="text-blue-600 text-xs mt-1 italic">
                    "{selectedParameter.source_text}"
                  </div>
                )}
                {selectedParameter.highlights && selectedParameter.highlights.length > 0 && (
                  <div className="flex gap-4 mt-2 text-xs">
                    <div className="flex items-center gap-1">
                      <div className="w-3 h-3 bg-blue-400 border border-blue-600"></div>
                      <span>Parameter Name</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <div className="w-3 h-3 bg-green-400 border border-green-600"></div>
                      <span>Value</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </Panel>

      {/* Resize Handle */}
      <PanelResizeHandle className="h-2 bg-gray-300 hover:bg-blue-500 transition-colors cursor-row-resize" />

      {/* Bottom Panel - Markdown Viewer */}
      <Panel defaultSize={50} minSize={30}>
        <MarkdownViewer 
          markdownContent={markdownContent}
          selectedParameter={selectedParameter}
        />
      </Panel>
    </PanelGroup>
  );
};

export default PDFViewer;

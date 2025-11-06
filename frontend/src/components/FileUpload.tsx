import React, { useRef, useState } from 'react';
import { Upload, FileText, FileSpreadsheet, PlayCircle, Sparkles } from 'lucide-react';
import axios from 'axios';
import { Parameter, ExtractionMetadata } from '../types';

interface FileUploadProps {
  onParametersUploaded: (parameters: string[]) => void;
  onPdfUploaded: (url: string) => void;
  onExtractionComplete: (results: Parameter[], metadata: ExtractionMetadata) => void;
  parametersCount: number;
  hasPdf: boolean;
  loading: boolean;
  setLoading: (loading: boolean) => void;
}

const API_BASE = 'http://localhost:8000';

const FileUpload: React.FC<FileUploadProps> = ({
  onParametersUploaded,
  onPdfUploaded,
  onExtractionComplete,
  parametersCount,
  hasPdf,
  loading,
  setLoading
}) => {
  const paramFileRef = useRef<HTMLInputElement>(null);
  const pdfFileRef = useRef<HTMLInputElement>(null);
  const [extractionMode, setExtractionMode] = useState<'simple' | 'ai'>('simple');

  const handleParameterFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE}/api/upload-parameters`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (response.data.success) {
        onParametersUploaded(response.data.parameters);
      }
    } catch (error: any) {
      alert('Error uploading parameter file: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handlePdfUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE}/api/upload-pdf`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (response.data.success) {
        onPdfUploaded(`${API_BASE}${response.data.pdf_url}`);
      }
    } catch (error: any) {
      alert('Error uploading PDF: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleExtract = async () => {
    if (!parametersCount || !hasPdf) {
      alert('Please upload both parameter list and PDF file first');
      return;
    }

    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE}/api/extract`, {
        mode: extractionMode
      });

      if (response.data.success) {
        // Add IDs to results
        const resultsWithIds = response.data.results.map((r: any, index: number) => ({
          ...r,
          id: `param-${index}`
        }));
        onExtractionComplete(resultsWithIds, response.data.metadata);
      }
    } catch (error: any) {
      alert('Error extracting parameters: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white border-b border-gray-200 px-6 py-4">
      {/* Extraction Mode Selection */}
      <div className="flex items-center gap-6 mb-4 pb-4 border-b border-gray-200">
        <div className="flex items-center gap-4">
          <span className="text-sm font-medium text-gray-700">Extraction Mode:</span>
          
          {/* Simple Mode Radio */}
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              name="extraction-mode"
              checked={extractionMode === 'simple'}
              onChange={() => setExtractionMode('simple')}
              className="w-4 h-4 text-blue-600 cursor-pointer"
            />
            <span className="text-sm font-medium text-gray-700">Simple Search</span>
          </label>
          
          {/* AI Mode Radio */}
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              name="extraction-mode"
              checked={extractionMode === 'ai'}
              onChange={() => setExtractionMode('ai')}
              className="w-4 h-4 text-purple-600 cursor-pointer"
            />
            <span className="flex items-center gap-1 text-sm font-medium text-gray-700">
              <Sparkles size={16} className="text-purple-600" />
              AI-Powered (OpenAI)
            </span>
          </label>
        </div>
        
        {/* Info message for AI mode */}
        {extractionMode === 'ai' && (
          <div className="text-xs text-gray-600 italic">
            Using OpenAI API key from backend/.env file
          </div>
        )}
      </div>
      
      <div className="flex items-center gap-4 flex-wrap">
        {/* Parameter File Upload */}
        <div className="flex items-center gap-2">
          <input
            ref={paramFileRef}
            type="file"
            accept=".csv,.xlsx,.xls,.json"
            onChange={handleParameterFileUpload}
            className="hidden"
          />
          <button
            onClick={() => paramFileRef.current?.click()}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            <FileSpreadsheet size={18} />
            Upload Parameters
          </button>
          {parametersCount > 0 && (
            <span className="text-sm text-green-600 font-medium">
              ✓ {parametersCount} parameters loaded
            </span>
          )}
        </div>

        {/* PDF Upload */}
        <div className="flex items-center gap-2">
          <input
            ref={pdfFileRef}
            type="file"
            accept=".pdf"
            onChange={handlePdfUpload}
            className="hidden"
          />
          <button
            onClick={() => pdfFileRef.current?.click()}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            <FileText size={18} />
            Upload PDF
          </button>
          {hasPdf && (
            <span className="text-sm text-green-600 font-medium">
              ✓ PDF loaded
            </span>
          )}
        </div>

        {/* Extract Button */}
        <button
          onClick={handleExtract}
          disabled={!parametersCount || !hasPdf || loading}
          className="flex items-center gap-2 px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
        >
          <PlayCircle size={18} />
          {loading ? 'Processing...' : 'Extract Parameters'}
        </button>
      </div>
    </div>
  );
};

export default FileUpload;

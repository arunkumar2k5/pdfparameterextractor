import React, { useState } from 'react';
import { Search, CheckCircle, AlertCircle, XCircle, Download, FileJson } from 'lucide-react';
import { Parameter, ExtractionMetadata } from '../types';

interface ParameterListProps {
  parameters: Parameter[];
  onParameterUpdate: (id: string, value: string) => void;
  onParameterSelect: (param: Parameter) => void;
  selectedParameter: Parameter | null;
  metadata: ExtractionMetadata | null;
}

const ParameterList: React.FC<ParameterListProps> = ({
  parameters,
  onParameterUpdate,
  onParameterSelect,
  selectedParameter,
  metadata
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filter, setFilter] = useState<'all' | 'found' | 'not_found' | 'low_confidence'>('all');

  const getStatusIcon = (param: Parameter) => {
    if (param.value === 'NF' || param.value === '') {
      return <XCircle className="text-red-500" size={18} />;
    }
    if (param.confidence < 70 && param.confidence > 0) {
      return <AlertCircle className="text-yellow-500" size={18} />;
    }
    return <CheckCircle className="text-green-500" size={18} />;
  };

  const getStatusColor = (param: Parameter) => {
    if (param.manually_edited) return 'bg-yellow-50 border-yellow-200';
    if (param.value === 'NF' || param.value === '') return 'bg-red-50 border-red-200';
    if (param.confidence < 70 && param.confidence > 0) return 'bg-yellow-50 border-yellow-200';
    return 'bg-green-50 border-green-200';
  };

  const filteredParameters = parameters.filter(param => {
    const matchesSearch = param.name.toLowerCase().includes(searchQuery.toLowerCase());
    
    if (filter === 'found') return matchesSearch && param.value !== 'NF' && param.value !== '';
    if (filter === 'not_found') return matchesSearch && (param.value === 'NF' || param.value === '');
    if (filter === 'low_confidence') return matchesSearch && param.confidence < 70 && param.confidence > 0;
    
    return matchesSearch;
  });

  const handleExportJSON = () => {
    const exportData = {
      metadata: {
        extraction_date: new Date().toISOString(),
        total_parameters: parameters.length,
        extracted_count: parameters.filter(p => p.value !== 'NF' && p.value !== '').length,
        not_found_count: parameters.filter(p => p.value === 'NF' || p.value === '').length,
        manually_edited_count: parameters.filter(p => p.manually_edited).length
      },
      parameters: parameters
    };

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `parameter-extraction-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleExportCSV = () => {
    const headers = ['Parameter Name', 'Value', 'Unit', 'Source Page', 'Confidence', 'Manually Edited'];
    const rows = parameters.map(p => [
      p.name,
      p.value,
      p.unit,
      p.source_page || 'N/A',
      p.confidence,
      p.manually_edited ? 'Yes' : 'No'
    ]);

    const csv = [headers, ...rows].map(row => row.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `parameter-extraction-${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-800 mb-3">Parameter Extraction Results</h2>
        
        {/* Search */}
        <div className="relative mb-3">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
          <input
            type="text"
            placeholder="Search parameters..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Filters */}
        <div className="flex gap-2 mb-3 flex-wrap">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1 rounded-full text-sm ${filter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'}`}
          >
            All ({parameters.length})
          </button>
          <button
            onClick={() => setFilter('found')}
            className={`px-3 py-1 rounded-full text-sm ${filter === 'found' ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-700'}`}
          >
            Found ({parameters.filter(p => p.value !== 'NF' && p.value !== '').length})
          </button>
          <button
            onClick={() => setFilter('not_found')}
            className={`px-3 py-1 rounded-full text-sm ${filter === 'not_found' ? 'bg-red-600 text-white' : 'bg-gray-200 text-gray-700'}`}
          >
            Not Found ({parameters.filter(p => p.value === 'NF' || p.value === '').length})
          </button>
          <button
            onClick={() => setFilter('low_confidence')}
            className={`px-3 py-1 rounded-full text-sm ${filter === 'low_confidence' ? 'bg-yellow-600 text-white' : 'bg-gray-200 text-gray-700'}`}
          >
            Low Confidence ({parameters.filter(p => p.confidence < 70 && p.confidence > 0).length})
          </button>
        </div>

        {/* Progress */}
        {metadata && (
          <div className="text-sm text-gray-600">
            <div className="flex justify-between mb-1">
              <span>Extraction Progress</span>
              <span className="font-medium">
                {metadata.extracted_count} / {metadata.total_parameters}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all"
                style={{ width: `${(metadata.extracted_count / metadata.total_parameters) * 100}%` }}
              />
            </div>
          </div>
        )}
      </div>

      {/* Parameter List */}
      <div className="flex-1 overflow-y-auto p-4">
        {filteredParameters.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            {parameters.length === 0 ? 'No parameters loaded' : 'No parameters match your search'}
          </div>
        ) : (
          <div className="space-y-2">
            {filteredParameters.map((param, index) => (
              <div
                key={param.id}
                onClick={() => onParameterSelect(param)}
                className={`border rounded-lg p-3 cursor-pointer transition-all ${
                  selectedParameter?.id === param.id ? 'ring-2 ring-blue-500' : ''
                } ${getStatusColor(param)}`}
              >
                <div className="flex items-start gap-2">
                  <div className="flex-shrink-0 mt-1">
                    {getStatusIcon(param)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium text-gray-700">
                        {index + 1}. {param.name}
                      </span>
                      {param.source_page && (
                        <span className="text-xs text-gray-500">
                          Page {param.source_page}
                        </span>
                      )}
                    </div>
                    <input
                      type="text"
                      value={param.value}
                      onChange={(e) => {
                        e.stopPropagation();
                        onParameterUpdate(param.id, e.target.value);
                      }}
                      onClick={(e) => e.stopPropagation()}
                      placeholder="Enter value or 'NF'"
                      className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
                    />
                    {param.confidence > 0 && (
                      <div className="mt-1 text-xs text-gray-500">
                        Confidence: {param.confidence}% | {param.extraction_method}
                      </div>
                    )}
                    {param.manually_edited && (
                      <div className="mt-1 text-xs text-yellow-700 font-medium">
                        ✏️ Manually edited
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Export Buttons */}
      <div className="p-4 border-t border-gray-200 bg-gray-50">
        <div className="flex gap-2">
          <button
            onClick={handleExportJSON}
            disabled={parameters.length === 0}
            className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            <FileJson size={18} />
            Export JSON
          </button>
          <button
            onClick={handleExportCSV}
            disabled={parameters.length === 0}
            className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            <Download size={18} />
            Export CSV
          </button>
        </div>
      </div>
    </div>
  );
};

export default ParameterList;

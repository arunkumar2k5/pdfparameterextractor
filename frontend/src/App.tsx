import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import ParameterList from './components/ParameterList';
import PDFViewer from './components/PDFViewer';
import GraphAnalysis from './components/GraphAnalysis';
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import { Parameter, ExtractionMetadata } from './types';
<<<<<<< HEAD
import { FileText, TrendingUp } from 'lucide-react';

type TabType = 'parameters' | 'graphs';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('parameters');
=======
import { FileText, BarChart3 } from 'lucide-react';

type TabType = 'extraction' | 'graph';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('extraction');
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
  const [parameters, setParameters] = useState<Parameter[]>([]);
  const [pdfUrl, setPdfUrl] = useState<string>('');
  const [markdownContent, setMarkdownContent] = useState<string>('');
  const [selectedParameter, setSelectedParameter] = useState<Parameter | null>(null);
  const [metadata, setMetadata] = useState<ExtractionMetadata | null>(null);
  const [loading, setLoading] = useState(false);

  const handleParametersUploaded = (params: string[]) => {
    const paramObjects: Parameter[] = params.map((name, index) => ({
      id: `param-${index}`,
      name,
      value: '',
      unit: '',
      source_page: null,
      extraction_method: 'pending',
      confidence: 0,
      manually_edited: false,
      source_text: '',
      notes: '',
      highlights: []
    }));
    setParameters(paramObjects);
  };

  const handlePdfUploaded = async (url: string) => {
    setPdfUrl(url);
    
    // Fetch markdown content
    try {
      const response = await fetch('http://localhost:8000/api/markdown');
      if (response.ok) {
        const data = await response.json();
        setMarkdownContent(data.markdown);
      }
    } catch (error) {
      console.error('Failed to fetch markdown:', error);
    }
  };

  const handleExtractionComplete = (results: Parameter[], meta: ExtractionMetadata) => {
    setParameters(results);
    setMetadata(meta);
  };

  const handleParameterUpdate = (id: string, value: string) => {
    setParameters(prev => prev.map(p => 
      p.id === id 
        ? { ...p, value, manually_edited: true } 
        : p
    ));
  };

  const handleParameterSelect = (param: Parameter) => {
    setSelectedParameter(param);
  };

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm">
        <h1 className="text-2xl font-bold text-gray-800">
          Engineering Parameter Extraction Tool
        </h1>
        <p className="text-sm text-gray-600 mt-1">
          Upload parameter lists and PDF datasheets for automated extraction
        </p>
      </header>

      {/* Tab Navigation */}
<<<<<<< HEAD
      <div className="bg-white border-b border-gray-200">
        <div className="px-6 flex space-x-1">
          <button
            onClick={() => setActiveTab('parameters')}
            className={`flex items-center px-4 py-3 font-medium text-sm transition-colors border-b-2 ${
              activeTab === 'parameters'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300'
            }`}
          >
            <FileText className="w-4 h-4 mr-2" />
            Parameter Extraction
          </button>
          <button
            onClick={() => setActiveTab('graphs')}
            className={`flex items-center px-4 py-3 font-medium text-sm transition-colors border-b-2 ${
              activeTab === 'graphs'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300'
            }`}
          >
            <TrendingUp className="w-4 h-4 mr-2" />
=======
      <div className="bg-white border-b border-gray-200 px-6">
        <div className="flex space-x-1">
          <button
            onClick={() => setActiveTab('extraction')}
            className={`flex items-center px-4 py-3 font-medium text-sm transition-colors border-b-2 ${
              activeTab === 'extraction'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300'
            }`}
          >
            <FileText className="mr-2" size={18} />
            Parameter Extraction
          </button>
          <button
            onClick={() => setActiveTab('graph')}
            className={`flex items-center px-4 py-3 font-medium text-sm transition-colors border-b-2 ${
              activeTab === 'graph'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300'
            }`}
          >
            <BarChart3 className="mr-2" size={18} />
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
            Graph Analysis
          </button>
        </div>
      </div>

      {/* Tab Content */}
<<<<<<< HEAD
      {activeTab === 'parameters' ? (
=======
      {activeTab === 'extraction' ? (
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
        <>
          {/* File Upload Section */}
          <FileUpload
            onParametersUploaded={handleParametersUploaded}
            onPdfUploaded={handlePdfUploaded}
            onExtractionComplete={handleExtractionComplete}
            parametersCount={parameters.length}
            hasPdf={!!pdfUrl}
            loading={loading}
            setLoading={setLoading}
          />

          {/* Main Content - Split View */}
          <div className="flex-1 overflow-hidden">
            <PanelGroup direction="horizontal">
              {/* Left Panel - Parameter List */}
              <Panel defaultSize={50} minSize={30}>
                <ParameterList
                  parameters={parameters}
                  onParameterUpdate={handleParameterUpdate}
                  onParameterSelect={handleParameterSelect}
                  selectedParameter={selectedParameter}
                  metadata={metadata}
                />
              </Panel>

              {/* Resize Handle */}
              <PanelResizeHandle className="w-2 bg-gray-300 hover:bg-blue-500 transition-colors cursor-col-resize" />

              {/* Right Panel - PDF Viewer */}
              <Panel defaultSize={50} minSize={30}>
                <PDFViewer
                  pdfUrl={pdfUrl}
                  markdownContent={markdownContent}
                  selectedParameter={selectedParameter}
                />
              </Panel>
            </PanelGroup>
          </div>
        </>
      ) : (
<<<<<<< HEAD
        <GraphAnalysis loading={loading} setLoading={setLoading} />
=======
        /* Graph Analysis Tab */
        <div className="flex-1 overflow-hidden">
          <GraphAnalysis />
        </div>
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
      )}
    </div>
  );
}

export default App;

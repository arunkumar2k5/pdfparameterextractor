import React, { useState } from 'react';
import { Upload, Send, Image as ImageIcon, Loader2, AlertCircle, CheckCircle } from 'lucide-react';

interface GraphAnalysisProps {
  // Add any props if needed
}

const GraphAnalysis: React.FC<GraphAnalysisProps> = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [prompt, setPrompt] = useState<string>('');
  const [response, setResponse] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [modelInfo, setModelInfo] = useState<{ model: string; provider: string } | null>(null);

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        setError('Please upload a valid image file (JPG, PNG, etc.)');
        return;
      }

      setSelectedImage(file);
      setError(null);
      setResponse('');
      setModelInfo(null);

      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedImage) {
      setError('Please upload an image first');
      return;
    }

    if (!prompt.trim()) {
      setError('Please enter a question or prompt');
      return;
    }

    setLoading(true);
    setError(null);
    setResponse('');

    try {
      const formData = new FormData();
      formData.append('file', selectedImage);
      formData.append('prompt', prompt);

      const res = await fetch('http://localhost:8000/api/analyze-graph', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }

      const data = await res.json();
      setResponse(data.answer);
      setModelInfo({ model: data.model, provider: data.provider });
    } catch (err: any) {
      setError(err.message || 'Failed to analyze graph');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setSelectedImage(null);
    setImagePreview(null);
    setPrompt('');
    setResponse('');
    setError(null);
    setModelInfo(null);
  };

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Header */}
      <div className="p-6 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Graph Analysis</h2>
        <p className="text-sm text-gray-600">
          Upload a graph image and ask questions about it using AI vision models
        </p>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="max-w-6xl mx-auto space-y-6">
          {/* Image Upload Section */}
          <div className="bg-white border-2 border-dashed border-gray-300 rounded-lg p-8 hover:border-blue-400 transition-colors">
            <div className="flex flex-col items-center justify-center space-y-4">
              {!imagePreview ? (
                <>
                  <ImageIcon className="text-gray-400" size={48} />
                  <div className="text-center">
                    <label
                      htmlFor="graph-upload"
                      className="cursor-pointer inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      <Upload className="mr-2" size={18} />
                      Upload Graph Image
                    </label>
                    <input
                      id="graph-upload"
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="hidden"
                    />
                    <p className="text-sm text-gray-500 mt-2">
                      Supports JPG, PNG, and other image formats
                    </p>
                  </div>
                </>
              ) : (
                <div className="w-full">
                  <div className="relative">
                    <img
                      src={imagePreview}
                      alt="Graph preview"
                      className="max-w-full max-h-96 mx-auto rounded-lg shadow-lg"
                    />
                    <button
                      onClick={handleClear}
                      className="absolute top-2 right-2 bg-red-500 text-white px-3 py-1 rounded-lg hover:bg-red-600 transition-colors text-sm"
                    >
                      Clear
                    </button>
                  </div>
                  <p className="text-sm text-gray-600 text-center mt-3">
                    {selectedImage?.name}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Prompt Section */}
          {imagePreview && (
            <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
              <label className="block text-sm font-semibold text-gray-700 mb-3">
                Ask a Question About the Graph
              </label>
              <div className="space-y-3">
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Example: What is the voltage at 0.6A at 25°C?"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  rows={3}
                />
                <div className="flex space-x-3">
                  <button
                    onClick={handleAnalyze}
                    disabled={loading || !prompt.trim()}
                    className="flex-1 flex items-center justify-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="mr-2 animate-spin" size={18} />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <Send className="mr-2" size={18} />
                        Analyze Graph
                      </>
                    )}
                  </button>
                </div>
              </div>

              {/* Quick Prompts */}
              <div className="mt-4">
                <p className="text-xs text-gray-500 mb-2">Quick prompts:</p>
                <div className="flex flex-wrap gap-2">
                  {[
                    'What is the equation of this graph?',
                    'Describe the relationship shown',
                    'What are the key characteristics?',
                  ].map((quickPrompt) => (
                    <button
                      key={quickPrompt}
                      onClick={() => setPrompt(quickPrompt)}
                      className="text-xs px-3 py-1 bg-white border border-gray-300 rounded-full hover:bg-gray-50 transition-colors"
                    >
                      {quickPrompt}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start space-x-3">
              <AlertCircle className="text-red-500 flex-shrink-0 mt-0.5" size={20} />
              <div>
                <p className="text-sm font-semibold text-red-800">Error</p>
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          )}

          {/* Response Display */}
          {response && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-6">
              <div className="flex items-start space-x-3 mb-4">
                <CheckCircle className="text-green-500 flex-shrink-0 mt-0.5" size={20} />
                <div className="flex-1">
                  <p className="text-sm font-semibold text-green-800 mb-1">Analysis Result</p>
                  {modelInfo && (
                    <p className="text-xs text-green-600">
                      Model: {modelInfo.model} ({modelInfo.provider})
                    </p>
                  )}
                </div>
              </div>
              <div className="bg-white rounded-lg p-4 border border-green-200">
                <pre className="whitespace-pre-wrap text-sm text-gray-800 font-sans">
                  {response}
                </pre>
              </div>
            </div>
          )}

          {/* Instructions */}
          {!imagePreview && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <h3 className="text-sm font-semibold text-blue-800 mb-3">How to Use</h3>
              <ol className="text-sm text-blue-700 space-y-2 list-decimal list-inside">
                <li>Upload a graph image (JPG, PNG, etc.)</li>
                <li>Enter your question in the text box</li>
                <li>Click "Analyze Graph" to get AI-powered insights</li>
                <li>The AI will analyze the graph and provide detailed answers</li>
              </ol>
              <div className="mt-4 pt-4 border-t border-blue-200">
                <p className="text-xs text-blue-600">
                  <strong>Example questions:</strong> "What is the voltage at 0.6A at 25°C?", 
                  "What is the equation of this graph?", "Describe the trend shown in this data"
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default GraphAnalysis;

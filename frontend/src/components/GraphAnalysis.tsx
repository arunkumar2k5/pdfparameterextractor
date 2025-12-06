import React, { useState } from 'react';
<<<<<<< HEAD
import { Upload, Image as ImageIcon, Zap, Calculator, AlertCircle } from 'lucide-react';
import { GraphCurve, GraphAnalysisResult } from '../types';
import { evaluate } from 'mathjs';

interface GraphAnalysisProps {
  loading: boolean;
  setLoading: (loading: boolean) => void;
}

const GraphAnalysis: React.FC<GraphAnalysisProps> = ({ loading, setLoading }) => {
  const [graphImage, setGraphImage] = useState<string | null>(null);
  const [graphFile, setGraphFile] = useState<File | null>(null);
  const [curves, setCurves] = useState<GraphCurve[]>([]);
  const [graphDescription, setGraphDescription] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [xValues, setXValues] = useState<{ [key: string]: string }>({});
  const [yResults, setYResults] = useState<{ [key: string]: number | string }>({});
  const [customQuestion, setCustomQuestion] = useState<string>('');
  const [questionAnswer, setQuestionAnswer] = useState<string>('');
=======
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
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
<<<<<<< HEAD
=======
      // Validate file type
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
      if (!file.type.startsWith('image/')) {
        setError('Please upload a valid image file (JPG, PNG, etc.)');
        return;
      }

<<<<<<< HEAD
      setGraphFile(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setGraphImage(e.target?.result as string);
        setError('');
        setCurves([]);
        setGraphDescription('');
=======
      setSelectedImage(file);
      setError(null);
      setResponse('');
      setModelInfo(null);

      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
      };
      reader.readAsDataURL(file);
    }
  };

<<<<<<< HEAD
  const handleProcessGraph = async () => {
    if (!graphFile) {
      setError('Please upload a graph image first');
=======
  const handleAnalyze = async () => {
    if (!selectedImage) {
      setError('Please upload an image first');
      return;
    }

    if (!prompt.trim()) {
      setError('Please enter a question or prompt');
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
      return;
    }

    setLoading(true);
<<<<<<< HEAD
    setError('');
    setQuestionAnswer(''); // Clear previous answer

    try {
      const formData = new FormData();
      formData.append('file', graphFile);
      
      // Add custom question if provided
      if (customQuestion.trim()) {
        console.log('📝 Sending question:', customQuestion.trim());
        formData.append('question', customQuestion.trim());
      } else {
        console.log('📊 No question - extracting equations');
      }

      const response = await fetch('http://localhost:8000/api/analyze-graph', {
=======
    setError(null);
    setResponse('');

    try {
      const formData = new FormData();
      formData.append('file', selectedImage);
      formData.append('prompt', prompt);

      const res = await fetch('http://localhost:8000/api/analyze-graph', {
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
        method: 'POST',
        body: formData,
      });

<<<<<<< HEAD
      if (!response.ok) {
        throw new Error('Failed to analyze graph');
      }

      const data: GraphAnalysisResult = await response.json();
      
      console.log('📥 Received response:', data);

      if (data.success) {
        // If there's a question answer, display it
        if (data.question_answer) {
          console.log('✅ Got answer:', data.question_answer);
          setQuestionAnswer(data.question_answer);
          setCurves([]); // Clear curves when answering questions
        } else {
          console.log('✅ Got equations:', data.curves.length, 'curves');
          // Normal equation extraction mode
          setCurves(data.curves);
          setGraphDescription(data.graph_description || '');
          
          // Initialize x values for each curve
          const initialXValues: { [key: string]: string } = {};
          data.curves.forEach(curve => {
            initialXValues[curve.id] = '';
          });
          setXValues(initialXValues);
          setYResults({});
        }
      } else {
        setError(data.error || 'Failed to analyze graph');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
=======
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }

      const data = await res.json();
      setResponse(data.answer);
      setModelInfo({ model: data.model, provider: data.provider });
    } catch (err: any) {
      setError(err.message || 'Failed to analyze graph');
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
    } finally {
      setLoading(false);
    }
  };

<<<<<<< HEAD
  const handleXValueChange = (curveId: string, value: string) => {
    setXValues(prev => ({ ...prev, [curveId]: value }));
    
    // Auto-calculate y when x is entered
    if (value.trim() !== '') {
      calculateY(curveId, value);
    } else {
      setYResults(prev => {
        const newResults = { ...prev };
        delete newResults[curveId];
        return newResults;
      });
    }
  };

  const calculateY = (curveId: string, xValueStr: string) => {
    const curve = curves.find(c => c.id === curveId);
    if (!curve) return;

    try {
      const xValue = parseFloat(xValueStr);
      if (isNaN(xValue)) {
        setYResults(prev => ({ ...prev, [curveId]: 'Invalid x value' }));
        return;
      }

      // Remove "y = " prefix if present and clean the equation
      let equation = curve.equation.replace(/^y\s*=\s*/i, '').trim();
      
      console.log('Original equation:', curve.equation);
      console.log('Cleaned equation:', equation);
      console.log('X value:', xValue);
      
      // Replace common mathematical notations
      equation = equation
        .replace(/\^/g, '^')  // Power
        .replace(/×/g, '*')   // Multiplication
        .replace(/÷/g, '/')   // Division
        .replace(/\s+/g, ''); // Remove spaces

      console.log('Final equation for evaluation:', equation);

      // Evaluate the equation
      const yValue = evaluate(equation, { x: xValue });
      
      console.log('Calculated Y value:', yValue);
      
      setYResults(prev => ({ ...prev, [curveId]: typeof yValue === 'number' ? yValue : String(yValue) }));
    } catch (err) {
      console.error('Calculation error for curve:', curve.name);
      console.error('Equation:', curve.equation);
      console.error('Error:', err);
      setYResults(prev => ({ ...prev, [curveId]: `Error: ${err instanceof Error ? err.message : 'Invalid equation'}` }));
    }
  };

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <h2 className="text-xl font-bold text-gray-800">Graph Analysis</h2>
        <p className="text-sm text-gray-600 mt-1">
          Upload a graph image to extract equations using AI
        </p>
      </div>

      {/* Upload Section */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        {/* Image Upload */}
        <div className="mb-4">
          <label className="flex items-center justify-center px-4 py-2 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-colors">
            <Upload className="w-5 h-5 mr-2 text-gray-600" />
            <span className="text-sm font-medium text-gray-700">
              {graphFile ? graphFile.name : 'Upload Graph (JPG, PNG)'}
            </span>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              className="hidden"
            />
          </label>
        </div>

        {/* Custom Question Input */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Ask a question about the graph (optional):
          </label>
          <input
            type="text"
            value={customQuestion}
            onChange={(e) => setCustomQuestion(e.target.value)}
            placeholder='e.g., "What is the dropout voltage at 25°C at 0.6A current?"'
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p className="text-xs text-gray-500 mt-1">
            💡 Leave blank to extract equations automatically, or enter a specific question to get an answer
          </p>
        </div>

        {/* Process Button - Now below question */}
        <div className="mb-4">
          <button
            onClick={handleProcessGraph}
            disabled={!graphFile || loading}
            className={`w-full flex items-center justify-center px-6 py-3 rounded-lg font-medium transition-colors ${
              !graphFile || loading
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            <Zap className="w-5 h-5 mr-2" />
            {loading ? 'Processing...' : 'Process Graph'}
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="flex items-center gap-2 text-red-600 bg-red-50 px-4 py-2 rounded-lg">
            <AlertCircle className="w-5 h-5" />
            <span className="text-sm">{error}</span>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left: Image Display */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <ImageIcon className="w-5 h-5 mr-2" />
              Uploaded Graph
            </h3>
            {graphImage ? (
              <div className="border border-gray-300 rounded-lg overflow-hidden">
                <img
                  src={graphImage}
                  alt="Uploaded graph"
                  className="w-full h-auto"
                />
              </div>
            ) : (
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
                <ImageIcon className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                <p className="text-gray-500">No graph uploaded yet</p>
              </div>
            )}

            {/* Graph Description */}
            {graphDescription && (
              <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                <p className="text-sm text-gray-700">{graphDescription}</p>
              </div>
            )}
          </div>

          {/* Right: Equations/Answer Display */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <Calculator className="w-5 h-5 mr-2" />
              {questionAnswer ? 'Answer' : 'Extracted Equations'}
            </h3>

            {/* Display Answer if question was asked */}
            {questionAnswer ? (
              <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                <h4 className="font-semibold text-green-800 mb-3">
                  Question: {customQuestion}
                </h4>
                <div className="bg-white p-4 rounded-lg">
                  <p className="text-gray-800 whitespace-pre-wrap">{questionAnswer}</p>
                </div>
                <button
                  onClick={() => {
                    setQuestionAnswer('');
                    setCustomQuestion('');
                  }}
                  className="mt-4 text-sm text-blue-600 hover:text-blue-800"
                >
                  ← Ask another question or extract equations
                </button>
              </div>
            ) : curves.length === 0 ? (
              <div className="text-center py-12">
                <Calculator className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                <p className="text-gray-500">
                  Upload and process a graph to see equations or get answers
                </p>
              </div>
            ) : (
              <div className="space-y-6">
                {curves.map((curve) => (
                  <div
                    key={curve.id}
                    className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                  >
                    {/* Curve Name */}
                    <h4 className="font-semibold text-gray-800 mb-2">
                      {curve.name}
                    </h4>

                    {/* Equation */}
                    <div className="bg-gray-50 p-3 rounded-lg mb-3">
                      <p className="text-sm text-gray-600 mb-1">Equation:</p>
                      <p className="font-mono text-lg text-blue-600">
                        {curve.equation}
                      </p>
                      {/* Warning if equation looks like descriptive text */}
                      {!curve.equation.match(/[0-9+\-*/^()]/g) && (
                        <p className="text-xs text-orange-600 mt-2">
                          ⚠️ Warning: This appears to be descriptive text, not a mathematical equation. 
                          Try re-processing the graph for better results.
                        </p>
                      )}
                    </div>

                    {/* Axis Labels */}
                    <div className="grid grid-cols-2 gap-2 mb-3 text-sm">
                      <div>
                        <span className="text-gray-600">X-axis: </span>
                        <span className="font-medium">{curve.x_axis}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Y-axis: </span>
                        <span className="font-medium">{curve.y_axis}</span>
                      </div>
                    </div>

                    {/* X Range */}
                    {curve.x_range && (
                      <div className="text-sm mb-3">
                        <span className="text-gray-600">Range: </span>
                        <span className="font-medium">{curve.x_range}</span>
                      </div>
                    )}

                    {/* Notes */}
                    {curve.notes && (
                      <div className="text-sm text-gray-600 mb-3 italic">
                        {curve.notes}
                      </div>
                    )}

                    {/* X Input and Y Result */}
                    <div className="border-t border-gray-200 pt-3">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Enter X value to calculate Y:
                      </label>
                      <div className="flex items-center gap-3">
                        <div className="flex-1">
                          <input
                            type="number"
                            step="any"
                            value={xValues[curve.id] || ''}
                            onChange={(e) => handleXValueChange(curve.id, e.target.value)}
                            placeholder="Enter x value"
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                        </div>
                        <div className="flex-1">
                          <div className="px-3 py-2 bg-green-50 border border-green-300 rounded-lg">
                            <span className="text-sm text-gray-600">Y = </span>
                            <span className="font-semibold text-green-700">
                              {yResults[curve.id] !== undefined
                                ? typeof yResults[curve.id] === 'number'
                                  ? (yResults[curve.id] as number).toFixed(4)
                                  : yResults[curve.id]
                                : '—'}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
=======
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
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
        </div>
      </div>
    </div>
  );
};

export default GraphAnalysis;

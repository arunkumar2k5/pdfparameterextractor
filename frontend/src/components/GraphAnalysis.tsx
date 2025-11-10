import React, { useState } from 'react';
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

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (!file.type.startsWith('image/')) {
        setError('Please upload a valid image file (JPG, PNG, etc.)');
        return;
      }

      setGraphFile(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setGraphImage(e.target?.result as string);
        setError('');
        setCurves([]);
        setGraphDescription('');
      };
      reader.readAsDataURL(file);
    }
  };

  const handleProcessGraph = async () => {
    if (!graphFile) {
      setError('Please upload a graph image first');
      return;
    }

    setLoading(true);
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
        method: 'POST',
        body: formData,
      });

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
    } finally {
      setLoading(false);
    }
  };

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
        </div>
      </div>
    </div>
  );
};

export default GraphAnalysis;

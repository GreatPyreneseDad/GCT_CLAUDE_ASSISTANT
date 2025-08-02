import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, CheckCircle, Info, MessageSquare } from 'lucide-react';
import GCTApiClient from '@/lib/api-client';
import { CoherenceProfile, CommunicationAnalysis } from '@/types';

interface CommunicationSectionProps {
  apiClient: GCTApiClient;
  userId: string;
  currentProfile: CoherenceProfile | null;
}

const CommunicationSection: React.FC<CommunicationSectionProps> = ({
  apiClient,
  userId,
  currentProfile
}) => {
  const [text, setText] = useState('');
  const [analysis, setAnalysis] = useState<CommunicationAnalysis | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    
    setIsAnalyzing(true);
    try {
      const result = await apiClient.analyzeCommunication(text, currentProfile ? userId : undefined);
      setAnalysis(result);
    } catch (error) {
      console.error('Analysis error:', error);
    }
    setIsAnalyzing(false);
  };

  const getScoreColor = (score: number) => {
    if (score > 0.7) return 'text-green-600';
    if (score > 0.4) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Analyze Communication</h3>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text to analyze for coherence patterns..."
          className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <div className="flex justify-between items-center mt-4">
          <span className="text-sm text-gray-500">{text.length} characters</span>
          <button
            onClick={handleAnalyze}
            disabled={!text.trim() || isAnalyzing}
            className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors"
          >
            {isAnalyzing ? 'Analyzing...' : 'Analyze Text'}
          </button>
        </div>
      </div>

      {/* Results Section */}
      {analysis && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Coherence Scores */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h4 className="text-lg font-semibold mb-4">Coherence Analysis</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className={`text-2xl font-bold ${getScoreColor(analysis.consistency_score)}`}>
                  {(analysis.consistency_score * 100).toFixed(0)}%
                </div>
                <div className="text-sm text-gray-600 mt-1">Consistency</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className={`text-2xl font-bold ${getScoreColor(analysis.wisdom_indicators)}`}>
                  {(analysis.wisdom_indicators * 100).toFixed(0)}%
                </div>
                <div className="text-sm text-gray-600 mt-1">Wisdom</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className={`text-2xl font-bold ${getScoreColor(analysis.moral_activation)}`}>
                  {(analysis.moral_activation * 100).toFixed(0)}%
                </div>
                <div className="text-sm text-gray-600 mt-1">Moral Activation</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className={`text-2xl font-bold ${getScoreColor(analysis.social_awareness)}`}>
                  {(analysis.social_awareness * 100).toFixed(0)}%
                </div>
                <div className="text-sm text-gray-600 mt-1">Social Awareness</div>
              </div>
            </div>

            <div className="mt-6 p-4 bg-indigo-50 rounded-lg">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-indigo-900">Overall Authenticity Score</span>
                <span className={`text-2xl font-bold ${getScoreColor(analysis.authenticity_score)}`}>
                  {(analysis.authenticity_score * 100).toFixed(0)}%
                </span>
              </div>
              <div className="mt-2 text-xs text-indigo-700">
                Confidence Level: {(analysis.confidence_level * 100).toFixed(0)}%
              </div>
            </div>
          </div>

          {/* Red Flags */}
          {analysis.red_flags.length > 0 && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-6">
              <div className="flex items-start space-x-3">
                <AlertTriangle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-semibold text-red-900 mb-2">Potential Issues Detected</h4>
                  <ul className="space-y-1">
                    {analysis.red_flags.map((flag, index) => (
                      <li key={index} className="text-sm text-red-800">• {flag}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* Enhancement Suggestions */}
          {analysis.enhancement_suggestions.length > 0 && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-6">
              <div className="flex items-start space-x-3">
                <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-semibold text-green-900 mb-2">Enhancement Suggestions</h4>
                  <ul className="space-y-1">
                    {analysis.enhancement_suggestions.map((suggestion, index) => (
                      <li key={index} className="text-sm text-green-800">• {suggestion}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </motion.div>
      )}

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-start space-x-3">
        <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
        <div className="text-sm text-blue-800">
          <p className="font-semibold mb-1">How Communication Analysis Works</p>
          <p>
            The system analyzes text for coherence patterns across four dimensions: consistency, 
            wisdom indicators, moral activation, and social awareness. It can detect potential 
            manipulation patterns and suggest improvements for more authentic communication.
          </p>
        </div>
      </div>
    </div>
  );
};

export default CommunicationSection;
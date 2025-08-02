import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Users, TrendingUp, AlertCircle, Lightbulb } from 'lucide-react';
import GCTApiClient from '@/lib/api-client';
import { CoherenceProfile, RelationshipAnalysis } from '@/types';

interface RelationshipSectionProps {
  apiClient: GCTApiClient;
  userId: string;
  currentProfile: CoherenceProfile | null;
}

const RelationshipSection: React.FC<RelationshipSectionProps> = ({
  apiClient,
  userId,
  currentProfile
}) => {
  const [otherUserId, setOtherUserId] = useState('');
  const [analysis, setAnalysis] = useState<RelationshipAnalysis | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleAnalyze = async () => {
    if (!currentProfile || !otherUserId.trim()) return;

    setIsAnalyzing(true);
    try {
      const result = await apiClient.analyzeRelationship(userId, otherUserId);
      setAnalysis(result);
    } catch (error) {
      console.error('Relationship analysis error:', error);
      alert('Both users need to have completed assessments for relationship analysis.');
    }
    setIsAnalyzing(false);
  };

  if (!currentProfile) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
        <p className="text-yellow-800">
          Please complete an assessment first to use relationship analysis features.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Analyze Relationship Compatibility</h3>
        <p className="text-sm text-gray-600 mb-4">
          Enter the User ID of another person who has completed an assessment to analyze your compatibility.
        </p>
        <div className="flex space-x-4">
          <input
            type="text"
            value={otherUserId}
            onChange={(e) => setOtherUserId(e.target.value)}
            placeholder="Enter other user's ID"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <button
            onClick={handleAnalyze}
            disabled={!otherUserId.trim() || isAnalyzing}
            className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors"
          >
            {isAnalyzing ? 'Analyzing...' : 'Analyze'}
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
          {/* Overall Compatibility */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h4 className="text-lg font-semibold mb-4">Compatibility Overview</h4>
            <div className="text-center p-6 bg-indigo-50 rounded-lg">
              <div className="text-4xl font-bold text-indigo-600">
                {(analysis.overall_compatibility * 100).toFixed(0)}%
              </div>
              <div className="text-sm text-indigo-700 mt-2">Overall Compatibility Score</div>
            </div>

            {/* Variable Compatibility */}
            <div className="grid grid-cols-2 gap-4 mt-6">
              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="text-sm text-gray-600">Internal Consistency</div>
                <div className="text-xl font-semibold">
                  {(analysis.variable_compatibility.internal_consistency * 100).toFixed(0)}%
                </div>
              </div>
              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="text-sm text-gray-600">Accumulated Wisdom</div>
                <div className="text-xl font-semibold">
                  {(analysis.variable_compatibility.accumulated_wisdom * 100).toFixed(0)}%
                </div>
              </div>
              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="text-sm text-gray-600">Moral Activation</div>
                <div className="text-xl font-semibold">
                  {(analysis.variable_compatibility.moral_activation * 100).toFixed(0)}%
                </div>
              </div>
              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="text-sm text-gray-600">Social Belonging</div>
                <div className="text-xl font-semibold">
                  {(analysis.variable_compatibility.social_belonging * 100).toFixed(0)}%
                </div>
              </div>
            </div>
          </div>

          {/* Transmission Dynamics */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h4 className="text-lg font-semibold mb-4 flex items-center">
              <TrendingUp className="w-5 h-5 mr-2" />
              Influence Dynamics
            </h4>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-sm">Your influence on them</span>
                <span className="font-semibold">
                  {(analysis.transmission_dynamics.a_to_b_influence * 100).toFixed(0)}%
                </span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-sm">Their influence on you</span>
                <span className="font-semibold">
                  {(analysis.transmission_dynamics.b_to_a_influence * 100).toFixed(0)}%
                </span>
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Dominant influencer: {analysis.transmission_dynamics.dominant_influencer === 'A' ? 'You' : 'Them'}
              </div>
            </div>
          </div>

          {/* Growth Opportunities */}
          {analysis.growth_opportunities.length > 0 && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-6">
              <h4 className="font-semibold text-green-900 mb-3 flex items-center">
                <Lightbulb className="w-5 h-5 mr-2" />
                Growth Opportunities
              </h4>
              <ul className="space-y-2">
                {analysis.growth_opportunities.map((opportunity, index) => (
                  <li key={index} className="text-sm text-green-800">• {opportunity}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Potential Conflicts */}
          {analysis.potential_conflicts.length > 0 && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
              <h4 className="font-semibold text-yellow-900 mb-3 flex items-center">
                <AlertCircle className="w-5 h-5 mr-2" />
                Potential Challenges
              </h4>
              <ul className="space-y-2">
                {analysis.potential_conflicts.map((conflict, index) => (
                  <li key={index} className="text-sm text-yellow-800">• {conflict}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommendations */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h4 className="font-semibold text-blue-900 mb-3">Relationship Recommendations</h4>
            <ul className="space-y-2">
              {analysis.relationship_recommendations.map((rec, index) => (
                <li key={index} className="text-sm text-blue-800">• {rec}</li>
              ))}
            </ul>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default RelationshipSection;
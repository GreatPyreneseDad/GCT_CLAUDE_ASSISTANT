import React from 'react';
import { motion } from 'framer-motion';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';
import { TrendingUp, Award, Target, Brain } from 'lucide-react';
import { CoherenceProfile } from '@/types';

interface InsightsSectionProps {
  currentProfile: CoherenceProfile | null;
}

const InsightsSection: React.FC<InsightsSectionProps> = ({ currentProfile }) => {
  if (!currentProfile) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
        <p className="text-yellow-800">
          Please complete an assessment first to view your insights.
        </p>
      </div>
    );
  }

  const radarData = [
    {
      variable: 'Consistency (Ψ)',
      value: currentProfile.variables.psi * 100,
      fullMark: 100,
    },
    {
      variable: 'Wisdom (ρ)',
      value: currentProfile.variables.rho * 100,
      fullMark: 100,
    },
    {
      variable: 'Moral Energy (q)',
      value: currentProfile.variables.q * 100,
      fullMark: 100,
    },
    {
      variable: 'Social Belonging (f)',
      value: currentProfile.variables.f * 100,
      fullMark: 100,
    },
  ];

  const getVariableLabel = (key: string): string => {
    const labels: Record<string, string> = {
      psi: 'Internal Consistency',
      rho: 'Accumulated Wisdom',
      q: 'Moral Activation Energy',
      f: 'Social Belonging Architecture'
    };
    return labels[key] || key;
  };

  return (
    <div className="space-y-6">
      {/* Overall Coherence Score */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-lg shadow-sm p-6"
      >
        <h3 className="text-lg font-semibold mb-4">Your Coherence Profile</h3>
        
        <div className="text-center p-8 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-lg">
          <div className="text-5xl font-bold text-indigo-600">
            {currentProfile.static_coherence ? currentProfile.static_coherence.toFixed(2) : '0.00'}
          </div>
          <div className="text-lg text-indigo-700 mt-2">Static Coherence Score</div>
          {currentProfile.coherence_velocity !== undefined && currentProfile.coherence_velocity !== null && (
            <div className="mt-4 flex items-center justify-center space-x-2">
              <TrendingUp className="w-5 h-5 text-indigo-600" />
              <span className="text-sm text-indigo-700">
                Velocity: {currentProfile.coherence_velocity.toFixed(3)} per day
              </span>
            </div>
          )}
        </div>

        {/* Radar Chart */}
        <div className="mt-8">
          <h4 className="text-md font-semibold mb-4">Variable Distribution</h4>
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={radarData}>
              <PolarGrid strokeDasharray="3 3" />
              <PolarAngleAxis dataKey="variable" />
              <PolarRadiusAxis angle={90} domain={[0, 100]} />
              <Radar
                name="Your Profile"
                dataKey="value"
                stroke="#6366f1"
                fill="#6366f1"
                fillOpacity={0.6}
              />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      {/* Insights */}
      {currentProfile.insights && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Strongest & Development Areas */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h4 className="font-semibold mb-4 flex items-center">
              <Award className="w-5 h-5 mr-2 text-green-600" />
              Strengths & Development
            </h4>
            <div className="space-y-4">
              <div className="p-4 bg-green-50 rounded-lg">
                <div className="text-sm text-green-700 font-medium">Strongest Area</div>
                <div className="text-lg font-semibold text-green-900">
                  {getVariableLabel(currentProfile.insights.strongest_area)}
                </div>
              </div>
              <div className="p-4 bg-yellow-50 rounded-lg">
                <div className="text-sm text-yellow-700 font-medium">Development Area</div>
                <div className="text-lg font-semibold text-yellow-900">
                  {getVariableLabel(currentProfile.insights.development_area)}
                </div>
              </div>
            </div>
          </div>

          {/* Leadership & Innovation */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h4 className="font-semibold mb-4 flex items-center">
              <Target className="w-5 h-5 mr-2 text-indigo-600" />
              Readiness Indicators
            </h4>
            <div className="space-y-4">
              {currentProfile.insights.leadership_readiness && (
                <div className="p-4 bg-indigo-50 rounded-lg">
                  <div className="text-sm text-indigo-700 font-medium">Leadership Readiness</div>
                  <div className="text-lg font-semibold text-indigo-900 capitalize">
                    {currentProfile.insights.leadership_readiness}
                  </div>
                </div>
              )}
              {currentProfile.insights.innovation_timing && (
                <div className="p-4 bg-purple-50 rounded-lg">
                  <div className="text-sm text-purple-700 font-medium">Innovation Timing</div>
                  <div className="text-lg font-semibold text-purple-900">
                    {currentProfile.insights.innovation_timing.replace(/_/g, ' ')}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Key Recommendations */}
      {currentProfile.insights?.key_recommendations && 
       currentProfile.insights.key_recommendations.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h4 className="font-semibold mb-4 flex items-center">
            <Brain className="w-5 h-5 mr-2 text-indigo-600" />
            Personalized Recommendations
          </h4>
          <ul className="space-y-3">
            {currentProfile.insights.key_recommendations.map((rec, index) => (
              <li key={index} className="flex items-start space-x-3">
                <span className="text-indigo-600 font-semibold">{index + 1}.</span>
                <span className="text-gray-700">{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Individual Optimization Parameters */}
      {currentProfile.individual_optimization && 
       Object.keys(currentProfile.individual_optimization).length > 0 && (
        <div className="bg-gray-50 rounded-lg p-6">
          <h4 className="text-sm font-semibold text-gray-700 mb-3">
            Individual Optimization Parameters
          </h4>
          <div className="flex space-x-6">
            {Object.entries(currentProfile.individual_optimization).map(([key, value]) => (
              <div key={key} className="text-center">
                <div className="text-xs text-gray-600">{key}</div>
                <div className="text-lg font-semibold text-gray-800">
                  {(value as number).toFixed(3)}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default InsightsSection;
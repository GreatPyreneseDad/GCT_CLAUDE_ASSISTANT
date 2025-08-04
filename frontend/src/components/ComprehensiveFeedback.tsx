import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  TrendingUp, TrendingDown, Minus, Target, Lightbulb, 
  CheckCircle, AlertCircle, BookOpen, Users, Brain, Heart,
  ChevronDown, ChevronUp, BarChart3, Sparkles
} from 'lucide-react';

interface FeedbackProps {
  profile: any;
  insights: any;
}

export function ComprehensiveFeedback({ profile, insights }: FeedbackProps) {
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    trajectory: true,
    dimensions: false,
    themes: true,
    actions: true
  });

  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({ ...prev, [section]: !prev[section] }));
  };

  const narrative = insights?.narrative_feedback;
  if (!narrative) return null;

  // Determine trajectory icon and color
  const getTrajectoryIcon = () => {
    const growth = narrative.probability_assessment?.growth || 0;
    const decline = narrative.probability_assessment?.decline || 0;
    
    if (growth > 0.6) return { icon: TrendingUp, color: 'text-green-600' };
    if (decline > 0.6) return { icon: TrendingDown, color: 'text-red-600' };
    return { icon: Minus, color: 'text-yellow-600' };
  };

  const { icon: TrajectoryIcon, color: trajectoryColor } = getTrajectoryIcon();

  // Dimension icons
  const dimensionIcons = {
    psi: Brain,
    rho: BookOpen,
    q: Target,
    f: Users
  };

  const dimensionNames = {
    psi: 'Internal Consistency',
    rho: 'Wisdom Integration',
    q: 'Moral Activation',
    f: 'Social Belonging'
  };

  return (
    <div className="space-y-6">
      {/* Overall Summary Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl p-6 shadow-lg"
      >
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Your Coherence Profile: {narrative.coherence_state}
            </h2>
            <div className="flex items-center space-x-2">
              <div className="text-3xl font-bold text-indigo-600">
                {profile.static_coherence.toFixed(2)}
              </div>
              <TrajectoryIcon className={`w-6 h-6 ${trajectoryColor}`} />
            </div>
          </div>
          <Sparkles className="w-8 h-8 text-indigo-400" />
        </div>
        
        <p className="text-gray-700 leading-relaxed">
          {narrative.overall_summary}
        </p>
      </motion.div>

      {/* Trajectory Analysis */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white rounded-lg shadow-md overflow-hidden"
      >
        <button
          onClick={() => toggleSection('trajectory')}
          className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
        >
          <div className="flex items-center space-x-3">
            <BarChart3 className="w-5 h-5 text-indigo-600" />
            <h3 className="text-lg font-semibold">Trajectory Analysis</h3>
          </div>
          {expandedSections.trajectory ? <ChevronUp /> : <ChevronDown />}
        </button>
        
        <AnimatePresence>
          {expandedSections.trajectory && (
            <motion.div
              initial={{ height: 0 }}
              animate={{ height: 'auto' }}
              exit={{ height: 0 }}
              className="overflow-hidden"
            >
              <div className="px-6 pb-4">
                <p className="text-gray-700 mb-4">
                  {narrative.trajectory_analysis}
                </p>
                
                {/* Probability Bars */}
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-600">Growth Probability</span>
                      <span className="font-semibold text-green-600">
                        {((narrative.probability_assessment?.growth || 0) * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-green-500 transition-all duration-500"
                        style={{ width: `${(narrative.probability_assessment?.growth || 0) * 100}%` }}
                      />
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-600">Stability Probability</span>
                      <span className="font-semibold text-yellow-600">
                        {((narrative.probability_assessment?.stable || 0) * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-yellow-500 transition-all duration-500"
                        style={{ width: `${(narrative.probability_assessment?.stable || 0) * 100}%` }}
                      />
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-600">Decline Risk</span>
                      <span className="font-semibold text-red-600">
                        {((narrative.probability_assessment?.decline || 0) * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-red-500 transition-all duration-500"
                        style={{ width: `${(narrative.probability_assessment?.decline || 0) * 100}%` }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Dimension Narratives */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-lg shadow-md overflow-hidden"
      >
        <button
          onClick={() => toggleSection('dimensions')}
          className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
        >
          <div className="flex items-center space-x-3">
            <Brain className="w-5 h-5 text-indigo-600" />
            <h3 className="text-lg font-semibold">Detailed Dimension Analysis</h3>
          </div>
          {expandedSections.dimensions ? <ChevronUp /> : <ChevronDown />}
        </button>
        
        <AnimatePresence>
          {expandedSections.dimensions && (
            <motion.div
              initial={{ height: 0 }}
              animate={{ height: 'auto' }}
              exit={{ height: 0 }}
              className="overflow-hidden"
            >
              <div className="px-6 pb-4 space-y-4">
                {Object.entries(narrative.dimension_narratives || {}).map(([dim, text]) => {
                  const Icon = dimensionIcons[dim as keyof typeof dimensionIcons];
                  const score = profile.variables[dim];
                  
                  return (
                    <div key={dim} className="border-l-4 border-indigo-200 pl-4">
                      <div className="flex items-center space-x-2 mb-2">
                        <Icon className="w-5 h-5 text-indigo-600" />
                        <h4 className="font-semibold">{dimensionNames[dim as keyof typeof dimensionNames]}</h4>
                        <span className={`text-sm font-medium ${
                          score > 0.7 ? 'text-green-600' : 
                          score > 0.4 ? 'text-yellow-600' : 'text-red-600'
                        }`}>
                          {(score * 100).toFixed(0)}%
                        </span>
                      </div>
                      <div className="text-gray-700 text-sm whitespace-pre-wrap">
                        {text}
                      </div>
                    </div>
                  );
                })}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Key Themes & Growth Opportunities */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Key Themes */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-lg shadow-md p-6"
        >
          <h3 className="text-lg font-semibold mb-4 flex items-center space-x-2">
            <Heart className="w-5 h-5 text-pink-600" />
            <span>Key Themes</span>
          </h3>
          <div className="space-y-2">
            {narrative.key_themes?.map((theme: string, index: number) => (
              <div key={index} className="flex items-start space-x-2">
                <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                <span className="text-gray-700 text-sm">{theme}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Growth Opportunities */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-lg shadow-md p-6"
        >
          <h3 className="text-lg font-semibold mb-4 flex items-center space-x-2">
            <Lightbulb className="w-5 h-5 text-yellow-600" />
            <span>Growth Opportunities</span>
          </h3>
          <div className="space-y-2">
            {narrative.growth_opportunities?.map((opportunity: string, index: number) => (
              <div key={index} className="flex items-start space-x-2">
                <AlertCircle className="w-4 h-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                <span className="text-gray-700 text-sm">{opportunity}</span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Actionable Steps */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg shadow-lg overflow-hidden"
      >
        <button
          onClick={() => toggleSection('actions')}
          className="w-full px-6 py-4 flex items-center justify-between text-white hover:bg-white/10 transition-colors"
        >
          <div className="flex items-center space-x-3">
            <Target className="w-5 h-5" />
            <h3 className="text-lg font-semibold">Your Action Plan</h3>
          </div>
          {expandedSections.actions ? <ChevronUp /> : <ChevronDown />}
        </button>
        
        <AnimatePresence>
          {expandedSections.actions && (
            <motion.div
              initial={{ height: 0 }}
              animate={{ height: 'auto' }}
              exit={{ height: 0 }}
              className="overflow-hidden"
            >
              <div className="px-6 pb-4 pt-2">
                <p className="text-white/90 mb-4">
                  Specific steps to enhance your coherence:
                </p>
                <div className="space-y-3">
                  {narrative.actionable_steps?.map((step: string, index: number) => (
                    <div key={index} className="bg-white/20 rounded-lg p-3">
                      <div className="flex items-start space-x-3">
                        <div className="bg-white/30 rounded-full p-1 mt-0.5">
                          <CheckCircle className="w-4 h-4 text-white" />
                        </div>
                        <span className="text-white text-sm flex-1">{step}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}
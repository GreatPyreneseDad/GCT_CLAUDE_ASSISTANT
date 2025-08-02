import React from 'react';
import { motion } from 'framer-motion';

interface CoherenceIndicatorProps {
  score: number;
}

const CoherenceIndicator: React.FC<CoherenceIndicatorProps> = ({ score }) => {
  const getColor = () => {
    if (score > 2.5) return 'text-green-600';
    if (score > 1.5) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getLabel = () => {
    if (score > 2.5) return 'High Coherence';
    if (score > 1.5) return 'Moderate Coherence';
    return 'Developing Coherence';
  };

  return (
    <motion.div
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      className="flex items-center space-x-2 bg-white px-4 py-2 rounded-lg shadow-sm"
    >
      <div className={`text-2xl font-bold ${getColor()}`}>
        {score.toFixed(2)}
      </div>
      <div>
        <div className="text-xs text-gray-500">Coherence Score</div>
        <div className={`text-sm font-medium ${getColor()}`}>{getLabel()}</div>
      </div>
    </motion.div>
  );
};

export default CoherenceIndicator;
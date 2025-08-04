/**
 * Floating widget that displays real-time coherence metrics
 */

import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import { motion, AnimatePresence } from 'framer-motion';
import { Activity, TrendingUp, TrendingDown, Minus, X, ChevronDown, ChevronUp } from 'lucide-react';
import { AnalysisResult } from '../utils/coherence-analyzer';

interface WidgetProps {
  onClose?: () => void;
}

const CoherenceWidget: React.FC<WidgetProps> = ({ onClose }) => {
  const [isMinimized, setIsMinimized] = useState(false);
  const [currentAnalysis, setCurrentAnalysis] = useState<AnalysisResult | null>(null);
  const [history, setHistory] = useState<AnalysisResult[]>([]);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    // Listen for updates from content script
    const handleMessage = (event: MessageEvent) => {
      if (event.data.type === 'GCT_ANALYSIS_UPDATE') {
        setCurrentAnalysis(event.data.analysis);
        setHistory(prev => [...prev.slice(-19), event.data.analysis]);
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  const getScoreColor = (score: number): string => {
    if (score >= 0.8) return 'text-green-500';
    if (score >= 0.6) return 'text-yellow-500';
    if (score >= 0.4) return 'text-orange-500';
    return 'text-red-500';
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'improving':
        return <TrendingUp className="w-4 h-4 text-green-500" />;
      case 'declining':
        return <TrendingDown className="w-4 h-4 text-red-500" />;
      default:
        return <Minus className="w-4 h-4 text-gray-500" />;
    }
  };

  if (!currentAnalysis) return null;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      className="fixed bottom-4 right-4 z-[9999] font-sans"
      style={{ maxWidth: isMinimized ? '200px' : '320px' }}
    >
      <div className="bg-white rounded-lg shadow-2xl border border-gray-200 overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white p-3 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Activity className="w-5 h-5" />
            <span className="font-semibold text-sm">GCT Monitor</span>
          </div>
          <div className="flex items-center space-x-1">
            <button
              onClick={() => setIsMinimized(!isMinimized)}
              className="p-1 hover:bg-white/20 rounded transition-colors"
            >
              {isMinimized ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>
            {onClose && (
              <button
                onClick={onClose}
                className="p-1 hover:bg-white/20 rounded transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

        <AnimatePresence>
          {!isMinimized && (
            <motion.div
              initial={{ height: 0 }}
              animate={{ height: 'auto' }}
              exit={{ height: 0 }}
              transition={{ duration: 0.2 }}
            >
              {/* Main Metrics */}
              <div className="p-4 space-y-3">
                {/* Overall Score */}
                <div className="text-center">
                  <div className="text-3xl font-bold">
                    <span className={getScoreColor(currentAnalysis.metrics.overall)}>
                      {(currentAnalysis.metrics.overall * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="text-xs text-gray-500 flex items-center justify-center space-x-1 mt-1">
                    <span>Coherence</span>
                    {getTrendIcon(currentAnalysis.insights.trajectory)}
                  </div>
                </div>

                {/* Dimension Scores */}
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div className="bg-gray-50 rounded p-2">
                    <div className="text-xs text-gray-500">Consistency (Ψ)</div>
                    <div className={`font-semibold ${getScoreColor(currentAnalysis.metrics.psi)}`}>
                      {(currentAnalysis.metrics.psi * 100).toFixed(0)}%
                    </div>
                  </div>
                  <div className="bg-gray-50 rounded p-2">
                    <div className="text-xs text-gray-500">Wisdom (ρ)</div>
                    <div className={`font-semibold ${getScoreColor(currentAnalysis.metrics.rho)}`}>
                      {(currentAnalysis.metrics.rho * 100).toFixed(0)}%
                    </div>
                  </div>
                  <div className="bg-gray-50 rounded p-2">
                    <div className="text-xs text-gray-500">Action (q)</div>
                    <div className={`font-semibold ${getScoreColor(currentAnalysis.metrics.q)}`}>
                      {(currentAnalysis.metrics.q * 100).toFixed(0)}%
                    </div>
                  </div>
                  <div className="bg-gray-50 rounded p-2">
                    <div className="text-xs text-gray-500">Social (f)</div>
                    <div className={`font-semibold ${getScoreColor(currentAnalysis.metrics.f)}`}>
                      {(currentAnalysis.metrics.f * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>

                {/* Insights Toggle */}
                <button
                  onClick={() => setShowDetails(!showDetails)}
                  className="w-full text-sm text-indigo-600 hover:text-indigo-700 font-medium"
                >
                  {showDetails ? 'Hide Details' : 'Show Details'}
                </button>

                {/* Detailed Insights */}
                <AnimatePresence>
                  {showDetails && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="space-y-2 text-xs"
                    >
                      {currentAnalysis.insights.strengths.length > 0 && (
                        <div>
                          <div className="font-semibold text-green-600 mb-1">Strengths:</div>
                          <ul className="list-disc list-inside text-gray-600 space-y-0.5">
                            {currentAnalysis.insights.strengths.map((s, i) => (
                              <li key={i}>{s}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      {currentAnalysis.insights.concerns.length > 0 && (
                        <div>
                          <div className="font-semibold text-orange-600 mb-1">Areas to Improve:</div>
                          <ul className="list-disc list-inside text-gray-600 space-y-0.5">
                            {currentAnalysis.insights.concerns.map((c, i) => (
                              <li key={i}>{c}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Mini Chart */}
                <div className="h-12 flex items-end space-x-1">
                  {history.slice(-20).map((h, i) => (
                    <div
                      key={i}
                      className="flex-1 bg-indigo-500 rounded-t transition-all duration-300"
                      style={{
                        height: `${h.metrics.overall * 100}%`,
                        opacity: 0.3 + (i / 20) * 0.7
                      }}
                    />
                  ))}
                </div>
              </div>

              {/* Footer */}
              <div className="bg-gray-50 px-4 py-2 text-xs text-gray-500 text-center">
                Confidence: {(currentAnalysis.metrics.confidence * 100).toFixed(0)}%
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

export function createCoherenceWidget() {
  let root: ReactDOM.Root | null = null;
  let container: HTMLDivElement | null = null;

  return {
    inject() {
      // Create container
      container = document.createElement('div');
      container.id = 'gct-coherence-widget';
      document.body.appendChild(container);

      // Create shadow root for style isolation
      const shadow = container.attachShadow({ mode: 'open' });
      
      // Add styles
      const style = document.createElement('style');
      style.textContent = `
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * {
          font-family: 'Inter', sans-serif;
        }
        
        /* Add Tailwind CSS here or load it dynamically */
      `;
      shadow.appendChild(style);

      // Create React root
      const widgetContainer = document.createElement('div');
      shadow.appendChild(widgetContainer);
      
      root = ReactDOM.createRoot(widgetContainer);
      root.render(<CoherenceWidget />);
    },

    update(analysis: AnalysisResult) {
      // Send update to widget via postMessage
      window.postMessage({
        type: 'GCT_ANALYSIS_UPDATE',
        analysis
      }, '*');
    },

    show() {
      if (container) {
        container.style.display = 'block';
      }
    },

    hide() {
      if (container) {
        container.style.display = 'none';
      }
    },

    destroy() {
      if (root) {
        root.unmount();
      }
      if (container) {
        container.remove();
      }
    }
  };
}
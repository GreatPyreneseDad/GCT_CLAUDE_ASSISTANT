import React, { useState, useEffect } from 'react';
import { 
  Activity, Settings, TrendingUp, TrendingDown, 
  Minus, Globe, Power, BarChart3, Info
} from 'lucide-react';
import { motion } from 'framer-motion';
import browser from 'webextension-polyfill';

interface StoredAnalysis {
  metrics: {
    psi: number;
    rho: number;
    q: number;
    f: number;
    overall: number;
    confidence: number;
  };
  insights: {
    strengths: string[];
    concerns: string[];
    trajectory: 'improving' | 'stable' | 'declining';
  };
  timestamp: number;
  url: string;
  platform: string;
}

export default function Popup() {
  const [isEnabled, setIsEnabled] = useState(true);
  const [analyses, setAnalyses] = useState<StoredAnalysis[]>([]);
  const [activeTab, setActiveTab] = useState<'overview' | 'history' | 'settings'>('overview');
  const [currentPlatform, setCurrentPlatform] = useState<string>('');

  useEffect(() => {
    // Load settings
    browser.storage.sync.get(['enabled']).then(({ enabled }) => {
      setIsEnabled(enabled !== false);
    });

    // Load analyses
    browser.storage.local.get(['analyses']).then(({ analyses }) => {
      setAnalyses(analyses || []);
    });

    // Get current tab info
    browser.tabs.query({ active: true, currentWindow: true }).then(tabs => {
      if (tabs[0]?.url) {
        const url = new URL(tabs[0].url);
        if (url.hostname.includes('chat.openai.com')) setCurrentPlatform('ChatGPT');
        else if (url.hostname.includes('claude.ai')) setCurrentPlatform('Claude');
        else if (url.hostname.includes('bard.google.com')) setCurrentPlatform('Bard');
        else if (url.hostname.includes('gemini.google.com')) setCurrentPlatform('Gemini');
        else if (url.hostname.includes('poe.com')) setCurrentPlatform('Poe');
        else if (url.hostname.includes('perplexity.ai')) setCurrentPlatform('Perplexity');
      }
    });
  }, []);

  const toggleEnabled = async () => {
    const newState = !isEnabled;
    setIsEnabled(newState);
    await browser.storage.sync.set({ enabled: newState });
  };

  const getRecentAnalyses = () => {
    return analyses.slice(-10).reverse();
  };

  const getAverageScore = () => {
    if (analyses.length === 0) return 0;
    const sum = analyses.reduce((acc, a) => acc + a.metrics.overall, 0);
    return sum / analyses.length;
  };

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

  return (
    <div className="w-full h-full bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white p-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            <Activity className="w-6 h-6" />
            <h1 className="text-lg font-bold">GCT Coherence Monitor</h1>
          </div>
          <button
            onClick={toggleEnabled}
            className={`p-2 rounded-lg transition-colors ${
              isEnabled ? 'bg-white/20 hover:bg-white/30' : 'bg-red-500 hover:bg-red-600'
            }`}
          >
            <Power className="w-5 h-5" />
          </button>
        </div>
        
        {currentPlatform && (
          <div className="flex items-center space-x-2 text-sm bg-white/20 rounded-lg px-3 py-1.5">
            <Globe className="w-4 h-4" />
            <span>Monitoring {currentPlatform}</span>
          </div>
        )}
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200 bg-white">
        {(['overview', 'history', 'settings'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`flex-1 py-3 text-sm font-medium transition-colors ${
              activeTab === tab
                ? 'text-indigo-600 border-b-2 border-indigo-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="p-4">
        {activeTab === 'overview' && (
          <div className="space-y-4">
            {/* Status */}
            <div className="bg-white rounded-lg p-4 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">Status</span>
                <span className={`text-sm font-medium ${isEnabled ? 'text-green-600' : 'text-red-600'}`}>
                  {isEnabled ? 'Active' : 'Disabled'}
                </span>
              </div>
              <p className="text-xs text-gray-500">
                {isEnabled 
                  ? 'Monitoring LLM responses for coherence'
                  : 'Click the power button to enable monitoring'}
              </p>
            </div>

            {/* Average Score */}
            {analyses.length > 0 && (
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">Average Coherence</span>
                  <BarChart3 className="w-4 h-4 text-gray-400" />
                </div>
                <div className="text-2xl font-bold">
                  <span className={getScoreColor(getAverageScore())}>
                    {(getAverageScore() * 100).toFixed(0)}%
                  </span>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Based on {analyses.length} analyzed responses
                </p>
              </div>
            )}

            {/* Recent Analysis */}
            {analyses.length > 0 && (
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <h3 className="text-sm font-medium text-gray-700 mb-3">Latest Analysis</h3>
                {(() => {
                  const latest = analyses[analyses.length - 1];
                  return (
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-gray-500">Overall Score</span>
                        <span className={`font-semibold ${getScoreColor(latest.metrics.overall)}`}>
                          {(latest.metrics.overall * 100).toFixed(0)}%
                        </span>
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div className="flex justify-between">
                          <span className="text-gray-500">Consistency</span>
                          <span>{(latest.metrics.psi * 100).toFixed(0)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-500">Wisdom</span>
                          <span>{(latest.metrics.rho * 100).toFixed(0)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-500">Action</span>
                          <span>{(latest.metrics.q * 100).toFixed(0)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-500">Social</span>
                          <span>{(latest.metrics.f * 100).toFixed(0)}%</span>
                        </div>
                      </div>
                      <div className="flex items-center space-x-1 text-xs text-gray-500">
                        <span>Trend:</span>
                        {getTrendIcon(latest.insights.trajectory)}
                        <span className="capitalize">{latest.insights.trajectory}</span>
                      </div>
                    </div>
                  );
                })()}
              </div>
            )}

            {/* Info */}
            <div className="bg-blue-50 rounded-lg p-3 flex items-start space-x-2">
              <Info className="w-4 h-4 text-blue-600 mt-0.5" />
              <div className="text-xs text-blue-800">
                <p className="font-medium mb-1">How it works</p>
                <p>
                  This extension analyzes LLM responses using Grounded Coherence Theory (GCT) 
                  to evaluate consistency, wisdom integration, actionability, and social awareness.
                </p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'history' && (
          <div className="space-y-3">
            {getRecentAnalyses().length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <BarChart3 className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <p className="text-sm">No analyses yet</p>
                <p className="text-xs">Visit an LLM platform to start monitoring</p>
              </div>
            ) : (
              getRecentAnalyses().map((analysis, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="bg-white rounded-lg p-3 shadow-sm"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs text-gray-500">
                      {new Date(analysis.timestamp).toLocaleTimeString()}
                    </span>
                    <span className={`font-semibold text-sm ${getScoreColor(analysis.metrics.overall)}`}>
                      {(analysis.metrics.overall * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="text-xs text-gray-600">
                    {analysis.platform} • {new URL(analysis.url).hostname}
                  </div>
                </motion.div>
              ))
            )}
          </div>
        )}

        {activeTab === 'settings' && (
          <div className="space-y-4">
            <div className="bg-white rounded-lg p-4 shadow-sm">
              <h3 className="font-medium text-gray-700 mb-3">Monitoring Settings</h3>
              
              <label className="flex items-center justify-between cursor-pointer">
                <span className="text-sm text-gray-600">Enable monitoring</span>
                <input
                  type="checkbox"
                  checked={isEnabled}
                  onChange={toggleEnabled}
                  className="w-5 h-5 text-indigo-600 rounded focus:ring-indigo-500"
                />
              </label>
            </div>

            <div className="bg-white rounded-lg p-4 shadow-sm">
              <h3 className="font-medium text-gray-700 mb-3">Data</h3>
              <button
                onClick={async () => {
                  await browser.storage.local.clear();
                  setAnalyses([]);
                }}
                className="w-full py-2 px-4 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors text-sm"
              >
                Clear Analysis History
              </button>
            </div>

            <div className="bg-white rounded-lg p-4 shadow-sm">
              <h3 className="font-medium text-gray-700 mb-3">About</h3>
              <div className="space-y-2 text-xs text-gray-600">
                <p>Version: 1.0.0</p>
                <p>Powered by Grounded Coherence Theory (GCT)</p>
                <p>
                  <a href="#" className="text-indigo-600 hover:text-indigo-700">
                    Learn more about GCT
                  </a>
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
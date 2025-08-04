import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Slider } from '@/components/ui/slider';
import { Progress } from '@/components/ui/progress';
import { CheckCircle, Info, MessageSquare, SlidersHorizontal } from 'lucide-react';
import GCTApiClient from '@/lib/api-client';
import { CoherenceProfile } from '@/types';
import { EnhancedConversationalAssessment } from './EnhancedConversationalAssessment';
import { TestRunner } from './TestRunner';

interface AssessmentSectionProps {
  apiClient: GCTApiClient;
  userId: string;
  onProfileUpdate: (profile: CoherenceProfile) => void;
}

const AssessmentSection: React.FC<AssessmentSectionProps> = ({ 
  apiClient, 
  userId, 
  onProfileUpdate 
}) => {
  const [assessmentType, setAssessmentType] = useState<'tier1' | 'tier2' | 'conversational'>('conversational');
  const [isAssessing, setIsAssessing] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [responses, setResponses] = useState<Record<string, any>>({});
  const [age, setAge] = useState<number | undefined>();
  const [showAssessment, setShowAssessment] = useState(false);

  const tier1Questions = [
    {
      category: 'Internal Consistency (Ψ)',
      questions: [
        { key: 'values_action_alignment', text: 'Rate how well your daily actions align with your stated values', type: 'scale' },
        { key: 'cross_context_consistency', text: 'How similarly do you behave in professional vs. personal moral situations?', type: 'scale' },
        { key: 'belief_behavior_match', text: 'When you say you\'ll do something important, how often do you follow through?', type: 'scale' },
        { key: 'emotional_authenticity', text: 'How often do your emotional responses match your stated beliefs?', type: 'scale' }
      ]
    },
    {
      category: 'Accumulated Wisdom (ρ)',
      questions: [
        { key: 'learning_from_setbacks', text: 'How well do you learn from difficult experiences?', type: 'scale' },
        { key: 'pattern_recognition', text: 'How good are you at recognizing when past lessons apply to new situations?', type: 'scale' },
        { key: 'decision_improvement', text: 'How much better are your decisions now compared to 5 years ago?', type: 'scale' },
        { key: 'resilience_growth', text: 'How much stronger do challenges make you over time?', type: 'scale' }
      ]
    },
    {
      category: 'Moral Activation Energy (q)',
      questions: [
        { key: 'injustice_response', text: 'How strongly do you feel compelled to act when witnessing injustice?', type: 'scale' },
        { key: 'moral_action_willingness', text: 'How willing are you to take costly action for your principles?', type: 'scale' },
        { key: 'principle_consistency', text: 'How consistently do you act on your moral principles?', type: 'scale' },
        { key: 'costly_action_history', text: 'How often have you sacrificed personal gain for ethical reasons?', type: 'scale' }
      ]
    },
    {
      category: 'Social Belonging Architecture (f)',
      questions: [
        { key: 'relationship_quality', text: 'Rate the depth and quality of your closest relationships', type: 'scale' },
        { key: 'cultural_resonance', text: 'How well do you feel you belong in your cultural communities?', type: 'scale' },
        { key: 'social_support', text: 'How strong is your social support network?', type: 'scale' },
        { key: 'community_contribution', text: 'How much do you contribute to your communities?', type: 'scale' }
      ]
    }
  ];

  const currentQuestions = tier1Questions;
  const totalQuestions = currentQuestions.reduce((acc, cat) => acc + cat.questions.length, 0);
  const questionsAnswered = Object.keys(responses).length;
  const progress = (questionsAnswered / totalQuestions) * 100;

  const handleResponse = (key: string, value: any) => {
    setResponses(prev => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async () => {
    setIsAssessing(true);
    try {
      const profile = assessmentType === 'tier1' 
        ? await apiClient.submitTier1Assessment(userId, responses, age)
        : await apiClient.submitTier2Assessment(userId, responses, age);
      
      onProfileUpdate(profile);
      setIsAssessing(false);
      setCurrentStep(currentQuestions.length); // Show results
    } catch (error) {
      console.error('Assessment error:', error);
      setIsAssessing(false);
    }
  };

  const renderQuestion = (question: any) => {
    if (question.type === 'scale') {
      return (
        <div className="space-y-4">
          <label className="block text-sm font-medium text-gray-700">
            {question.text}
          </label>
          <div className="px-4">
            <Slider
              value={[responses[question.key] || 5]}
              onValueChange={(value) => handleResponse(question.key, value[0])}
              max={10}
              step={1}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-2">
              <span>0 - Never/Very Poor</span>
              <span>5 - Sometimes/Average</span>
              <span>10 - Always/Excellent</span>
            </div>
          </div>
        </div>
      );
    }
    return null;
  };

  if (currentStep >= currentQuestions.length) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-lg shadow-lg p-8"
      >
        <div className="text-center">
          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h3 className="text-2xl font-bold mb-2">Assessment Complete!</h3>
          <p className="text-gray-600">
            Your coherence profile has been generated. Check the Insights tab for detailed results.
          </p>
          <button
            onClick={() => {
              setCurrentStep(0);
              setResponses({});
            }}
            className="mt-6 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Take Another Assessment
          </button>
        </div>
      </motion.div>
    );
  }

  // Handle conversational assessment completion
  const handleConversationalComplete = async (profile: any) => {
    try {
      // Submit to backend
      const result = await apiClient.submitTier1Assessment(
        profile.user_id,
        profile.variables,
        age
      );
      onProfileUpdate(result);
      setShowAssessment(false);
    } catch (error) {
      console.error('Failed to submit conversational assessment:', error);
    }
  };

  // Show conversational assessment if selected and started
  if (showAssessment && assessmentType === 'conversational') {
    return (
      <div className="space-y-6">
        <EnhancedConversationalAssessment onComplete={handleConversationalComplete} />
      </div>
    );
  }

  // Show traditional assessment if selected and started
  if (showAssessment && (assessmentType === 'tier1' || assessmentType === 'tier2')) {
    // Traditional slider assessment logic here
    const currentQuestions = tier1Questions;
    const totalQuestions = currentQuestions.reduce((acc, cat) => acc + cat.questions.length, 0);
    const questionsAnswered = Object.keys(responses).length;
    const progress = (questionsAnswered / totalQuestions) * 100;

    return (
      <div className="space-y-6">
        {/* Your existing slider assessment UI */}
        {currentStep < currentQuestions.length && (
          <>
            {/* Progress Bar */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium">Progress</span>
                <span className="text-sm text-gray-500">{questionsAnswered} of {totalQuestions} questions</span>
              </div>
              <Progress value={progress} className="h-2 bg-gray-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-indigo-600 transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </Progress>
            </div>

            {/* Questions */}
            <motion.div
              key={currentStep}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white rounded-lg shadow-sm p-6"
            >
              <h3 className="text-lg font-semibold mb-6">{currentQuestions[currentStep].category}</h3>
              <div className="space-y-6">
                {currentQuestions[currentStep].questions.map((question) => (
                  <div key={question.key}>
                    {renderQuestion(question)}
                  </div>
                ))}
              </div>
              
              <div className="flex justify-between mt-8">
                <button
                  onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
                  disabled={currentStep === 0}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800 disabled:opacity-50"
                >
                  Previous
                </button>
                
                {currentStep === currentQuestions.length - 1 ? (
                  <button
                    onClick={handleSubmit}
                    disabled={questionsAnswered < totalQuestions || isAssessing}
                    className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors"
                  >
                    {isAssessing ? 'Processing...' : 'Submit Assessment'}
                  </button>
                ) : (
                  <button
                    onClick={() => setCurrentStep(currentStep + 1)}
                    className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                  >
                    Next
                  </button>
                )}
              </div>
            </motion.div>
          </>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Assessment Type Selection */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Choose Assessment Type</h3>
        <div className="grid grid-cols-3 gap-4">
          <button
            onClick={() => setAssessmentType('conversational')}
            className={`p-4 rounded-lg border-2 transition-all ${
              assessmentType === 'conversational' 
                ? 'border-indigo-600 bg-indigo-50' 
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <MessageSquare className="w-8 h-8 mx-auto mb-2 text-indigo-600" />
            <h4 className="font-semibold">AI Conversation</h4>
            <p className="text-sm text-gray-600 mt-1">Natural chat • 5-10 minutes</p>
            <p className="text-xs text-indigo-600 mt-1">✨ Recommended</p>
          </button>
          <button
            onClick={() => setAssessmentType('tier1')}
            className={`p-4 rounded-lg border-2 transition-all ${
              assessmentType === 'tier1' 
                ? 'border-indigo-600 bg-indigo-50' 
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <SlidersHorizontal className="w-8 h-8 mx-auto mb-2 text-gray-600" />
            <h4 className="font-semibold">Quick Sliders</h4>
            <p className="text-sm text-gray-600 mt-1">Traditional • 15-20 minutes</p>
          </button>
          <button
            onClick={() => setAssessmentType('tier2')}
            className={`p-4 rounded-lg border-2 transition-all ${
              assessmentType === 'tier2' 
                ? 'border-indigo-600 bg-indigo-50' 
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <h4 className="font-semibold">Tier 2: Professional</h4>
            <p className="text-sm text-gray-600 mt-1">45-60 minutes</p>
          </button>
        </div>
      </div>

      {/* Start Assessment Button */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <button
          onClick={() => setShowAssessment(true)}
          className="w-full py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-semibold"
        >
          Start {assessmentType === 'conversational' ? 'AI Conversation' : 'Assessment'}
        </button>
      </div>

      {/* Test Runner - Only show in development */}
      {process.env.NODE_ENV === 'development' && (
        <TestRunner onRunTest={(testResponses) => {
          // Automatically run the assessment with test data
          console.log('Running automated test with responses:', testResponses);
          // You can add logic here to automatically fill and submit the assessment
        }} />
      )}

      {/* Age Input */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Your Age (optional, for calibration)
        </label>
        <input
          type="number"
          value={age || ''}
          onChange={(e) => setAge(e.target.value ? parseInt(e.target.value) : undefined)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          placeholder="Enter your age"
        />
      </div>

      {/* Progress Bar */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium">Progress</span>
          <span className="text-sm text-gray-500">{questionsAnswered} of {totalQuestions} questions</span>
        </div>
        <Progress value={progress} className="h-2 bg-gray-200 rounded-full overflow-hidden">
          <div 
            className="h-full bg-indigo-600 transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </Progress>
      </div>

      {/* Questions */}
      <motion.div
        key={currentStep}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        className="bg-white rounded-lg shadow-sm p-6"
      >
        <h3 className="text-lg font-semibold mb-6">{currentQuestions[currentStep].category}</h3>
        <div className="space-y-6">
          {currentQuestions[currentStep].questions.map((question) => (
            <div key={question.key}>
              {renderQuestion(question)}
            </div>
          ))}
        </div>
        
        <div className="flex justify-between mt-8">
          <button
            onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
            disabled={currentStep === 0}
            className="px-4 py-2 text-gray-600 hover:text-gray-800 disabled:opacity-50"
          >
            Previous
          </button>
          
          {currentStep === currentQuestions.length - 1 ? (
            <button
              onClick={handleSubmit}
              disabled={questionsAnswered < totalQuestions || isAssessing}
              className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors"
            >
              {isAssessing ? 'Processing...' : 'Submit Assessment'}
            </button>
          ) : (
            <button
              onClick={() => setCurrentStep(currentStep + 1)}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Next
            </button>
          )}
        </div>
      </motion.div>

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-start space-x-3">
        <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
        <div className="text-sm text-blue-800">
          <p className="font-semibold mb-1">About Your Assessment</p>
          <p>
            Your responses help calculate your coherence profile across four key dimensions. 
            Be honest and reflective - there are no "right" answers, only authentic ones.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AssessmentSection;
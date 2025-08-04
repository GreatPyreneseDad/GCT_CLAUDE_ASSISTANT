import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, CheckCircle, XCircle, Loader } from 'lucide-react';
import { motion } from 'framer-motion';

interface TestRunnerProps {
  onRunTest: (responses: any) => void;
}

export function TestRunner({ onRunTest }: TestRunnerProps) {
  const [isRunning, setIsRunning] = useState(false);
  const [currentStep, setCurrentStep] = useState('');
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState<any>(null);

  // Test responses for automated testing
  const testResponses = {
    // PSI - Internal Consistency
    psi_1: {
      question: "Let's explore your internal consistency. Tell me about a recent decision where you had to choose between what was easy and what aligned with your values. What happened?",
      answer: "Last month I had to choose between accepting a lucrative contract that would require me to work with a company whose practices I disagree with, or staying true to my environmental values. I chose to decline the offer and instead took a smaller project with a sustainable startup. It was financially challenging but I sleep better at night.",
      type: "story"
    },
    psi_2: {
      question: "Thank you for sharing that. On a scale of 1-10, how satisfied were you with your choice?",
      answer: 7,
      type: "scale"
    },
    psi_3: {
      question: "I often find myself doing things that contradict what I say I believe in.",
      answer: false,
      type: "true_false"
    },
    psi_4: {
      question: "When I make promises to myself, I almost always keep them.",
      answer: true,
      type: "true_false"
    },
    psi_5: {
      question: "When your personal values conflict with what others expect of you, you typically:",
      answer: 1, // "Try to find a compromise that honors both"
      type: "choice"
    },
    psi_6: {
      question: "How often do your emotions align with your logical understanding of situations?",
      answer: 7,
      type: "scale"
    },
    psi_7: {
      question: "Rate how consistently you behave across different areas of your life (work, home, social):",
      answer: 6,
      type: "scale"
    },
    psi_8: {
      question: "Finally for this section, describe a time when you felt most authentic and true to yourself. What were the circumstances?",
      answer: "I felt most authentic when I gave a presentation about a cause I deeply care about - ocean conservation. I wasn't trying to impress anyone or meet expectations. I was just sharing my genuine passion and knowledge. The audience could feel my authenticity and it led to meaningful connections.",
      type: "story"
    },

    // RHO - Wisdom Integration
    rho_1: {
      question: "Now let's explore wisdom integration. Share a significant challenge or failure from your past. What did you learn, and how do you apply that lesson today?",
      answer: "My startup failed after 2 years due to poor financial planning. I learned the hard way that passion without practical skills isn't enough. Now I always ensure I have proper financial projections and advisors before starting any venture. This lesson has saved me from several potential mistakes.",
      type: "story"
    },
    rho_2: {
      question: "I often notice patterns in my life experiences that help me make better decisions.",
      answer: true,
      type: "true_false"
    },
    rho_3: {
      question: "When facing new challenges, how often do you consciously apply lessons from past experiences?",
      answer: 8,
      type: "scale"
    },
    rho_4: {
      question: "When someone disagrees with you, you typically:",
      answer: 0, // "Try to understand their perspective before responding"
      type: "choice"
    },
    rho_5: {
      question: "My abilities and wisdom are fixed traits that don't change much over time.",
      answer: false,
      type: "true_false"
    },
    rho_6: {
      question: "Tell me about a belief or assumption you've changed significantly over the years. What caused this shift?",
      answer: "I used to believe that working harder was always the answer to success. After experiencing burnout, I realized that working smarter and maintaining balance is far more sustainable. This shift came from seeing highly successful people who prioritized well-being alongside achievement.",
      type: "story"
    },
    rho_7: {
      question: "How well do you recognize when a current situation is similar to something you've experienced before?",
      answer: 7,
      type: "scale"
    },

    // Q - Moral Activation
    q_1: {
      question: "Let's talk about moral activation. Describe a recent situation where you witnessed something wrong or unjust. What did you do, and why?",
      answer: "I saw a colleague being unfairly criticized in a meeting for something that wasn't their fault. I spoke up and clarified the situation, even though it meant contradicting my supervisor. I couldn't stand by while someone was being scapegoated.",
      type: "story"
    },
    q_2: {
      question: "I often notice moral dimensions in everyday situations that others might overlook.",
      answer: true,
      type: "true_false"
    },
    q_3: {
      question: "When you see an opportunity to help or make a difference, how quickly do you act?",
      answer: 7,
      type: "scale"
    },
    q_4: {
      question: "You start a community project that faces unexpected resistance. You would most likely:",
      answer: 1, // "Modify your approach based on feedback"
      type: "choice"
    },
    q_5: {
      question: "I regularly think about how my actions (or inaction) affect others.",
      answer: true,
      type: "true_false"
    },
    q_6: {
      question: "Tell me about a time when doing the right thing came at a personal cost. How did you handle it?",
      answer: "I reported a safety violation at my workplace knowing it would strain my relationship with my team. It did create tension for weeks, but I handled it by being transparent about my reasons and continuing to support my colleagues in other ways. Eventually, they understood I was looking out for everyone's wellbeing.",
      type: "story"
    },
    q_7: {
      question: "How willing are you to stand up for your principles when it's unpopular or risky?",
      answer: 7,
      type: "scale"
    },

    // F - Social Belonging
    f_1: {
      question: "Finally, let's explore social belonging. Describe your closest relationships. What makes them meaningful to you?",
      answer: "My closest relationships are with my partner, two best friends from college, and my sister. What makes them meaningful is the mutual support, ability to be vulnerable, and shared growth. We celebrate each other's successes and provide comfort during struggles without judgment.",
      type: "story"
    },
    f_2: {
      question: "I have people in my life who truly understand and accept me for who I am.",
      answer: true,
      type: "true_false"
    },
    f_3: {
      question: "How connected do you feel to your broader community or social groups?",
      answer: 6,
      type: "scale"
    },
    f_4: {
      question: "In your relationships and communities, you tend to be:",
      answer: 1, // "Someone who maintains a good balance"
      type: "choice"
    },
    f_5: {
      question: "I often hide my true thoughts and feelings to maintain relationships.",
      answer: false,
      type: "true_false"
    },
    f_6: {
      question: "Tell me about a time when you felt a deep sense of belonging. What created that feeling?",
      answer: "At a volunteer event for environmental cleanup, I felt deep belonging when everyone shared their personal reasons for caring about the cause. The shared values and collaborative spirit created an instant bond. It wasn't just about the work, but about being with people who understood what mattered to me.",
      type: "story"
    },
    f_7: {
      question: "If you faced a major life crisis tomorrow, how many people could you turn to for genuine support?",
      answer: 2, // "3-5 people"
      type: "choice"
    },
    f_8: {
      question: "How often do you feel lonely or isolated, even when around others?",
      answer: 3,
      type: "scale"
    }
  };

  const runAutomatedTest = async () => {
    setIsRunning(true);
    setProgress(0);
    setResults(null);

    try {
      // Simulate processing time
      setCurrentStep('Preparing test responses...');
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setCurrentStep('Formatting responses for assessment...');
      setProgress(20);
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setCurrentStep('Submitting to assessment system...');
      setProgress(40);
      
      // Call the parent's onRunTest with our test responses
      onRunTest(testResponses);
      
      setCurrentStep('Processing responses...');
      setProgress(60);
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setCurrentStep('Generating insights...');
      setProgress(80);
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setCurrentStep('Test completed successfully!');
      setProgress(100);
      
      setResults({
        success: true,
        timestamp: new Date().toISOString(),
        responseCount: Object.keys(testResponses).length,
        dimensions: ['psi', 'rho', 'q', 'f']
      });
      
    } catch (error) {
      setCurrentStep('Test failed');
      setResults({
        success: false,
        error: error.message
      });
    } finally {
      setIsRunning(false);
    }
  };

  const resetTest = () => {
    setCurrentStep('');
    setProgress(0);
    setResults(null);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg shadow-md p-6"
    >
      <h3 className="text-lg font-semibold mb-4 flex items-center space-x-2">
        <Play className="w-5 h-5 text-indigo-600" />
        <span>Automated Test Runner</span>
      </h3>
      
      <p className="text-gray-600 mb-6">
        Run an automated test of the assessment system with pre-configured responses
        representing a moderately coherent individual.
      </p>

      <div className="space-y-4">
        {/* Control Buttons */}
        <div className="flex space-x-3">
          <button
            onClick={runAutomatedTest}
            disabled={isRunning}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
              isRunning 
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
                : 'bg-indigo-600 text-white hover:bg-indigo-700'
            }`}
          >
            {isRunning ? (
              <>
                <Loader className="w-4 h-4 animate-spin" />
                <span>Running Test...</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                <span>Run Test</span>
              </>
            )}
          </button>
          
          <button
            onClick={resetTest}
            disabled={isRunning}
            className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Reset</span>
          </button>
        </div>

        {/* Progress Bar */}
        {(isRunning || progress > 0) && (
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">{currentStep}</span>
              <span className="text-gray-500">{progress}%</span>
            </div>
            <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
              <motion.div 
                className="h-full bg-indigo-600"
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
          </div>
        )}

        {/* Results */}
        {results && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`p-4 rounded-lg ${
              results.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
            }`}
          >
            <div className="flex items-start space-x-3">
              {results.success ? (
                <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
              ) : (
                <XCircle className="w-5 h-5 text-red-600 mt-0.5" />
              )}
              <div className="flex-1">
                <h4 className="font-semibold text-gray-900">
                  {results.success ? 'Test Completed Successfully' : 'Test Failed'}
                </h4>
                {results.success ? (
                  <div className="text-sm text-gray-600 mt-1">
                    <p>✓ Submitted {results.responseCount} responses</p>
                    <p>✓ Covered all {results.dimensions.length} dimensions</p>
                    <p>✓ Assessment ready for review</p>
                  </div>
                ) : (
                  <p className="text-sm text-red-600 mt-1">{results.error}</p>
                )}
              </div>
            </div>
          </motion.div>
        )}

        {/* Test Details */}
        <details className="text-sm text-gray-600">
          <summary className="cursor-pointer hover:text-gray-800">
            Test Response Details
          </summary>
          <div className="mt-2 p-3 bg-gray-50 rounded-lg">
            <p className="mb-2">This test simulates a moderately coherent individual with:</p>
            <ul className="list-disc list-inside space-y-1">
              <li>Good value-action alignment (Ψ ~70%)</li>
              <li>Strong wisdom integration (ρ ~75%)</li>
              <li>Moderate moral activation (q ~65%)</li>
              <li>Decent social connections (f ~60%)</li>
            </ul>
            <p className="mt-2">Expected overall coherence: ~2.3-2.5/4.0</p>
          </div>
        </details>
      </div>
    </motion.div>
  );
}
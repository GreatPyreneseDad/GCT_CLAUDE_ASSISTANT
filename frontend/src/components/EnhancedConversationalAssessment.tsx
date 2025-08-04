import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, Send, Sparkles, RefreshCw, CheckCircle, Circle, AlertCircle } from 'lucide-react';
import { apiClient } from '../lib/api-client';
import { motion, AnimatePresence } from 'framer-motion';
import { ComprehensiveFeedback } from './ComprehensiveFeedback';

interface Message {
  id: string;
  role: 'assistant' | 'user';
  content: string;
  timestamp: Date;
  questionType?: 'story' | 'true_false' | 'scale' | 'choice';
  questionId?: string;
  options?: string[];
  scaleLabels?: [string, string];
}

interface AssessmentProgress {
  psi: { total: number; answered: number };
  rho: { total: number; answered: number };
  q: { total: number; answered: number };
  f: { total: number; answered: number };
}

interface EnhancedConversationalAssessmentProps {
  onComplete: (profile: any) => void;
  userId?: string;
}

export function EnhancedConversationalAssessment({ onComplete, userId }: EnhancedConversationalAssessmentProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [currentDimension, setCurrentDimension] = useState<'intro' | 'psi' | 'rho' | 'q' | 'f' | 'complete'>('intro');
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [responses, setResponses] = useState<Record<string, any>>({});
  const [progress, setProgress] = useState<AssessmentProgress>({
    psi: { total: 8, answered: 0 },
    rho: { total: 7, answered: 0 },
    q: { total: 7, answered: 0 },
    f: { total: 8, answered: 0 }
  });
  const [showQuickResponse, setShowQuickResponse] = useState<{
    type: string;
    options?: string[];
    scaleLabels?: [string, string];
  } | null>(null);
  const [selectedScale, setSelectedScale] = useState<number>(5);
  const [completedProfile, setCompletedProfile] = useState<any>(null);
  const [completedInsights, setCompletedInsights] = useState<any>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Start the conversation
    addAssistantMessage(
      "✨ Welcome! I'm here to help you discover your coherence profile through a comprehensive conversation. " +
      "This assessment will explore four key dimensions of your life:\n\n" +
      "• **Internal Consistency** - How aligned are your actions with your values?\n" +
      "• **Wisdom Integration** - How well do you learn from experiences?\n" +
      "• **Moral Activation** - How readily do you act on your principles?\n" +
      "• **Social Belonging** - How connected are you to others?\n\n" +
      "I'll ask various types of questions - some will be open-ended, others true/false or rating scales. " +
      "Ready to begin?"
    );
  }, []);

  const addAssistantMessage = (content: string, questionType?: string, options?: any) => {
    const message: Message = {
      id: Date.now().toString(),
      role: 'assistant',
      content,
      timestamp: new Date(),
      questionType: questionType as any,
      options: options?.options,
      scaleLabels: options?.scaleLabels
    };
    setMessages(prev => [...prev, message]);
    
    // Show quick response options if applicable
    if (questionType && questionType !== 'story') {
      setShowQuickResponse({
        type: questionType,
        options: options?.options,
        scaleLabels: options?.scaleLabels
      });
    } else {
      setShowQuickResponse(null);
    }
  };

  const addUserMessage = (content: string) => {
    const message: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, message]);
    setShowQuickResponse(null);
  };

  // Question sequences for each dimension
  const questionSequences = {
    psi: [
      {
        id: 'psi_1',
        text: "Let's explore your internal consistency. Tell me about a recent decision where you had to choose between what was easy and what aligned with your values. What happened?",
        type: 'story'
      },
      {
        id: 'psi_2',
        text: "Thank you for sharing that. On a scale of 1-10, how satisfied were you with your choice?",
        type: 'scale',
        scaleLabels: ['Very dissatisfied', 'Very satisfied']
      },
      {
        id: 'psi_3',
        text: "I often find myself doing things that contradict what I say I believe in.",
        type: 'true_false'
      },
      {
        id: 'psi_4',
        text: "When I make promises to myself, I almost always keep them.",
        type: 'true_false'
      },
      {
        id: 'psi_5',
        text: "When your personal values conflict with what others expect of you, you typically:",
        type: 'choice',
        options: [
          "Always follow your values, regardless of consequences",
          "Try to find a compromise that honors both",
          "Go along with others to avoid conflict",
          "It depends entirely on the situation"
        ]
      },
      {
        id: 'psi_6',
        text: "How often do your emotions align with your logical understanding of situations?",
        type: 'scale',
        scaleLabels: ['Never', 'Always']
      },
      {
        id: 'psi_7',
        text: "Rate how consistently you behave across different areas of your life (work, home, social):",
        type: 'scale',
        scaleLabels: ['Very inconsistent', 'Very consistent']
      },
      {
        id: 'psi_8',
        text: "Finally for this section, describe a time when you felt most authentic and true to yourself. What were the circumstances?",
        type: 'story'
      }
    ],
    rho: [
      {
        id: 'rho_1',
        text: "Now let's explore wisdom integration. Share a significant challenge or failure from your past. What did you learn, and how do you apply that lesson today?",
        type: 'story'
      },
      {
        id: 'rho_2',
        text: "I often notice patterns in my life experiences that help me make better decisions.",
        type: 'true_false'
      },
      {
        id: 'rho_3',
        text: "When facing new challenges, how often do you consciously apply lessons from past experiences?",
        type: 'scale',
        scaleLabels: ['Never', 'Always']
      },
      {
        id: 'rho_4',
        text: "When someone disagrees with you, you typically:",
        type: 'choice',
        options: [
          "Try to understand their perspective before responding",
          "Defend your position while listening to theirs",
          "Agree to disagree without exploring further",
          "Try to convince them you're right"
        ]
      },
      {
        id: 'rho_5',
        text: "My abilities and wisdom are fixed traits that don't change much over time.",
        type: 'true_false'
      },
      {
        id: 'rho_6',
        text: "Tell me about a belief or assumption you've changed significantly over the years. What caused this shift?",
        type: 'story'
      },
      {
        id: 'rho_7',
        text: "How well do you recognize when a current situation is similar to something you've experienced before?",
        type: 'scale',
        scaleLabels: ['Very poorly', 'Very well']
      }
    ],
    q: [
      {
        id: 'q_1',
        text: "Let's talk about moral activation. Describe a recent situation where you witnessed something wrong or unjust. What did you do, and why?",
        type: 'story'
      },
      {
        id: 'q_2',
        text: "I often notice moral dimensions in everyday situations that others might overlook.",
        type: 'true_false'
      },
      {
        id: 'q_3',
        text: "When you see an opportunity to help or make a difference, how quickly do you act?",
        type: 'scale',
        scaleLabels: ['Very slowly/Never', 'Immediately']
      },
      {
        id: 'q_4',
        text: "You start a community project that faces unexpected resistance. You would most likely:",
        type: 'choice',
        options: [
          "Push through despite the obstacles",
          "Modify your approach based on feedback",
          "Hand it off to someone else",
          "Abandon it and try something different"
        ]
      },
      {
        id: 'q_5',
        text: "I regularly think about how my actions (or inaction) affect others.",
        type: 'true_false'
      },
      {
        id: 'q_6',
        text: "Tell me about a time when doing the right thing came at a personal cost. How did you handle it?",
        type: 'story'
      },
      {
        id: 'q_7',
        text: "How willing are you to stand up for your principles when it's unpopular or risky?",
        type: 'scale',
        scaleLabels: ['Not at all willing', 'Completely willing']
      }
    ],
    f: [
      {
        id: 'f_1',
        text: "Finally, let's explore social belonging. Describe your closest relationships. What makes them meaningful to you?",
        type: 'story'
      },
      {
        id: 'f_2',
        text: "I have people in my life who truly understand and accept me for who I am.",
        type: 'true_false'
      },
      {
        id: 'f_3',
        text: "How connected do you feel to your broader community or social groups?",
        type: 'scale',
        scaleLabels: ['Completely disconnected', 'Deeply connected']
      },
      {
        id: 'f_4',
        text: "In your relationships and communities, you tend to be:",
        type: 'choice',
        options: [
          "Someone who gives more than they receive",
          "Someone who maintains a good balance",
          "Someone who receives more than they give",
          "Someone who keeps interactions minimal"
        ]
      },
      {
        id: 'f_5',
        text: "I often hide my true thoughts and feelings to maintain relationships.",
        type: 'true_false'
      },
      {
        id: 'f_6',
        text: "Tell me about a time when you felt a deep sense of belonging. What created that feeling?",
        type: 'story'
      },
      {
        id: 'f_7',
        text: "If you faced a major life crisis tomorrow, how many people could you turn to for genuine support?",
        type: 'choice',
        options: [
          "None",
          "1-2 people",
          "3-5 people",
          "More than 5 people"
        ]
      },
      {
        id: 'f_8',
        text: "How often do you feel lonely or isolated, even when around others?",
        type: 'scale',
        scaleLabels: ['Never', 'Always']
      }
    ]
  };

  const getCurrentQuestion = () => {
    if (currentDimension === 'intro' || currentDimension === 'complete') return null;
    const questions = questionSequences[currentDimension];
    return questions[currentQuestionIndex] || null;
  };

  const handleResponse = async (response: any, questionType: string) => {
    const currentQuestion = getCurrentQuestion();
    if (!currentQuestion) return;

    // Store the response
    setResponses(prev => ({
      ...prev,
      [currentQuestion.id]: response
    }));

    // Update progress
    setProgress(prev => ({
      ...prev,
      [currentDimension]: {
        ...prev[currentDimension as keyof AssessmentProgress],
        answered: prev[currentDimension as keyof AssessmentProgress].answered + 1
      }
    }));

    // Move to next question or dimension
    const questions = questionSequences[currentDimension as keyof typeof questionSequences];
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      const nextQuestion = questions[currentQuestionIndex + 1];
      setTimeout(() => {
        addAssistantMessage(
          nextQuestion.text,
          nextQuestion.type,
          { options: nextQuestion.options, scaleLabels: nextQuestion.scaleLabels }
        );
      }, 1000);
    } else {
      // Move to next dimension
      moveToNextDimension();
    }
  };

  const moveToNextDimension = () => {
    let nextDimension: typeof currentDimension = 'complete';
    
    switch (currentDimension) {
      case 'intro':
        nextDimension = 'psi';
        break;
      case 'psi':
        nextDimension = 'rho';
        addAssistantMessage("Excellent work on exploring your internal consistency. Let's move on to wisdom integration.");
        break;
      case 'rho':
        nextDimension = 'q';
        addAssistantMessage("Great insights on how you learn and grow. Now let's explore moral activation.");
        break;
      case 'q':
        nextDimension = 'f';
        addAssistantMessage("Thank you for sharing about your actions and principles. Finally, let's discuss social belonging.");
        break;
      case 'f':
        nextDimension = 'complete';
        break;
    }

    setCurrentDimension(nextDimension);
    setCurrentQuestionIndex(0);

    if (nextDimension === 'complete') {
      completeAssessment();
    } else if (nextDimension !== 'complete') {
      const questions = questionSequences[nextDimension as keyof typeof questionSequences];
      setTimeout(() => {
        addAssistantMessage(
          questions[0].text,
          questions[0].type,
          { options: questions[0].options, scaleLabels: questions[0].scaleLabels }
        );
      }, 2000);
    }
  };

  const completeAssessment = async () => {
    setIsTyping(true);
    
    try {
      // Format responses for LLM analysis
      const formattedResponses: Record<string, any> = {};
      
      // Collect all questions from all dimensions
      Object.entries(responses).forEach(([questionId, answer]) => {
        // Find the question across all dimensions
        let question: any = null;
        for (const dim of ['psi', 'rho', 'q', 'f'] as const) {
          const found = questionSequences[dim].find(q => q.id === questionId);
          if (found) {
            question = found;
            break;
          }
        }
        
        if (question) {
          formattedResponses[questionId] = {
            question: question.text,
            answer: answer,
            type: question.type
          };
        }
      });
      
      // Submit to LLM assessment endpoint
      const response = await apiClient.post('/api/enhanced/assessment/complete/llm', {
        responses: formattedResponses,
        user_id: userId || 'enhanced_conversational_user'
      });

      if (response.data.success) {
        const profile = response.data.profile;
        const insights = response.data.insights;
        
        console.log('Assessment completed successfully:', { profile, insights });
        
        // Store for comprehensive feedback display
        setCompletedProfile(profile);
        setCompletedInsights(insights);
        
        // Check if we have narrative feedback
        const hasNarrative = insights.narrative_feedback && Object.keys(insights.narrative_feedback).length > 0;
        
        addAssistantMessage(
          `🎉 Congratulations on completing the comprehensive assessment!\n\n` +
          `I've analyzed your responses in detail and prepared personalized feedback about your coherence profile.\n\n` +
          `Your overall coherence score is ${profile.static_coherence.toFixed(2)}/4.0` +
          (hasNarrative ? `, placing you in the "${insights.narrative_feedback.coherence_state}" category.` : `.`) +
          `\n\n${hasNarrative ? 'Scroll down to see your comprehensive feedback report.' : 'Your detailed analysis is below.'}`
        );

        setTimeout(() => {
          onComplete(profile);
        }, 1000);
      } else {
        console.error('Assessment failed:', response.data);
        addAssistantMessage("I encountered an error processing your assessment. The analysis may be incomplete.");
      }
    } catch (error) {
      console.error('Assessment completion error:', error);
      addAssistantMessage("I encountered an error processing your assessment. Please try again.");
    } finally {
      setIsTyping(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isTyping) return;

    const userInput = input;
    setInput('');
    addUserMessage(userInput);

    const currentQuestion = getCurrentQuestion();
    
    if (currentDimension === 'intro') {
      // Start assessment after intro
      setCurrentDimension('psi');
      const firstQuestion = questionSequences.psi[0];
      setTimeout(() => {
        addAssistantMessage(
          firstQuestion.text,
          firstQuestion.type,
          { options: firstQuestion.options, scaleLabels: firstQuestion.scaleLabels }
        );
      }, 1000);
    } else if (currentQuestion && currentQuestion.type === 'story') {
      // Handle story response
      handleResponse(userInput, 'story');
    }
  };

  const handleQuickResponse = (response: any) => {
    const currentQuestion = getCurrentQuestion();
    if (!currentQuestion) return;

    // Format response for display
    let displayResponse = '';
    switch (currentQuestion.type) {
      case 'true_false':
        displayResponse = response ? 'True' : 'False';
        break;
      case 'scale':
        displayResponse = `${response}/10`;
        break;
      case 'choice':
        displayResponse = currentQuestion.options?.[response] || response;
        break;
      default:
        displayResponse = response.toString();
    }

    addUserMessage(displayResponse);
    handleResponse(response, currentQuestion.type);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
    <div className="flex flex-col bg-white rounded-lg shadow-sm">
      {/* Header with Progress */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-4 rounded-t-lg">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            <Sparkles className="w-5 h-5" />
            <h3 className="font-semibold">Comprehensive Coherence Assessment</h3>
          </div>
          <button
            onClick={() => window.location.reload()}
            className="p-2 hover:bg-white/20 rounded-lg transition-colors"
            title="Start over"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
        
        {/* Progress indicators */}
        {currentDimension !== 'intro' && currentDimension !== 'complete' && (
          <div className="grid grid-cols-4 gap-2">
            {(['psi', 'rho', 'q', 'f'] as const).map((dim) => {
              const dimProgress = progress[dim];
              const isActive = currentDimension === dim;
              const isComplete = dimProgress.answered === dimProgress.total;
              const percentComplete = (dimProgress.answered / dimProgress.total) * 100;
              
              return (
                <div key={dim} className="text-center">
                  <div className="text-xs mb-1 opacity-80">
                    {dim === 'psi' ? 'Consistency' :
                     dim === 'rho' ? 'Wisdom' :
                     dim === 'q' ? 'Action' : 'Belonging'}
                  </div>
                  <div className="relative h-2 bg-white/20 rounded-full overflow-hidden">
                    <motion.div
                      className={`h-full ${isActive ? 'bg-white' : 'bg-white/50'}`}
                      initial={{ width: 0 }}
                      animate={{ width: `${percentComplete}%` }}
                      transition={{ duration: 0.5 }}
                    />
                  </div>
                  <div className="text-xs mt-1">
                    {dimProgress.answered}/{dimProgress.total}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Messages */}
      <div className="overflow-y-auto p-4 space-y-4 min-h-[400px] max-h-[600px]">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-4 ${
                message.role === 'user'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              <p className={`whitespace-pre-wrap ${
                message.role === 'user' ? 'text-white' : 'text-gray-800'
              } text-base leading-relaxed`}>{message.content}</p>
              <p className={`text-xs mt-2 ${
                message.role === 'user' ? 'text-white/70' : 'text-gray-500'
              }`}>
                {message.timestamp.toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg p-3">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Response Options */}
      <AnimatePresence>
        {showQuickResponse && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="border-t p-4 bg-gray-50"
          >
            {showQuickResponse.type === 'true_false' && (
              <div className="flex justify-center space-x-4">
                <button
                  onClick={() => handleQuickResponse(true)}
                  className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  <CheckCircle className="w-4 h-4 inline mr-2" />
                  True
                </button>
                <button
                  onClick={() => handleQuickResponse(false)}
                  className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                >
                  <Circle className="w-4 h-4 inline mr-2" />
                  False
                </button>
              </div>
            )}
            
            {showQuickResponse.type === 'scale' && (
              <div className="space-y-2">
                <div className="flex justify-between text-sm text-gray-600">
                  <span>{showQuickResponse.scaleLabels?.[0]}</span>
                  <span className="font-semibold">{selectedScale}/10</span>
                  <span>{showQuickResponse.scaleLabels?.[1]}</span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={selectedScale}
                  onChange={(e) => setSelectedScale(parseInt(e.target.value))}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
                <button
                  onClick={() => handleQuickResponse(selectedScale)}
                  className="w-full mt-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                >
                  Submit: {selectedScale}/10
                </button>
              </div>
            )}
            
            {showQuickResponse.type === 'choice' && (
              <div className="space-y-2">
                {showQuickResponse.options?.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuickResponse(index)}
                    className="w-full text-left px-4 py-3 bg-white border-2 border-gray-300 rounded-lg hover:border-indigo-600 hover:bg-indigo-50 transition-colors"
                  >
                    <span className="text-gray-800 font-medium block">
                      {String.fromCharCode(65 + index)}. {option}
                    </span>
                  </button>
                ))}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Input */}
      {currentDimension !== 'complete' && !showQuickResponse && (
        <div className="border-t p-4">
          <div className="flex space-x-2">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={
                currentDimension === 'intro'
                  ? "Type 'yes' or ask any questions to begin..."
                  : "Share your thoughts..."
              }
              className="flex-1 px-4 py-3 text-gray-800 text-base border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
              rows={3}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || isTyping}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}
      
    </div>
      
      {/* Comprehensive Feedback Display - Outside the main container */}
      {currentDimension === 'complete' && completedProfile && completedInsights && (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mt-8"
        >
          <ComprehensiveFeedback 
            profile={completedProfile} 
            insights={completedInsights} 
          />
        </motion.div>
      )}
    </>
  );
}
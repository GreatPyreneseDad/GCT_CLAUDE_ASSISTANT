import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, Send, Sparkles, RefreshCw } from 'lucide-react';
import { apiClient } from '../lib/api-client';

interface Message {
  id: string;
  role: 'assistant' | 'user';
  content: string;
  timestamp: Date;
  coherenceData?: {
    psi?: number;
    rho?: number;
    q?: number;
    f?: number;
  };
}

interface ConversationalAssessmentProps {
  onComplete: (profile: any) => void;
}

export function ConversationalAssessment({ onComplete }: ConversationalAssessmentProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [currentPhase, setCurrentPhase] = useState<'intro' | 'psi' | 'rho' | 'q' | 'f' | 'complete'>('intro');
  const [coherenceScores, setCoherenceScores] = useState({
    psi: 0,
    rho: 0,
    q: 0,
    f: 0
  });
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
      "✨ Hi! I'm your Coherence Guide. I'll help you discover your coherence profile through a natural conversation. " +
      "This will take about 5-10 minutes. Ready to begin?"
    );
  }, []);

  const addAssistantMessage = (content: string, coherenceData?: any) => {
    const message: Message = {
      id: Date.now().toString(),
      role: 'assistant',
      content,
      timestamp: new Date(),
      coherenceData
    };
    setMessages(prev => [...prev, message]);
  };

  const addUserMessage = (content: string) => {
    const message: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, message]);
  };

  const getNextQuestion = () => {
    switch (currentPhase) {
      case 'intro':
        return "Let's start with understanding your inner alignment. Tell me about a recent decision you made - how did it feel in relation to your values?";
      
      case 'psi':
        return "That's insightful. Now, when you face challenges, how do you typically learn from them? Can you share a recent example where you grew from a difficult experience?";
      
      case 'rho':
        return "I appreciate your openness. Let's talk about action - when you see something that needs to be done (whether at work, home, or in your community), how do you decide whether to step up?";
      
      case 'q':
        return "Great perspective! Finally, tell me about your connections with others. How would you describe the quality of your relationships and your sense of belonging?";
      
      case 'f':
        return "Thank you for sharing all of that. Based on our conversation, I'm calculating your coherence profile...";
      
      default:
        return "";
    }
  };

  const analyzeResponse = async (userResponse: string, phase: string) => {
    // Send to backend for AI analysis
    try {
      const response = await apiClient.post('/enhanced/conversational/analyze', {
        text: userResponse,
        phase: phase,
        user_id: 'conversational_user'
      });

      if (response.data.success) {
        const score = response.data.score[phase] || 0.5;
        const followUp = response.data.follow_up;
        
        // Store the follow-up for next question
        if (followUp) {
          // We'll use this instead of the generic next question
          return { score, followUp };
        }
        
        return { score, followUp: null };
      }
      
      // Fallback to basic analysis
      return { score: 0.5, followUp: null };
    } catch (error) {
      console.error('Analysis error:', error);
      // Fallback to basic analysis
      return { score: 0.5, followUp: null };
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isTyping) return;

    const userInput = input;
    setInput('');
    addUserMessage(userInput);
    setIsTyping(true);

    // Simulate AI thinking
    setTimeout(async () => {
      let nextPhase = currentPhase;
      let score = 0;

      // Analyze the response based on current phase
      let customFollowUp = null;
      if (currentPhase !== 'intro' && currentPhase !== 'complete') {
        const analysis = await analyzeResponse(userInput, currentPhase);
        score = analysis.score;
        customFollowUp = analysis.followUp;
        
        // Update coherence scores
        setCoherenceScores(prev => ({
          ...prev,
          [currentPhase]: score
        }));
      }

      // Progress to next phase
      switch (currentPhase) {
        case 'intro':
          nextPhase = 'psi';
          break;
        case 'psi':
          nextPhase = 'rho';
          break;
        case 'rho':
          nextPhase = 'q';
          break;
        case 'q':
          nextPhase = 'f';
          break;
        case 'f':
          nextPhase = 'complete';
          break;
      }

      setCurrentPhase(nextPhase);

      if (nextPhase === 'complete') {
        // Calculate final coherence
        const finalScores = {
          ...coherenceScores,
          f: score
        };
        
        const overallCoherence = 
          finalScores.psi + 
          (finalScores.rho * finalScores.psi) + 
          finalScores.q + 
          (finalScores.f * finalScores.psi);

        addAssistantMessage(
          `🎉 Your coherence profile is complete!\n\n` +
          `Overall Coherence: ${overallCoherence.toFixed(2)}/4.0\n\n` +
          `• Internal Consistency (Ψ): ${(finalScores.psi * 100).toFixed(0)}%\n` +
          `• Wisdom Integration (ρ): ${(finalScores.rho * 100).toFixed(0)}%\n` +
          `• Moral Activation (q): ${(finalScores.q * 100).toFixed(0)}%\n` +
          `• Social Belonging (f): ${(finalScores.f * 100).toFixed(0)}%\n\n` +
          `I'll save this profile and provide personalized insights.`,
          finalScores
        );

        // Submit the assessment
        setTimeout(() => {
          onComplete({
            user_id: 'conversational_user',
            variables: finalScores,
            static_coherence: overallCoherence,
            assessment_type: 'conversational'
          });
        }, 2000);
      } else {
        // Ask next question
        const nextQuestion = getNextQuestion();
        
        // Use custom follow-up from AI analysis or default question
        const questionToAsk = customFollowUp || nextQuestion;
        
        // Add contextual feedback based on previous answer
        let feedback = "";
        if (currentPhase !== 'intro' && !customFollowUp) {
          if (score > 0.7) {
            feedback = "That shows strong alignment. ";
          } else if (score > 0.4) {
            feedback = "I hear both strengths and areas for growth. ";
          } else {
            feedback = "Thank you for your honesty. ";
          }
        }

        addAssistantMessage(customFollowUp ? questionToAsk : feedback + questionToAsk);
      }

      setIsTyping(false);
    }, 1500);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const resetConversation = () => {
    setMessages([]);
    setCurrentPhase('intro');
    setCoherenceScores({ psi: 0, rho: 0, q: 0, f: 0 });
    addAssistantMessage(
      "✨ Hi! I'm your Coherence Guide. I'll help you discover your coherence profile through a natural conversation. " +
      "This will take about 5-10 minutes. Ready to begin?"
    );
  };

  return (
    <div className="flex flex-col h-[600px] bg-white rounded-lg shadow-sm">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-4 rounded-t-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Sparkles className="w-5 h-5" />
            <h3 className="font-semibold">AI Coherence Assessment</h3>
          </div>
          <button
            onClick={resetConversation}
            className="p-2 hover:bg-white/20 rounded-lg transition-colors"
            title="Start over"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
        <p className="text-sm text-white/80 mt-1">
          Discovering your coherence through conversation
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                message.role === 'user'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              <p className="whitespace-pre-wrap">{message.content}</p>
              <p className="text-xs mt-1 opacity-70">
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

      {/* Input */}
      <div className="border-t p-4">
        <div className="flex space-x-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Share your thoughts..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
            rows={2}
            disabled={currentPhase === 'complete'}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isTyping || currentPhase === 'complete'}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
        
        {/* Progress indicator */}
        <div className="mt-3 flex items-center justify-between text-xs text-gray-500">
          <span>
            Phase: {currentPhase === 'psi' ? 'Internal Consistency' :
                   currentPhase === 'rho' ? 'Wisdom Integration' :
                   currentPhase === 'q' ? 'Moral Activation' :
                   currentPhase === 'f' ? 'Social Belonging' :
                   currentPhase === 'complete' ? 'Complete' : 'Introduction'}
          </span>
          <span>
            {currentPhase !== 'intro' && currentPhase !== 'complete' && 
             `${Object.values(coherenceScores).filter(s => s > 0).length}/4 dimensions assessed`}
          </span>
        </div>
      </div>
    </div>
  );
}
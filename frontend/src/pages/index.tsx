import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { User, MessageSquare, Users, BarChart3 } from 'lucide-react';
import GCTApiClient from '@/lib/api-client';
import { CoherenceProfile } from '@/types';
import AssessmentSection from '@/components/AssessmentSection';
import CommunicationSection from '@/components/CommunicationSection';
import RelationshipSection from '@/components/RelationshipSection';
import InsightsSection from '@/components/InsightsSection';
import CoherenceIndicator from '@/components/CoherenceIndicator';

const GCTDashboard: React.FC = () => {
  const [apiClient] = useState(new GCTApiClient());
  const [currentProfile, setCurrentProfile] = useState<CoherenceProfile | null>(null);
  const [activeTab, setActiveTab] = useState('assessment');
  const [userId, setUserId] = useState<string>('');

  useEffect(() => {
    // Generate or retrieve user ID
    const storedUserId = localStorage.getItem('gct_user_id');
    if (storedUserId) {
      setUserId(storedUserId);
      loadUserProfile(storedUserId);
    } else {
      const newUserId = generateUserId();
      setUserId(newUserId);
      localStorage.setItem('gct_user_id', newUserId);
    }
  }, []);

  const generateUserId = (): string => {
    return 'user_' + Math.random().toString(36).substr(2, 9);
  };

  const loadUserProfile = async (id: string) => {
    try {
      const profile = await apiClient.getUserProfile(id);
      setCurrentProfile(profile);
    } catch (error) {
      console.log('No existing profile found');
    }
  };

  return (
    <>
      <Head>
        <title>GCT Assistant - Grounded Coherence Theory</title>
        <meta name="description" content="Personal Coherence & Communication Analysis" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <header className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-indigo-600 rounded-lg flex items-center justify-center">
                    <span className="text-white font-bold text-lg">GCT</span>
                  </div>
                </div>
                <div className="ml-4">
                  <h1 className="text-2xl font-bold text-gray-900">Grounded Coherence Theory</h1>
                  <p className="text-sm text-gray-500">Personal Coherence & Communication Analysis</p>
                </div>
              </div>
              {currentProfile && (
                <div className="flex items-center space-x-4">
                  <CoherenceIndicator score={currentProfile.static_coherence} />
                </div>
              )}
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-4 mb-8 bg-white rounded-lg shadow-sm p-1">
              <TabsTrigger 
                value="assessment" 
                className="flex items-center justify-center space-x-2 px-4 py-2 rounded-md data-[state=active]:bg-indigo-600 data-[state=active]:text-white transition-all"
              >
                <User className="w-4 h-4" />
                <span>Assessment</span>
              </TabsTrigger>
              <TabsTrigger 
                value="communication" 
                className="flex items-center justify-center space-x-2 px-4 py-2 rounded-md data-[state=active]:bg-indigo-600 data-[state=active]:text-white transition-all"
              >
                <MessageSquare className="w-4 h-4" />
                <span>Communication</span>
              </TabsTrigger>
              <TabsTrigger 
                value="relationships" 
                className="flex items-center justify-center space-x-2 px-4 py-2 rounded-md data-[state=active]:bg-indigo-600 data-[state=active]:text-white transition-all"
              >
                <Users className="w-4 h-4" />
                <span>Relationships</span>
              </TabsTrigger>
              <TabsTrigger 
                value="insights" 
                className="flex items-center justify-center space-x-2 px-4 py-2 rounded-md data-[state=active]:bg-indigo-600 data-[state=active]:text-white transition-all"
              >
                <BarChart3 className="w-4 h-4" />
                <span>Insights</span>
              </TabsTrigger>
            </TabsList>

            <TabsContent value="assessment">
              <AssessmentSection 
                apiClient={apiClient} 
                userId={userId} 
                onProfileUpdate={setCurrentProfile} 
              />
            </TabsContent>

            <TabsContent value="communication">
              <CommunicationSection 
                apiClient={apiClient} 
                userId={userId} 
                currentProfile={currentProfile} 
              />
            </TabsContent>

            <TabsContent value="relationships">
              <RelationshipSection 
                apiClient={apiClient} 
                userId={userId} 
                currentProfile={currentProfile} 
              />
            </TabsContent>

            <TabsContent value="insights">
              <InsightsSection 
                currentProfile={currentProfile} 
              />
            </TabsContent>
          </Tabs>
        </main>
      </div>
    </>
  );
};

export default GCTDashboard;
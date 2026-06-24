import React, { useState, useEffect, useRef } from 'react';
import VoiceOrb from './components/VoiceOrb';
import VisualizerArea from './components/VisualizerArea';
import ProfileCardWidget from './components/widgets/ProfileCardWidget';
import useSpeechRecognition from './hooks/useSpeechRecognition';
import useSpeechSynthesis from './hooks/useSpeechSynthesis';
import { askAssistant } from './services/api';

function App() {
  const [sessionId] = useState(`session_${Math.random().toString(36).substr(2, 9)}`);
  const [agentStatus, setAgentStatus] = useState('idle'); // idle, listening, thinking, speaking, error
  const [visualPayload, setVisualPayload] = useState(null);
  const [userProfile, setUserProfile] = useState(null);
  const [transcriptDisplay, setTranscriptDisplay] = useState('');

  const { speak, stopSpeaking } = useSpeechSynthesis();

  const handleTranscriptComplete = async (finalTranscript) => {
    if (!finalTranscript.trim()) {
      setAgentStatus('idle');
      return;
    }

    setTranscriptDisplay(finalTranscript);
    setAgentStatus('thinking');

    try {
      const response = await askAssistant(finalTranscript, sessionId);
      
      if (response.visual_payload) {
        setVisualPayload(response.visual_payload);
      }
      
      // Update profile if returned (assuming backend might echo it or we extract from payload)
      // Note: In Stage 2, backend returns profile_complete status, maybe we can expose profile in response
      if (response.profile) {
        setUserProfile(response.profile);
      }

      setAgentStatus('speaking');
      speak(response.answer, () => {
        setAgentStatus('idle');
      });

    } catch (error) {
      console.error(error);
      setAgentStatus('error');
      setTimeout(() => setAgentStatus('idle'), 3000);
    }
  };

  const { isListening, transcript, startListening, stopListening, isSupported } = useSpeechRecognition({
    onTranscriptComplete: handleTranscriptComplete
  });

  // Update transcript display while listening
  useEffect(() => {
    if (isListening && transcript) {
      setTranscriptDisplay(transcript);
    }
  }, [isListening, transcript]);

  // Handle unexpected mic turn off
  useEffect(() => {
    if (!isListening && agentStatus === 'listening') {
      setAgentStatus('idle');
      setTranscriptDisplay(prev => prev || 'Microphone stopped. Please try again.');
    }
  }, [isListening]); // intentionally omitting agentStatus to avoid loops

  const handleOrbClick = () => {
    if (agentStatus === 'idle' || agentStatus === 'error') {
      startListening();
      setAgentStatus('listening');
      setTranscriptDisplay('');
    } else if (agentStatus === 'listening') {
      stopListening();
      setAgentStatus('idle'); // <--- Fix: Force state back to idle
    } else if (agentStatus === 'speaking') {
      stopSpeaking();
      setAgentStatus('idle');
    }
  };

  if (!isSupported) {
    return (
      <div style={{ color: 'white', padding: '2rem', textAlign: 'center' }}>
        <h2>Browser Not Supported</h2>
        <p>Please use Google Chrome for Speech Recognition support.</p>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="logo-text">Clymber AI</h1>
        <div className="status-indicator">
          {agentStatus === 'listening' && 'Listening...'}
          {agentStatus === 'thinking' && 'Processing...'}
          {agentStatus === 'speaking' && 'Speaking...'}
        </div>
      </header>

      <main className="main-content">
        <div className="visualizer-wrapper">
          <VisualizerArea payload={visualPayload} />
        </div>
        
        {userProfile && (
          <div className="profile-wrapper">
            <ProfileCardWidget profile={userProfile} />
          </div>
        )}
      </main>

      <footer className="app-footer">
        <div className="transcript-area glass-panel">
          {transcriptDisplay || <span style={{ opacity: 0.5 }}>Tap the microphone and start speaking...</span>}
        </div>
        <VoiceOrb status={agentStatus} onClick={handleOrbClick} />
      </footer>
    </div>
  );
}

export default App;

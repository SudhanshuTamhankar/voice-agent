import React from 'react';
import { Mic, MicOff, Loader, Volume2, AlertCircle } from 'lucide-react';
import './VoiceOrb.css';

export default function VoiceOrb({ status, onClick }) {
  // status: 'idle' | 'listening' | 'thinking' | 'speaking' | 'error'
  
  const getIcon = () => {
    switch (status) {
      case 'idle':
        return <Mic size={32} />;
      case 'listening':
        return <Mic size={32} color="#fff" />;
      case 'thinking':
        return <Loader size={32} color="#fff" />;
      case 'speaking':
        return <Volume2 size={32} color="#fff" />;
      case 'error':
        return <AlertCircle size={32} color="#fff" />;
      default:
        return <Mic size={32} />;
    }
  };

  return (
    <div className="orb-container">
      <button 
        className={`voice-orb ${status}`} 
        onClick={onClick}
        aria-label="Toggle Voice Recording"
      >
        {getIcon()}
      </button>
    </div>
  );
}

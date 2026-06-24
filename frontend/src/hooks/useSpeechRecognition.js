import { useState, useEffect, useCallback } from 'react';

export default function useSpeechRecognition({ onTranscriptComplete }) {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [recognition, setRecognition] = useState(null);

  useEffect(() => {
    if (typeof window !== 'undefined' && ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const rec = new SpeechRecognition();
      
      rec.continuous = false; // We want it to stop after one utterance
      rec.interimResults = true;
      // rec.lang = 'en-IN'; // Default to browser language to prevent unsupported locale errors
      
      rec.onresult = (event) => {
        let currentTranscript = '';
        let isFinal = false;
        
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            isFinal = true;
            currentTranscript += event.results[i][0].transcript;
          } else {
            currentTranscript += event.results[i][0].transcript;
          }
        }
        
        setTranscript(currentTranscript);
        
        if (isFinal && onTranscriptComplete) {
          setIsListening(false);
          onTranscriptComplete(currentTranscript);
        }
      };

      rec.onerror = (event) => {
        console.error('Speech recognition error', event.error);
        setIsListening(false);
      };

      rec.onend = () => {
        setIsListening(false);
      };

      setRecognition(rec);
    } else {
      console.warn('Speech recognition not supported in this browser.');
    }
  }, [onTranscriptComplete]);

  const startListening = useCallback(() => {
    if (recognition && !isListening) {
      setTranscript('');
      setIsListening(true);
      try {
        recognition.start();
      } catch (e) {
        console.error(e);
      }
    }
  }, [recognition, isListening]);

  const stopListening = useCallback(() => {
    if (recognition && isListening) {
      recognition.stop();
      setIsListening(false);
    }
  }, [recognition, isListening]);

  return {
    isListening,
    transcript,
    startListening,
    stopListening,
    isSupported: !!recognition
  };
}

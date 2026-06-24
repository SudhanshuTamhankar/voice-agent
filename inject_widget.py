import re

with open('static/clymber_raw.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

widget_code = """
<!-- VOICE WIDGET START -->
<style>
  #voice-widget-container {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 999999;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    font-family: 'Inter', sans-serif;
  }
  
  #voice-widget-window {
    width: 350px;
    height: 60vh;
    min-height: 450px;
    max-height: 800px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(30,28,36,.08);
    border-radius: 24px;
    box-shadow: 0 22px 54px -20px rgba(30,28,36,.38);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    margin-bottom: 20px;
    transition: opacity 0.3s, transform 0.3s;
    opacity: 0;
    transform: translateY(20px) scale(0.95);
    pointer-events: none;
  }
  
  #voice-widget-window.open {
    opacity: 1;
    transform: translateY(0) scale(1);
    pointer-events: auto;
  }

  .vw-header {
    background: #5036FF; /* --indigo */
    color: #fff;
    padding: 16px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'General Sans', sans-serif;
  }
  .vw-header h3 { color: #fff !important; margin: 0 !important; font-size: 18px !important; letter-spacing: 0 !important;}
  .vw-close { background: none; border: none; color: #fff; font-size: 24px; cursor: pointer; opacity: 0.8;}
  .vw-close:hover { opacity: 1; }

  .vw-body {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
    background: transparent;
  }

  .vw-msg {
    max-width: 85%;
    padding: 12px 16px;
    border-radius: 16px;
    font-size: 14px;
    line-height: 1.4;
    word-wrap: break-word;
  }
  .vw-msg.bot {
    background: #F6F5FB; /* --paper-2 */
    align-self: flex-start;
    border-bottom-left-radius: 4px;
    color: #1E1C24; /* --ink */
    border: 1px solid rgba(30,28,36,.08);
    width: 100%;
    max-width: 95%;
  }
  .vw-msg.user {
    background: #5036FF; /* --indigo */
    color: #fff;
    align-self: flex-end;
    border-bottom-right-radius: 4px;
  }

  /* Visual Smart Notes Styling */
  .vw-visual-card {
    background: #fff;
    border: 1px solid #DFD8FF;
    border-radius: 12px;
    padding: 16px;
    margin-top: 8px;
    box-shadow: 0 4px 12px rgba(80,54,255,0.05);
  }
  .vw-visual-title {
    font-family: 'General Sans', sans-serif;
    font-weight: 600;
    color: #3A26C7;
    margin-bottom: 8px;
    font-size: 15px;
  }
  .vw-visual-list {
    margin: 0;
    padding-left: 20px;
    color: #4A4854;
    font-size: 13px;
  }
  .vw-visual-list li { margin-bottom: 6px; }
  .vw-visual-highlight {
    font-weight: 600;
    color: #1E1C24;
    background: #9FEFB4;
    padding: 2px 6px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 8px;
  }

  .vw-footer {
    padding: 16px;
    border-top: 1px solid rgba(30,28,36,.08);
    background: #fff;
    display: flex;
    gap: 10px;
    align-items: center;
  }

  .vw-input {
    flex: 1;
    border: 1px solid rgba(30,28,36,.16);
    border-radius: 999px;
    padding: 12px 16px;
    font-size: 14px;
    outline: none;
    font-family: 'Inter', sans-serif;
    background: #fff;
    color: #1E1C24;
  }
  .vw-input:focus { border-color: #5036FF; }

  .vw-mic-btn {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: none;
    background: #9FEFB4; /* --mint */
    color: #2A2370; /* --deep */
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: transform 0.1s, background 0.2s;
    flex-shrink: 0;
  }
  .vw-mic-btn:hover { transform: scale(1.05); }
  .vw-mic-btn.recording {
    background: #ff4b4b !important;
    color: #fff !important;
    animation: vw-pulse 1.5s infinite;
  }
  
  .vw-send-btn {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: none;
    background: #5036FF;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    flex-shrink: 0;
  }

  #voice-widget-fab {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: #5036FF;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 12px 28px rgba(80,54,255,.4);
    cursor: pointer;
    transition: transform 0.2s;
    border: none;
  }
  #voice-widget-fab:hover {
    transform: scale(1.08);
  }
  #voice-widget-fab svg { width: 32px; height: 32px; fill: currentColor; }

  @keyframes vw-pulse {
    0% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(255, 75, 75, 0); }
    100% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
  }
  
  .vw-typing-indicator {
    font-style: italic;
    color: #7A7885; /* --muted */
    font-size: 13px;
    display: none;
    margin-top: 4px;
  }
  
  /* Onboarding View */
  #vw-onboarding {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: #fff;
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 32px;
    text-align: center;
  }
  .vw-onboard-icon {
    width: 80px; height: 80px;
    background: #DFD8FF;
    color: #3A26C7;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 24px;
  }
  .vw-onboard-icon svg { width: 40px; height: 40px; }
  .vw-onboard-title {
    font-family: 'General Sans', sans-serif;
    font-weight: 600; font-size: 20px; color: #1E1C24; margin-bottom: 12px;
  }
  .vw-onboard-text {
    font-size: 14px; color: #4A4854; margin-bottom: 32px; line-height: 1.5;
  }
  .vw-explore-btn {
    background: #5036FF; color: #fff;
    border: none; border-radius: 999px;
    padding: 16px 24px; font-size: 15px; font-weight: 600;
    cursor: pointer; box-shadow: 0 8px 20px rgba(80,54,255,0.3);
    transition: transform 0.2s; width: 100%;
  }
  .vw-explore-btn:hover { transform: translateY(-2px); box-shadow: 0 12px 24px rgba(80,54,255,0.4); }
</style>

<div id="voice-widget-container">
  <div id="voice-widget-window">
    <div class="vw-header">
      <h3>Admissions Assistant</h3>
      <button class="vw-close" id="vw-close-btn">&times;</button>
    </div>
    
    <!-- ONBOARDING VIEW -->
    <div id="vw-onboarding">
      <div class="vw-onboard-icon">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9-4.03-9-9-9zm0 16c-3.86 0-7-3.14-7-7s3.14-7 7-7 7 3.14 7 7-3.14 7-7 7zm1-11h-2v3H8v2h3v3h2v-3h3v-2h-3V8z"/></svg>
      </div>
      <div class="vw-onboard-title">AI Admissions Assistant</div>
      <div class="vw-onboard-text">Speak to our intelligent agent to evaluate your profile, estimate percentiles, and find the right B-Schools.</div>
      <button class="vw-explore-btn" id="vw-explore-btn">Explore Your Potential</button>
    </div>

    <!-- CHAT VIEW -->
    <div class="vw-body" id="vw-chat-body" style="display:none;">
      <div class="vw-typing-indicator" id="vw-typing">Assistant is typing...</div>
    </div>
    <div class="vw-footer" id="vw-chat-footer" style="display:none;">
      <input type="text" id="vw-text-input" class="vw-input" placeholder="Type a message or tap mic..." autocomplete="off" />
      <button id="vw-mic-btn" class="vw-mic-btn">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.91-3c-.49 0-.9.39-.9.88 0 2.71-2.26 4.96-4.96 4.96s-5.06-2.22-5.06-4.96c0-.5-.4-.9-.9-.9s-.9.39-.9.88c0 3.25 2.5 5.92 5.67 6.35V21c0 .55.45 1 1 1s1-.45 1-1v-2.78c3.17-.43 5.67-3.1 5.67-6.35 0-.49-.4-.88-.88-.88z"/></svg>
      </button>
      <button id="vw-send-btn" class="vw-send-btn" style="display:none;">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
      </button>
    </div>
  </div>

  <button id="voice-widget-fab">
    <svg viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.91-3c-.49 0-.9.39-.9.88 0 2.71-2.26 4.96-4.96 4.96s-5.06-2.22-5.06-4.96c0-.5-.4-.9-.9-.9s-.9.39-.9.88c0 3.25 2.5 5.92 5.67 6.35V21c0 .55.45 1 1 1s1-.45 1-1v-2.78c3.17-.43 5.67-3.1 5.67-6.35 0-.49-.4-.88-.88-.88z"/></svg>
  </button>
</div>

<script>
  (function() {
    const fab = document.getElementById('voice-widget-fab');
    const win = document.getElementById('voice-widget-window');
    const closeBtn = document.getElementById('vw-close-btn');
    const chatBody = document.getElementById('vw-chat-body');
    const textInput = document.getElementById('vw-text-input');
    const micBtn = document.getElementById('vw-mic-btn');
    const sendBtn = document.getElementById('vw-send-btn');
    const typingIndicator = document.getElementById('vw-typing');
    const exploreBtn = document.getElementById('vw-explore-btn');
    const onboardingView = document.getElementById('vw-onboarding');
    const chatFooter = document.getElementById('vw-chat-footer');

    const sessionId = 'web_session_' + Math.random().toString(36).substring(7);
    let currentAudio = null;
    let isInitiated = false;

    fab.addEventListener('click', () => {
      win.classList.toggle('open');
      if (win.classList.contains('open') && isInitiated) {
        setTimeout(() => textInput.focus(), 300);
      }
    });

    closeBtn.addEventListener('click', () => {
      win.classList.remove('open');
      if(currentAudio) {
        currentAudio.pause();
      }
    });

    exploreBtn.addEventListener('click', async () => {
      isInitiated = true;
      onboardingView.style.display = 'none';
      chatBody.style.display = 'flex';
      chatFooter.style.display = 'flex';
      
      const welcomeText = "Hi! I am the Clymber AI Admissions Assistant. I can evaluate your profile, recommend colleges, or explain IIM shortlisting methodologies. How can I help you today?";
      
      // Show speaking indicator but no text yet
      typingIndicator.style.display = 'block';
      typingIndicator.textContent = "Assistant is speaking...";
      
      // Wait for the speech to load and start playing
      await playTTS(welcomeText);
      
      // Once audio is ready and playing, hide indicator
      typingIndicator.style.display = 'none';
      typingIndicator.textContent = "Assistant is typing...";
      
      // You can either show the text now, or just leave it empty. We will show a short prompt.
      addSimpleMessage("How can I help you today?", 'bot');
    });

    // Also highlight on the site that this is the Voice Agent demo
    window.addEventListener('DOMContentLoaded', () => {
        // Try to find the main hero heading and change it
        const h1s = document.querySelectorAll('h1');
        h1s.forEach(h1 => {
            if(h1.textContent.includes('Clear CAT') || h1.textContent.includes('top IIMs')) {
                h1.innerHTML = 'Experience the <br><em style="color:#5036FF;">Clymber Voice Agent</em>';
            }
        });
        const subtitles = document.querySelectorAll('p.hero-sub');
        subtitles.forEach(p => {
            if(p.textContent.includes('Personalized CAT prep') || p.textContent.includes('No mass coaching')) {
                p.innerHTML = '<strong>Voice-First AI Assistant.</strong> Click the purple microphone button in the bottom right corner to start talking to our new admissions expert!';
            }
        });
    });

    textInput.addEventListener('input', () => {
      if (textInput.value.trim().length > 0) {
        micBtn.style.display = 'none';
        sendBtn.style.display = 'flex';
      } else {
        micBtn.style.display = 'flex';
        sendBtn.style.display = 'none';
      }
    });

    textInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') handleSend();
    });
    sendBtn.addEventListener('click', () => handleSend());

    function addSimpleMessage(text, sender) {
      const el = document.createElement('div');
      el.className = `vw-msg ${sender}`;
      el.textContent = text;
      chatBody.insertBefore(el, typingIndicator);
      chatBody.scrollTop = chatBody.scrollHeight;
    }

    function addVisualMessage(payload) {
      const el = document.createElement('div');
      el.className = `vw-msg bot`;
      
      let html = '';
      if (payload.type === 'evaluation') {
         html += `<div class="vw-visual-highlight">${payload.data.label}</div>`;
         html += `<div class="vw-visual-card">`;
         html += `<div class="vw-visual-title">Composite Score: ${payload.data.composite_score || 'N/A'}</div>`;
         html += `<div><strong>Strengths:</strong> ${payload.data.strengths}</div>`;
         html += `<div style="margin-top:4px;"><strong>Risks:</strong> ${payload.data.risks}</div>`;
         html += `</div>`;
      } 
      else if (payload.type === 'percentile_target') {
         const target = payload.data.is_possible ? payload.data.percentile_range : 'Not Reachable';
         html += `<div class="vw-visual-highlight">Target: ${target} %ile</div>`;
         html += `<div class="vw-visual-card">`;
         html += `<div class="vw-visual-title">${payload.data.institute_id.toUpperCase().replace('_', ' ')}</div>`;
         html += `<div style="font-size:13px;color:#4A4854;">${payload.data.explanation}</div>`;
         html += `</div>`;
      }
      else if (payload.type === 'formula') {
         html += `<div class="vw-visual-highlight">Methodology Notes</div>`;
         html += `<div class="vw-visual-card">`;
         html += `<div class="vw-visual-title">${payload.data.institute}</div>`;
         if (payload.data.formula && payload.data.formula !== "Not Disclosed") {
             html += `<div style="margin-bottom:8px;font-size:14px;color:#1E1C24;"><strong>Formula:</strong> ${payload.data.formula}</div>`;
         }
         html += `<ul class="vw-visual-list">`;
         if (payload.data.key_factors && Array.isArray(payload.data.key_factors)) {
             payload.data.key_factors.forEach(bp => {
                 html += `<li>${bp}</li>`;
             });
         }
         html += `</ul></div>`;
      }
      else if (payload.type === 'recommendation_list') {
         html += `<div class="vw-visual-highlight">College Matches</div>`;
         html += `<div class="vw-visual-card">`;
         if (payload.data.safe && payload.data.safe.length > 0) html += `<div><strong>Safe:</strong> ${payload.data.safe.join(', ')}</div>`;
         if (payload.data.target && payload.data.target.length > 0) html += `<div style="margin-top:4px;"><strong>Target:</strong> ${payload.data.target.join(', ')}</div>`;
         if (payload.data.stretch && payload.data.stretch.length > 0) html += `<div style="margin-top:4px;"><strong>Stretch:</strong> ${payload.data.stretch.join(', ')}</div>`;
         html += `</div>`;
      }
      else if (payload.type === 'missing_fields') {
         html += `<div class="vw-visual-highlight" style="background:#FFE6E6;color:#D32F2F;">Missing Information</div>`;
         html += `<div class="vw-visual-card">`;
         html += `<div class="vw-visual-title" style="color:#D32F2F;">Please Provide:</div>`;
         html += `<ul class="vw-visual-list">`;
         if (payload.data.fields && Array.isArray(payload.data.fields)) {
             payload.data.fields.forEach(f => {
                 let niceName = f.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                 html += `<li>${niceName}</li>`;
             });
         }
         html += `</ul></div>`;
      }
      else {
         html = payload.text || JSON.stringify(payload);
      }
      
      el.innerHTML = html;
      chatBody.insertBefore(el, typingIndicator);
      chatBody.scrollTop = chatBody.scrollHeight;
    }

    async function handleSend(textOverride = null) {
      const text = textOverride || textInput.value.trim();
      if (!text) return;
      
      textInput.value = '';
      micBtn.style.display = 'flex';
      sendBtn.style.display = 'none';
      
      // Do not show the user's transcript in the UI
      typingIndicator.style.display = 'block';
      chatBody.scrollTop = chatBody.scrollHeight;

      if(currentAudio) {
        currentAudio.pause();
        currentAudio = null;
      }

      try {
        const res = await fetch('/ask', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: text, session_id: sessionId })
        });
        
        const data = await res.json();
        
        if (data.answer) {
          // Await TTS so the visual card only appears when audio is ready to play
          await playTTS(data.answer);
          
          typingIndicator.style.display = 'none';
          
          if (data.visual_payload) {
             addVisualMessage(data.visual_payload);
          } else {
             addSimpleMessage(data.answer, 'bot');
          }
        } else {
          typingIndicator.style.display = 'none';
          addSimpleMessage("Sorry, I encountered an error.", 'bot');
        }
      } catch (err) {
        typingIndicator.style.display = 'none';
        addSimpleMessage("Connection error. Is the backend running?", 'bot');
      }
    }

    async function playTTS(text) {
      try {
        const res = await fetch('/tts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: text, session_id: sessionId })
        });
        if(res.ok) {
            const blob = await res.blob();
            const url = URL.createObjectURL(blob);
            currentAudio = new Audio(url);
            currentAudio.play();
        }
      } catch(err) {
        console.error("TTS failed", err);
      }
    }

    let mediaRecorder = null;
    let audioChunks = [];
    let audioContext = null;
    let analyser = null;
    let vadStream = null;
    let vadReq = null;

    function startVAD() {
      if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (audioContext.state === 'suspended') {
        audioContext.resume();
      }
      
      analyser = audioContext.createAnalyser();
      analyser.minDecibels = -90;
      analyser.maxDecibels = -10;
      analyser.smoothingTimeConstant = 0.85;
      
      const source = audioContext.createMediaStreamSource(vadStream);
      source.connect(analyser);
      
      const bufferLength = analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);
      
      let speechStarted = false;
      let silenceStart = Date.now();
      const SILENCE_THRESHOLD = 15;
      const SILENCE_DURATION = 2000; // 2 seconds of silence after speaking
      const MAX_SILENCE_DURATION = 5000; // 5 seconds of silence if no speaking
      
      function detectSilence() {
        if (!mediaRecorder || mediaRecorder.state !== 'recording') return;
        
        analyser.getByteFrequencyData(dataArray);
        let sum = 0;
        for(let i=0; i<bufferLength; i++) {
            sum += dataArray[i];
        }
        let average = sum / bufferLength;
        
        if (average > SILENCE_THRESHOLD) {
            speechStarted = true;
            silenceStart = Date.now();
        } else {
            if (speechStarted && (Date.now() - silenceStart > SILENCE_DURATION)) {
                mediaRecorder.stop();
                return;
            } else if (!speechStarted && (Date.now() - silenceStart > MAX_SILENCE_DURATION)) {
                mediaRecorder.stop();
                return;
            }
        }
        vadReq = requestAnimationFrame(detectSilence);
      }
      
      vadReq = requestAnimationFrame(detectSilence);
    }

    async function initMediaRecorder() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        vadStream = stream;
        mediaRecorder = new MediaRecorder(stream);
        
        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunks.push(event.data);
          }
        };

        mediaRecorder.onstart = () => {
          audioChunks = [];
          micBtn.classList.add('recording');
          startVAD();
        };

        mediaRecorder.onstop = async () => {
          if (vadReq) cancelAnimationFrame(vadReq);
          micBtn.classList.remove('recording');
          const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
          
          // Send to backend for transcription
          typingIndicator.style.display = 'block';
          typingIndicator.textContent = "Thinking...";
          chatBody.scrollTop = chatBody.scrollHeight;
          
          const formData = new FormData();
          formData.append('file', audioBlob, 'recording.webm');
          
          try {
            const res = await fetch('/transcribe', {
              method: 'POST',
              body: formData
            });
            if (res.ok) {
              const data = await res.json();
              if (data.text) {
                handleSend(data.text);
              } else {
                typingIndicator.style.display = 'none';
              }
            } else {
              typingIndicator.style.display = 'none';
              addSimpleMessage("Sorry, could not transcribe audio.", 'bot');
            }
          } catch (err) {
            typingIndicator.style.display = 'none';
            console.error(err);
          }
        };
        
        return true;
      } catch (err) {
        console.error("Microphone access denied or error:", err);
        return false;
      }
    }

    micBtn.addEventListener('click', async () => {
      if (currentAudio) currentAudio.pause();
      
      if (micBtn.classList.contains('recording')) {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
          mediaRecorder.stop();
        }
      } else {
        if (!mediaRecorder) {
          const success = await initMediaRecorder();
          if (!success) {
            alert("Microphone access is required to use voice input.");
            return;
          }
        }
        mediaRecorder.start();
      }
    });
  })();
</script>
<!-- VOICE WIDGET END -->
"""

# Clean up missing assets to prevent 404 errors in the terminal
import re
# Remove all images
html_content = re.sub(r'<img[^>]*>', '', html_content, flags=re.IGNORECASE)
# Remove picture tags
html_content = re.sub(r'<picture.*?</picture>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
# Remove iframes (other widgets)
html_content = re.sub(r'<iframe.*?</iframe>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
# Remove external scripts that might try to load assets
html_content = re.sub(r'<script\b[^>]*src=[^>]*>.*?</script>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
# Remove inline styles with background-image urls
html_content = re.sub(r'url\([^)]+\)', 'none', html_content, flags=re.IGNORECASE)

# Replace any lingering image paths in inline scripts (like /landing/StudentImage/...) with a transparent 1x1 pixel data URI
blank_pixel = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="
html_content = re.sub(r'/[^"\']+\.(png|webp|jpg|jpeg|svg)', blank_pixel, html_content, flags=re.IGNORECASE)

if "</body>" in html_content:
    new_html = html_content.replace("</body>", widget_code + "\n</body>")
else:
    new_html = html_content + widget_code

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Widget injected into static/index.html successfully!")

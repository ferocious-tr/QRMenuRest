"""
Utility for playing notification sounds in Streamlit
"""

import streamlit as st
import streamlit.components.v1 as components

def play_notification_sound_v1():
    """
    Play notification sound using Web Audio API (synthetic beep)
    This creates a simple beep sound without external files
    """
    sound_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script>
            window.onload = function() {
                try {
                    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    
                    // Create oscillator for beep sound
                    const oscillator = audioContext.createOscillator();
                    const gainNode = audioContext.createGain();
                    
                    oscillator.connect(gainNode);
                    gainNode.connect(audioContext.destination);
                    
                    // Configure sound (pleasant notification tone)
                    oscillator.frequency.value = 800; // Hz
                    oscillator.type = 'sine';
                    
                    // Volume envelope (fade in/out)
                    gainNode.gain.setValueAtTime(0, audioContext.currentTime);
                    gainNode.gain.linearRampToValueAtTime(0.5, audioContext.currentTime + 0.01);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
                    
                    // Play sound
                    oscillator.start(audioContext.currentTime);
                    oscillator.stop(audioContext.currentTime + 0.5);
                } catch (e) {
                    console.log('Audio playback failed:', e);
                }
            };
        </script>
    </head>
    <body style="margin:0;padding:0;"></body>
    </html>
    """
    components.html(sound_html, height=0, width=0)

def play_notification_sound_v2():
    """
    Play notification sound using dual-tone beep (more attention-grabbing)
    """
    sound_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script>
            window.onload = function() {
                try {
                    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    
                    // First beep (higher pitch)
                    const osc1 = audioContext.createOscillator();
                    const gain1 = audioContext.createGain();
                    osc1.connect(gain1);
                    gain1.connect(audioContext.destination);
                    osc1.frequency.value = 1000;
                    osc1.type = 'sine';
                    gain1.gain.setValueAtTime(0.5, audioContext.currentTime);
                    gain1.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.15);
                    osc1.start(audioContext.currentTime);
                    osc1.stop(audioContext.currentTime + 0.15);
                    
                    // Second beep (lower pitch) - slightly delayed
                    const osc2 = audioContext.createOscillator();
                    const gain2 = audioContext.createGain();
                    osc2.connect(gain2);
                    gain2.connect(audioContext.destination);
                    osc2.frequency.value = 800;
                    osc2.type = 'sine';
                    gain2.gain.setValueAtTime(0.5, audioContext.currentTime + 0.2);
                    gain2.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.35);
                    osc2.start(audioContext.currentTime + 0.2);
                    osc2.stop(audioContext.currentTime + 0.35);
                } catch (e) {
                    console.log('Audio playback failed:', e);
                }
            };
        </script>
    </head>
    <body style="margin:0;padding:0;"></body>
    </html>
    """
    components.html(sound_html, height=0, width=0)

def play_notification_sound_v3():
    """
    Play notification sound from external URL
    Requires internet connection
    """
    sound_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script>
            window.onload = function() {
                var audio = new Audio('https://assets.mixkit.co/active_storage/sfx/2354/2354-preview.mp3');
                audio.play().catch(e => console.log('Audio playback failed:', e));
            };
        </script>
    </head>
    <body style="margin:0;padding:0;"></body>
    </html>
    """
    components.html(sound_html, height=0, width=0)

def play_success_sound():
    """
    Play a pleasant success/completion sound
    """
    sound_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script>
            window.onload = function() {
                try {
                    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    
                    // Ascending three-note chord (C-E-G)
                    const notes = [523.25, 659.25, 783.99]; // Hz
                    
                    notes.forEach((freq, index) => {
                        const osc = audioContext.createOscillator();
                        const gain = audioContext.createGain();
                        osc.connect(gain);
                        gain.connect(audioContext.destination);
                        osc.frequency.value = freq;
                        osc.type = 'sine';
                        
                        const startTime = audioContext.currentTime + (index * 0.1);
                        gain.gain.setValueAtTime(0.5, startTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, startTime + 0.3);
                        
                        osc.start(startTime);
                        osc.stop(startTime + 0.3);
                    });
                } catch (e) {
                    console.log('Audio playback failed:', e);
                }
            };
        </script>
    </head>
    <body style="margin:0;padding:0;"></body>
    </html>
    """
    components.html(sound_html, height=0, width=0)

def play_alert_sound():
    """
    Play an urgent alert sound (for important notifications)
    """
    sound_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script>
            window.onload = function() {
                try {
                    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    
                    // Three rapid beeps
                    for (let i = 0; i < 3; i++) {
                        const osc = audioContext.createOscillator();
                        const gain = audioContext.createGain();
                        osc.connect(gain);
                        gain.connect(audioContext.destination);
                        osc.frequency.value = 1200;
                        osc.type = 'square';
                        
                        const startTime = audioContext.currentTime + (i * 0.2);
                        gain.gain.setValueAtTime(0.25, startTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, startTime + 0.1);
                        
                        osc.start(startTime);
                        osc.stop(startTime + 0.1);
                    }
                } catch (e) {
                    console.log('Audio playback failed:', e);
                }
            };
        </script>
    </head>
    <body style="margin:0;padding:0;"></body>
    </html>
    """
    components.html(sound_html, height=0, width=0)

# Default export - use the dual-tone version
play_notification_sound = play_notification_sound_v2

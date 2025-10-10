# GitHub Copilot Instructions for Rainvow Repository

## Project Overview

Rainvow is a collection of multimedia and visualization tools written primarily in Python, with some HTML/JavaScript components for AR experiences. The project focuses on:

- Audio visualization (ondads.py)
- RGB keyboard control (keyboard_rgb.py)
- System monitoring with context awareness (hydra_observer.py)
- Spotify integration for live music display (spotify_live/)
- Augmented Reality demos with Hydra-synth effects (ar.html, pdf_overlay.html)
- TikTok streaming setup automation (live.sh)

## Language and Style Guidelines

### Python Code
- **Language**: All code comments and docstrings should be in Spanish
- **Style**: Follow PEP 8 conventions
- **Dependencies**: Use standard libraries when possible; external dependencies include:
  - `numpy`, `sounddevice` for audio processing
  - `psutil`, `pynput` for system monitoring
  - `spotipy`, `flask` for Spotify integration
  - `openrgb-python` for keyboard control
  - `rich`, `colorama` for terminal colors
- **Error Handling**: Use try/except blocks with fallbacks (see audio_source() in ondads.py)

### Shell Scripts
- Use `zsh` (#!/bin/zsh) for shell scripts
- Include dependency checks with Homebrew installation
- Always use `set -e` for error handling
- Log outputs with `exec > >(tee -a ~/live.log) 2>&1`
- Include cleanup functions with trap handlers

### HTML/JavaScript
- Use external CDN libraries (A-Frame, AR.js, Hydra-synth, PDF.js)
- Keep styling inline or in `<style>` tags
- Use dark themes (#121212 backgrounds)
- Ensure responsive design with viewport meta tags

## Key Components

### Audio Visualization (ondads.py)
- Real-time audio capture with sounddevice
- FFT-based frequency band analysis
- Adaptive gain control per band
- Rich console output with rainbow colors
- Fallback to noise if audio input fails

### System Observer (hydra_observer.py)
- Monitors CPU, memory, and active window
- Detects context (ZIP, music) and triggers actions
- Records audio samples when music context detected
- Logs events to JSON files in logs/ directory
- Uses threading for concurrent monitoring

### Spotify Live (spotify_live/)
- Flask web application (port 8888)
- OAuth2 flow with Spotify API
- Real-time currently playing track display
- Search functionality with preview audio
- Templates in templates/index.html

### Live Streaming (live.sh)
- Automates TikTok streaming setup on macOS
- Manages scrcpy, sndcpy, VLC, and audio routing
- Uses BlackHole for virtual audio devices
- Requires Homebrew packages: scrcpy, vlc, switchaudio-osx, adb

### AR Demos (ar.html, pdf_overlay.html)
- A-Frame + AR.js for marker-based AR
- Hydra-synth overlays for visual effects
- HIRO marker detection
- PDF rendering with pdf.js
- Canvas blending modes for effects

## Common Patterns

### Audio Processing
```python
# Always include fallback for failed audio input
try:
    with sd.InputStream(...) as stream:
        # process audio
except Exception:
    # fallback to test data
```

### Color Themes
- Rainbow colors: ["red", "orange1", "yellow1", "green1", "cyan", "blue", "magenta"]
- Dark backgrounds: #121212 or #222
- Terminal colors use colorama or rich

### Environment Variables
- `HYDRA_CLI`: Path to hydra CLI tool
- `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, `SPOTIPY_REDIRECT_URI`: Spotify API credentials
- `FLASK_SECRET`: Flask session secret

## File Organization

```
/
├── README.md                   # Main documentation (Spanish)
├── ondads.py                   # Audio visualizer
├── keyboard_rgb.py             # RGB keyboard controller
├── hydra_observer.py           # System monitor with context detection
├── screenshot.py               # Screenshot utility
├── pentaquark.py               # Utility script
├── live.sh                     # TikTok streaming automation
├── ar.html                     # AR demo with marker detection
├── pdf_overlay.html            # PDF viewer with Hydra overlay
├── spotify_live/               # Spotify web app
│   ├── app.py                  # Flask application
│   ├── templates/
│   │   └── index.html          # Main UI
│   └── README.md               # Setup instructions
└── aurawave/                   # Additional utilities
```

## Development Workflow

1. **Testing Python scripts**: Run directly with `python3 script.py`
2. **Dependencies**: Install with `pip install <package>` or use requirements if present
3. **Web apps**: Start with `python3 app.py` (Flask) or `python3 -m http.server` (static)
4. **Shell scripts**: Make executable with `chmod +x` before running
5. **Logs**: Check logs/ directory for system observer output
6. **Screenshots**: Saved to screenshots/ directory

## Important Notes

- All user-facing messages and documentation should be in Spanish
- Code should handle missing dependencies gracefully
- Audio/video tools need hardware access (microphone, camera)
- macOS-specific scripts use Homebrew for dependency management
- Web AR requires HTTPS or localhost for camera access
- Always provide fallback behavior for missing hardware/services

## When Suggesting Code Changes

1. Maintain Spanish for user-facing text and documentation
2. Keep existing error handling patterns
3. Preserve dark theme aesthetics
4. Use existing dependency libraries
5. Follow the established file organization
6. Include appropriate fallbacks for hardware/service failures
7. Test with minimal dependencies when possible

## Testing and Quality Assurance

### Manual Testing
Since this is a collection of utilities without formal test suites, testing is primarily manual:

1. **Audio Scripts**: Test with actual audio input or verify fallback to test data
   ```bash
   python3 ondads.py  # Should show rainbow visualization or fallback gracefully
   ```

2. **Spotify Integration**: Test OAuth flow and API calls
   ```bash
   cd spotify_live && python3 app.py  # Access http://localhost:8888
   ```

3. **System Observer**: Verify monitoring and logging
   ```bash
   python3 hydra_observer.py  # Check logs/ directory for output
   ```

4. **AR Demos**: Test in browser with HTTPS or localhost
   ```bash
   python3 -m http.server 8000  # Access http://localhost:8000/ar.html
   ```

### Code Quality
- Follow PEP 8 for Python code
- Use descriptive variable names in Spanish for user-facing strings
- Keep functions small and focused (see modular design in ondads.py)
- Always include error handling with try/except blocks
- Test graceful degradation when dependencies are missing

### Validation Checklist
Before submitting changes:
- [ ] Code runs without errors
- [ ] Fallback behavior works when hardware/services unavailable
- [ ] Spanish text is grammatically correct
- [ ] No new unnecessary dependencies introduced
- [ ] Dark theme preserved in HTML/web interfaces
- [ ] Existing functionality not broken

## Dependency Management

### Python Dependencies
Install required packages individually as needed:

```bash
# Audio visualization
pip install numpy sounddevice rich colorama

# System monitoring
pip install psutil pynput pygetwindow

# Spotify integration
pip install spotipy flask

# RGB keyboard control
pip install openrgb-python

# Screenshots
pip install pyautogui
```

**Note**: Not all dependencies are required for all scripts. Each script handles missing dependencies gracefully with try/except blocks.

### macOS Dependencies (for live.sh)
```bash
brew install scrcpy vlc switchaudio-osx
brew install --cask android-platform-tools  # for adb
```

### Checking Dependencies
Each Python script should check for dependencies and provide helpful error messages:

```python
try:
    import required_module
except ImportError:
    print("Please install: pip install required_module")
    # Optionally provide fallback behavior
```

## Troubleshooting Common Issues

### Audio Not Working
- **Issue**: `ondads.py` shows no audio input or errors
- **Solution**: Check microphone permissions, try fallback mode, verify sounddevice installation
- **Fallback**: Script automatically generates test data if audio fails

### Spotify API Errors
- **Issue**: OAuth flow fails or 401 errors
- **Solution**: Verify `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, and `SPOTIPY_REDIRECT_URI` environment variables
- **Check**: Ensure redirect URI matches exactly in Spotify Developer Dashboard

### AR Demo Not Loading Camera
- **Issue**: Camera permission denied or AR.js not detecting marker
- **Solution**: Use HTTPS or localhost, grant camera permissions, use HIRO marker
- **Test**: Print HIRO marker from https://github.com/AR-js-org/AR.js#hiro-marker

### RGB Keyboard Not Responding
- **Issue**: `keyboard_rgb.py` cannot connect to OpenRGB
- **Solution**: Ensure OpenRGB server is running, check connection settings
- **Verify**: OpenRGB SDK server must be enabled in OpenRGB settings

### System Observer Not Logging
- **Issue**: `hydra_observer.py` not creating logs
- **Solution**: Check write permissions for logs/ directory
- **Check**: Verify `pygetwindow` works on your platform (may not work on all systems)

## Examples and Patterns

### Creating a New Audio Visualizer
```python
import numpy as np
import sounddevice as sd
from rich.console import Console

console = Console()

def audio_callback(indata, frames, time, status):
    """Process audio data in real-time"""
    if status:
        console.print(f"[red]Error: {status}[/red]")
    
    # Your visualization logic here
    volume = np.linalg.norm(indata) * 10
    console.print(f"[cyan]Volume: {volume:.2f}[/cyan]")

try:
    with sd.InputStream(callback=audio_callback, channels=1):
        console.print("[green]Starting audio visualization...[/green]")
        sd.sleep(10000)  # Run for 10 seconds
except Exception as e:
    console.print(f"[yellow]Audio not available: {e}[/yellow]")
    # Fallback to test data
```

### Adding a New Spotify Endpoint
```python
@app.route('/api/recently-played')
def recently_played():
    """Get user's recently played tracks"""
    token = session.get('token')
    if not token:
        return jsonify({'error': 'No autenticado'}), 401
    
    try:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_recently_played(limit=10)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### Creating a New Hydra Effect
```html
<script src="https://unpkg.com/hydra-synth"></script>
<script>
  const hydra = new Hydra({ detectAudio: false });
  
  // Custom rainbow pattern
  osc(10, 0.1, 1.5)
    .color(1.0, 0.5, 0.8)
    .rotate(0, 0.1)
    .modulate(osc(3, 0.5))
    .out();
</script>
```

### System Monitoring Pattern
```python
import psutil
import time

def monitor_loop(interval=1.0):
    """Monitor system resources continuously"""
    while True:
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        
        # Your monitoring logic here
        if cpu > 80:
            print(f"⚠️  High CPU usage: {cpu}%")
        
        time.sleep(interval)

if __name__ == "__main__":
    try:
        monitor_loop()
    except KeyboardInterrupt:
        print("Monitoring stopped")
```

## Project Maintenance

### Adding New Features
1. Create standalone script or extend existing component
2. Follow existing patterns (error handling, fallbacks, Spanish messages)
3. Update README.md with new feature description
4. Add example usage to this file if pattern is reusable

### Updating Dependencies
- Test thoroughly before updating major versions
- Maintain backward compatibility where possible
- Document breaking changes in CHANGELOG.md

### Documentation Updates
When code changes:
1. Update relevant README sections
2. Update ARCHITECTURE.md if modular structure changes
3. Add examples to this copilot-instructions.md if new patterns introduced
4. Update CHANGELOG.md with notable changes

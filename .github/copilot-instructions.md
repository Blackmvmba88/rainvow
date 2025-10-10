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

## Testing Guidelines

Since this project uses manual testing rather than automated unit tests:
- Verify Python scripts by running them directly: `python3 script.py`
- Test Flask applications by starting the server and checking endpoints
- Validate audio/video components with actual hardware when possible
- Use fallback modes (test data, noise) when hardware isn't available
- Document test results in TESTING.md following existing format
- Check logs/ directory for system observer output during testing

## Build and Validation

- **No build step required**: Python scripts run directly
- **Linting**: Follow PEP 8, though no automated linter is configured
- **Dependencies**: Install manually with `pip install <package>`
- **Git workflow**: Keep commits small and focused
- **Ignored files**: `.gitignore` excludes `__pycache__/`, `*.pyc`, `.env`

## Security Best Practices

- Never commit sensitive credentials to the repository
- Use environment variables for API keys and secrets:
  - `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, `SPOTIPY_REDIRECT_URI`
  - `FLASK_SECRET`
  - `HYDRA_CLI`
- Store credentials in `.env` (already in `.gitignore`)
- Validate external inputs in web applications
- Use OAuth2 flows correctly (see spotify_live/app.py as reference)

## Common Tasks

### Adding a new Python utility
1. Create script in repository root
2. Add Spanish docstring at the top
3. Include try/except for missing dependencies with helpful error messages
4. Add usage instructions to README.md
5. Test manually and document in TESTING.md

### Modifying audio/visual components
1. Maintain modular architecture (separate functions for capture, analysis, visualization)
2. Keep fallback modes for testing without hardware
3. Use existing color schemes (rainbow colors, dark backgrounds)
4. Test with actual hardware when possible

### Updating Flask applications
1. Maintain existing OAuth flow patterns
2. Keep Spanish user-facing messages
3. Test all routes manually
4. Verify token refresh logic
5. Update templates/ if UI changes required

#!/bin/bash
set -e

mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"

# Start virtual framebuffer
Xvfb :99 -screen 0 1280x1024x24 &
sleep 1

# Start XFCE4 desktop session
dbus-launch xfce4-session &
sleep 3

# Expose the virtual desktop over noVNC for local interactive debugging.
x11vnc -display :99 -forever -shared -nopw -listen 0.0.0.0 -rfbport 5900 &
websockify --web=/usr/share/novnc 0.0.0.0:6080 localhost:5900 &

# Launch the challenge GUI
python3 challenge.py &
sleep 2

# Start the MCP server (foreground)
exec python3 server.py

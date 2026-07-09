#!/bin/sh
echo "Installing Kado Panel v0.1.0 Alpha..."
PLUGIN_DIR="/usr/lib/enigma2/python/Plugins/Extensions/KadoPanel"
mkdir -p "$PLUGIN_DIR"
cp -r KadoPanel/src/* "$PLUGIN_DIR/"
chmod -R 755 "$PLUGIN_DIR"
echo "Kado Panel installed. Please restart Enigma2."

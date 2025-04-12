#!/usr/bin/env bash

set -o errexit

# Install system dependencies
apt-get update
apt-get install -y portaudio19-dev

# Install Python dependencies
pip install -r requirements.txt

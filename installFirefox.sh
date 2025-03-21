#!/bin/bash

# Remove Snap version of Firefox
sudo snap remove firefox

# Add Mozilla PPA
sudo add-apt-repository ppa:mozillateam/ppa
sudo apt update

# Set package priority
echo -e "Package: *\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 1001" | sudo tee /etc/apt/preferences.d/mozilla-firefox

# Install Firefox via APT
sudo apt install firefox

# Prevent Firefox Snap from reinstalling
echo "firefox hold" | sudo dpkg --set-selections

#!/bin/bash

## Update package lists to ensure latest package info
echo "Updating package list..."
sudo apt update -y

## Install make, python3.12-venv, and tree
echo "Installing required packages..."
sudo apt install -y make python3.12-venv tree

## Confirm installations were successful
echo "Installation complete. Verifying installed packages..."

## Check versions of installations
make --version | head -n 1
python3 --version
tree --version

echo "Installations successful. You're good to go!"

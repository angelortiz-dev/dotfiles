#!/usr/bin/env fish

set -e

# Ensure config directory exists
mkdir -p ~/.config

# Get repo root (current working directory)
set REPO_ROOT (pwd)

# Symlink dotfiles
ln -sf $REPO_ROOT/ghostty ~/.config/ghostty
ln -sf $REPO_ROOT/tmux/tmux.conf ~/.tmux.conf
ln -sf $REPO_ROOT/fish ~/.config/fish
ln -sf $REPO_ROOT/starship ~/.config/starship
ln -sf $REPO_ROOT/nvim ~/.config/nvim
ln -sf $REPO_ROOT/brewfile ~/.config/brewfile/Brewfile

echo "✅ Dotfiles installed"

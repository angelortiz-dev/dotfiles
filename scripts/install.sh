#!/usr/bin/env bash
set -e

mkdir -p ~/.config

ln -sf $(pwd)/ghostty ~/.config/ghostty
ln -sf $(pwd)/tmux/tmux.conf ~/.tmux.conf
ln -sf $(pwd)/fish ~/.config/fish
ln -sf $(pwd)/starship ~/.config/starship
ln -sf $(pwd)/nvim ~/.config/nvim
ln -sf $(pwd)/brewfile ~/.config/brewfile

echo "✅ Dotfiles installed"

# 🚀 Dotfiles

A clean, minimalist macOS development environment configuration for Ghostty, Fish, Neovim, and Starship.

## 📋 What's Included

- **Ghostty** - Modern GPU-accelerated terminal emulator
- **Fish Shell** - User-friendly shell with intelligent auto-completion
- **Starship** - Fast, minimal, customizable shell prompt
- **Neovim** - Extensible text editor with Lua configuration
- **Homebrew** - Package manager for macOS dependencies
- **Tmux** - Terminal multiplexer for session management
- **Docker & Kubernetes** - Experimental container and orchestration configs

## 🚀 Quick Setup

### One-Line Installation

```bash
git clone https://github.com/yourusername/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
python3 scripts/setup.py
```

### What the Setup Script Does

The `setup.py` script handles the complete environment setup:

1. ✅ **Installs Xcode Command Line Tools** (if needed)
2. ✅ **Installs Homebrew** (if needed)
3. ✅ **Creates `~/.config` directory structure**
4. ✅ **Creates symlinks** for all configuration files
5. ✅ **Installs Homebrew packages** from `Brewfile`
6. ✅ **Sets Fish as default shell** (if not already)
7. ✅ **Verifies installation** of all tools

### Manual Installation

If you prefer to install manually:

```bash
# 1. Install Xcode CLT
xcode-select --install

# 2. Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 3. Create config directory
mkdir -p ~/.config

# 4. Create symlinks
ln -sf $(pwd)/ghostty ~/.config/ghostty
ln -sf $(pwd)/fish ~/.config/fish
ln -sf $(pwd)/starship ~/.config/starship
ln -sf $(pwd)/nvim ~/.config/nvim
ln -sf $(pwd)/tmux/tmux.conf ~/.tmux.conf
ln -sf $(pwd)/brewfile ~/.config/brewfile

# 5. Install packages
brew bundle install --file brewfile/Brewfile

# 6. Set Fish as default shell
chsh -s /opt/homebrew/bin/fish
```

## 📁 Repository Structure

```
dotfiles/
├── brewfile/
│   └── Brewfile
├── docker/
│   └── docker-compose.debug.yml
├── fish/
│   └── config.fish
├── ghostty/
│   └── config
├── k8s/
│   ├── base/
│   │   └── deployment.yaml
│   └── overlays/
│       └── dev/
│           └── patch-env.yaml
├── nvim/
│   ├── init.lua
│   └── lua/
│       ├── lsp.lua
│       └── test.lua
├── scripts/
│   ├── install.fish
│   └── install.sh
├── secrets/
│   └── README.md
├── starship/
│   └── starship.toml
├── tmux/
│   └── tmux.conf
├── .gitignore
└── README.md
```

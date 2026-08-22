if status is-interactive
    # Commands to run in interactive sessions can go here

    # Disable greeting
    set fish_greeting

    # Paths (Must be defined BEFORE mise activates)
    fish_add_path -g /opt/homebrew/bin
    fish_add_path -g $HOME/.local/bin
    fish_add_path -g /Users/robot/.lmstudio/bin
    
    # Global Binary Paths for Cargo and Bun binaries
    fish_add_path -g -a $HOME/.local/share/cargo/bin
    fish_add_path -g -a $HOME/.local/share/bun/bin

    # Starship prompt
    starship init fish | source

    # Mise Activation (Handles environments dynamically)
    mise activate fish | source

    # Editor
    set -Ux EDITOR nvim
    set -Ux VISUAL nvim

    # Aliases
    alias ll="eza -la --icons"
    alias ls="eza --icons"
    alias cat="bat -p"
    alias vim="nvim"
    alias g="git"

    # FZF integration
    fzf --fish | source
end

if test -n "$TMUX"
    set -gx TERM tmux-256color
else
    set -gx TERM xterm-256color
end

# Docker Aliases
alias d="docker"
alias dc="docker compose"
alias dcu="docker compose up"
alias dcd="docker compose down"
alias dcb="docker compose build"

# Homebrew Config
set -gx HOMEBREW_BUNDLE_FILE ~/.config/brewfile/Brewfile
set -gx HOMEBREW_NO_AUTO_UPDATE 1

# Python Settings
set -Ux PYTHONDONTWRITEBYTECODE 1
set -Ux PYTHONUNBUFFERED 1

# Rust / Cargo Settings (Mise isolation)
set -gx MISE_CARGO_HOME "$HOME/.local/share/cargo"
set -gx MISE_RUSTUP_HOME "$HOME/.local/share/rustup"

# Config Spec
set -gx XDG_CONFIG_HOME ~/.config

# Added by OrbStack: command-line tools and integration
source ~/.orbstack/shell/init2.fish 2>/dev/null || :


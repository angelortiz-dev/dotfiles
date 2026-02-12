if status is-interactive
# Commands to run in interactive sessions can go here

# Disable greeting
set fish_greeting

# Starship prompt
starship init fish | source

# Editor
set -Ux EDITOR nvim
set -Ux VISUAL nvim

# Paths
fish_add_path /opt/homebrew/bin
fish_add_path ~/.local/bin

# Aliases
alias ll="eza -la --icons"
alias ls="eza --icons"
alias cat="bat"
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

# Docker
alias d="docker"
alias dc="docker compose"
alias dcu="docker compose up"
alias dcd="docker compose down"
alias dcb="docker compose build"

set -gx HOMEBREW_BUNDLE_FILE ~/.config/brewfile/Brewfile
set -gx HOMEBREW_NO_AUTO_UPDATE 1

# Python
set -Ux PYTHONDONTWRITEBYTECODE 1
set -Ux PYTHONUNBUFFERED 1

# Ensure mise-managed versions are loaded (managed by scripts/setup_mise.py)
# >>> MISE INIT - managed by setup_mise.py
if type -q mise
  eval (mise env fish)
end
# <<< MISE INIT - managed by setup_mise.py

if status is-interactive
  set fish_greeting
  starship init fish | source
  direnv hook fish | source
end

set -Ux EDITOR nvim
set -Ux VISUAL nvim

fish_add_path /opt/homebrew/bin
fish_add_path ~/.local/bin

alias ll="eza -la --icons"
alias ls="eza --icons"
alias cat="bat"
alias vim="nvim"
alias g="git"

fzf --fish | source

if test -n "$TMUX"
  set -gx TERM tmux-256color
else
  set -gx TERM xterm-256color
end

if status is-interactive; and not set -q TMUX
  tmux attach -t main || tmux new -s main
end

# FastAPI
alias api="uv run uvicorn app.main:app --reload"
alias api-prod="uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"

# Vue
alias fe="npm run dev"
alias fe-build="npm run build"

# Docker
alias d="docker"
alias dc="docker compose"
alias dcu="docker compose up"
alias dcd="docker compose down"
alias dcb="docker compose build"

# uv
alias uvi="uv venv .venv"
alias uvd="uv sync"
alias uvr="uv run"

set -Ux PYTHONDONTWRITEBYTECODE 1
set -Ux PYTHONUNBUFFERED 1

source ~/.orbstack/shell/init2.fish 2>/dev/null || :

# pnpm
set -gx PNPM_HOME "/Users/coder/Library/pnpm"
if not string match -q -- $PNPM_HOME $PATH
  set -gx PATH "$PNPM_HOME" $PATH
end
# pnpm end

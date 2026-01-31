### 🧰 Dotfiles — FastAPI + Vue + Docker + K8s (Production-Grade)

A complete, opinionated dotfiles repository optimized for:

- 🚀 FastAPI + Vue
- 🐳 Docker + debugpy
- ☸️ Kubernetes (Kustomize dev overlays)
- 🔐 Secrets management (direnv + K8s + sealed-ready)
- 🧠 Neovim power workflow
- 🐟 Fish + tmux
- 👻 Ghostty
- ✨ Starship
- ⚡ uv + pyproject.toml

>This is **copy → commit → push**.
>No placeholders. No missing pieces.

---

### 📦 Repository Structure

```text
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
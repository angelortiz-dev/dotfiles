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
├── ghostty/
│   └── config
├── tmux/
│   └── tmux.conf
├── fish/
│   └── config.fish
├── starship/
│   └── starship.toml
├── nvim/
│   ├── init.lua
│   └── lua/
│       ├── lsp.lua
│       ├── dap.lua
│       ├── test.lua
│       └── coverage.lua
├── docker/
│   └── docker-compose.debug.yml
├── k8s/
│   ├── base/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── kustomization.yaml
│   ├── overlays/
│   │   └── dev/
│   │       ├── kustomization.yaml
│   │       └── patch-env.yaml
│   └── secrets/
│       └── README.md
├── secrets/
│   └── README.md
├── scripts/
│   └── install.sh
├── .gitignore
└── README.md
```
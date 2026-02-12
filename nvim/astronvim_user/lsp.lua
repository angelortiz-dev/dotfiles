local lsp = require("lspconfig")

-- Pyright config: strict type checking for Python projects (FastAPI/Django)
lsp.pyright.setup({
  settings = {
    python = {
      analysis = {
        typeCheckingMode = "strict",
      },
    },
  },
})

-- Ruff can be integrated separately (null-ls) if desired

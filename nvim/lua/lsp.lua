local lsp = require("lspconfig")

lsp.pyright.setup({
  settings = {
    python = {
      analysis = {
        typeCheckingMode = "strict",
      },
    },
  },
})

lsp.ruff.setup({})

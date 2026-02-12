-- AstroNvim user entrypoint copied from dotfiles
local M = {}

-- load plugins table if needed by AstroNvim
M.plugins = require("user.plugins")

-- LSP and neotest setup
require("user.mason")
require("user.lsp")
require("user.null_ls")
require("user.neotest")

return M

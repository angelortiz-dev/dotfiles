vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.expandtab = true
vim.opt.termguicolors = true
vim.opt.signcolumn = "yes"
vim.g.mapleader = " "

local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  { "nvim-lualine/lualine.nvim" },
  { "nvim-tree/nvim-tree.lua" },
  { "nvim-treesitter/nvim-treesitter", build = ":TSUpdate" },
  { "neovim/nvim-lspconfig" },
  { "mfussenegger/nvim-dap" },
  { "mfussenegger/nvim-dap-python" },
  { "nvim-neotest/neotest" },
  { "nvim-neotest/neotest-python" },
  { "andythigpen/nvim-coverage" },
  { "folke/tokyonight.nvim" },
})

vim.cmd.colorscheme("tokyonight")

require("lualine").setup()
require("nvim-tree").setup()
require("nvim-treesitter.configs").setup({ highlight = { enable = true } })

require("lsp")
require("dap")
require("test")
require("coverage")

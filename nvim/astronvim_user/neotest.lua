require("neotest").setup({
  adapters = {
    require("neotest-python")({
      runner = "pytest",
      -- Use system/project python; AstroNvim users often manage venvs per-project
      python = "python",
    }),
  },
})

vim.keymap.set("n", "<leader>tt", function() require("neotest").run.run() end)
vim.keymap.set("n", "<leader>tf", function() require("neotest").run.run(vim.fn.expand("%")) end)
vim.keymap.set("n", "<leader>to", function() require("neotest").output.open({ enter = true }) end)

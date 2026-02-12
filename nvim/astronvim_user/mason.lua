-- Ensure Mason-managed tools (pyright, ruff, black, isort) are installed
local ok_mason, mason = pcall(require, "mason")
if not ok_mason then
  vim.notify("mason.nvim not available; skipping tool installation", vim.log.levels.WARN)
  return
end

mason.setup()

local ok_registry, registry = pcall(require, "mason-registry")
if not ok_registry then
  vim.notify("mason-registry not available", vim.log.levels.WARN)
  return
end

local ensure_installed = { "pyright", "ruff", "black", "isort" }

for _, pkg_name in ipairs(ensure_installed) do
  local ok_has = registry.has_package(pkg_name)
  if not ok_has then
    -- attempt to refresh the registry and check again
    registry.refresh()
    ok_has = registry.has_package(pkg_name)
  end

  if not ok_has then
    vim.notify(string.format("Mason package not found: %s", pkg_name), vim.log.levels.WARN)
  else
    local pkg = registry.get_package(pkg_name)
    if not pkg:is_installed() then
      vim.notify(string.format("Installing Mason package: %s", pkg_name))
      pkg:install()
    end
  end
end

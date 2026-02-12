#!/usr/bin/env python3
"""Install AstroNvim and copy user config from this dotfiles repo.

Usage:
  python3 scripts/setup_astronvim.py [--yes]

This script will:
  - backup existing $XDG_CONFIG_HOME/nvim (if present)
  - clone https://github.com/AstroNvim/AstroNvim.git into $XDG_CONFIG_HOME/nvim
  - copy the contents of this repo's `nvim/astronvim_user/` into
    $XDG_CONFIG_HOME/nvim/lua/user
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path
import sys
import datetime


def abspath_repo_root() -> Path:
    # repo root is one level up from scripts/
    return Path(__file__).resolve().parents[1]


def get_paths(repo_root: Path):
    from os import environ
    xdg = Path(environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config")))
    nvim = xdg / "nvim"
    src = repo_root / "nvim" / "astronvim_user"
    dest_user = nvim / "lua" / "user"
    return xdg, nvim, src, dest_user


def backup_existing(nvim: Path):
    if nvim.exists():
        ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        backup = nvim.with_name(nvim.name + f".backup.{ts}")
        print(f"Backing up existing Neovim config: {nvim} -> {backup}")
        nvim.rename(backup)


def clone_astronvim(nvim: Path):
    print(f"Cloning AstroNvim into {nvim}")
    cmd = ["git", "clone", "--depth", "1", "https://github.com/AstroNvim/AstroNvim.git", str(nvim)]
    subprocess.check_call(cmd)


def install_user_config(src: Path, dest_user: Path):
    if not src.exists():
        raise SystemExit(f"User AstroNvim config not found at {src}")
    print(f"Copying user config from {src} to {dest_user}")
    dest_user.parent.mkdir(parents=True, exist_ok=True)
    # Copy contents of src into dest_user; allow overwrite
    for item in src.iterdir():
        target = dest_user / item.name
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    args = parser.parse_args()

    repo_root = abspath_repo_root()
    xdg, nvim, src, dest_user = get_paths(repo_root)

    print("This will install AstroNvim and copy your user config from this dotfiles repo.")
    if not args.yes:
        ans = input("Continue? [y/N] ")
        if ans.lower() != "y":
            print("Aborting.")
            sys.exit(0)

    backup_existing(nvim)
    clone_astronvim(nvim)
    install_user_config(src, dest_user)

    print("Done. Start Neovim to finish the first-run setup.")
    print(f"User config copied to: {dest_user}")


if __name__ == "__main__":
    main()

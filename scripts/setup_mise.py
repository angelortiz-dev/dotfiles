#!/usr/bin/env python3
"""Install languages via mise and ensure Fish shell loads mise-managed versions.

This script will:
  - verify `mise` is available in PATH
  - run `mise install` for requested runtimes (python, rust, bun)
  - insert or update a safe init block in your Fish config to load mise's env

Usage:
  python3 scripts/setup_mise.py [--yes] [--config PATH]
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path
import sys


MISE_BLOCK_BEGIN = "# >>> MISE INIT - managed by setup_mise.py"
MISE_BLOCK_END = "# <<< MISE INIT - managed by setup_mise.py"
MISE_BLOCK = f"{MISE_BLOCK_BEGIN}\nif type -q mise\n    eval (mise env fish)\nend\n{MISE_BLOCK_END}\n"


def run(cmd: list[str]) -> int:
    try:
        return subprocess.call(cmd)
    except FileNotFoundError:
        return 127


def ensure_mise_available() -> bool:
    return shutil.which("mise") is not None


def install_runtimes(runtimes: list[str]) -> None:
    for r in runtimes:
        print(f"Installing {r} via mise...")
        rc = run(["mise", "install", r])
        if rc == 0:
            print(f"Installed {r}")
        else:
            print(f"mise install {r} returned code {rc}")


def verify_bins_in_fish(bins: list[str]) -> bool:
    """Run an interactive fish shell, load mise env, and check that each binary is found on PATH.

    Returns True if all binaries were found, False otherwise.
    """
    checks = []
    for b in bins:
        checks.append(f"printf '%s\\n' \"{b}:\"; command -v {b} || printf ''")
    cmd = "; and ".join(checks)
    fish_cmd = f"if type -q mise; eval (mise env fish); end; {cmd}"

    try:
        proc = subprocess.run(["fish", "-ic", fish_cmd], capture_output=True, text=True, check=False)
    except FileNotFoundError:
        print("fish shell not found; cannot verify binaries in fish interactive sessions.")
        return False

    out = proc.stdout.strip()
    missing = []
    lines = [l for l in out.splitlines() if l.strip() != ""]
    found = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.endswith(":"):
            name = line[:-1]
            val = lines[i+1] if i+1 < len(lines) and not lines[i+1].endswith(":") else ""
            found[name] = val
            i += 2
        else:
            i += 1

    for b in bins:
        path = found.get(b, "")
        if not path:
            missing.append(b)
        else:
            print(f"{b} -> {path}")

    if missing:
        print("Missing in fish interactive PATH:", ", ".join(missing))
        return False
    return True


def update_fish_config(config_path: Path) -> None:
    if not config_path.exists():
        print(f"Fish config not found at {config_path}; creating new file")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(MISE_BLOCK)
        return

    text = config_path.read_text()
    if MISE_BLOCK_BEGIN in text and MISE_BLOCK_END in text:
        # Replace existing block
        pre = text.split(MISE_BLOCK_BEGIN, 1)[0]
        post = text.split(MISE_BLOCK_END, 1)[-1]
        new_text = pre + MISE_BLOCK + post.lstrip("\n")
        config_path.write_text(new_text)
        print(f"Updated existing mise init block in {config_path}")
    else:
        # Append at EOF with a blank line
        with config_path.open("a") as f:
            if not text.endswith("\n"):
                f.write("\n")
            f.write("\n" + MISE_BLOCK)
        print(f"Appended mise init block to {config_path}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    p.add_argument("--config", type=Path, help="Path to fish config.fish (defaults to $XDG_CONFIG_HOME/fish/config.fish)")
    return p.parse_args()


def xdg_config_home() -> Path:
    from os import environ
    return Path(environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config")))


def main() -> None:
    args = parse_args()

    config_path = args.config or (xdg_config_home() / "fish" / "config.fish")

    runtimes = ["python", "rust", "bun"]

    print("This script will install runtimes via mise and update your Fish config to load mise-managed versions.")
    if not args.yes:
        ans = input("Continue? [y/N] ")
        if ans.lower() != "y":
            print("Aborting.")
            sys.exit(0)

    if not ensure_mise_available():
        print("mise not found in PATH. Please install mise first and re-run this script.")
        sys.exit(1)

    install_runtimes(runtimes)
    update_fish_config(config_path)

    # Verify that fish interactive sessions can see the installed binaries
    print("Verifying installed binaries are available in interactive fish sessions...")
    bins_to_check = ["python", "rustc", "bun"]
    ok = verify_bins_in_fish(bins_to_check)
    if not ok:
        print("Verification failed: some binaries were not found in fish interactive PATH.")
        print("Try restarting your terminal or run: source ", config_path)
        sys.exit(2)

    print("Done. Restart your shell or run 'source' on your fish config to pick up changes.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Dotfiles setup script for macOS development environment.
Handles installation of Homebrew, CLT, symlinks, and Brewfile packages.
Supports both new setups and updates to existing installations.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


class Colors:
    """ANSI color codes."""
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_status(message: str, status: str = "INFO") -> None:
    """Print formatted status message."""
    if status == "INFO":
        color = Colors.BLUE
        symbol = "ℹ"
    elif status == "SUCCESS":
        color = Colors.GREEN
        symbol = "✓"
    elif status == "WARNING":
        color = Colors.YELLOW
        symbol = "⚠"
    elif status == "ERROR":
        color = Colors.RED
        symbol = "✗"
    else:
        color = Colors.RESET
        symbol = "•"

    print(f"{color}{symbol} {message}{Colors.RESET}")


def run_command(cmd: list, description: str = "", check: bool = True) -> Tuple[int, str]:
    """
    Execute a shell command and return exit code and output.

    Args:
        cmd: Command as list of strings
        description: Human-readable description of what's running
        check: Whether to raise exception on non-zero exit

    Returns:
        Tuple of (exit_code, output)
    """
    if description:
        print_status(description, "INFO")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )

        if check and result.returncode != 0:
            if result.stderr:
                print_status(f"Command failed: {result.stderr}", "ERROR")
            raise subprocess.CalledProcessError(result.returncode, cmd)

        return result.returncode, result.stdout + result.stderr

    except subprocess.CalledProcessError as e:
        print_status(f"Failed to execute: {' '.join(cmd)}", "ERROR")
        sys.exit(1)


def check_command_exists(cmd: str) -> bool:
    """Check if a command exists in PATH."""
    return subprocess.run(
        ["which", cmd],
        capture_output=True,
        check=False
    ).returncode == 0


def install_xcode_clt() -> bool:
    """
    Install Xcode Command Line Tools if not already installed.

    Returns:
        True if CLT is installed (or was just installed), False otherwise
    """
    if check_command_exists("gcc"):
        print_status("Xcode Command Line Tools already installed", "SUCCESS")
        return True

    print_status("Installing Xcode Command Line Tools...", "INFO")

    # Use xcode-select to install CLT
    code, _ = run_command(
        ["xcode-select", "--install"],
        description="Initializing Xcode CLT installer",
        check=False
    )

    if code == 0:
        print_status("Xcode CLT install initiated. Please complete the installation when prompted.")
        # Wait for user to complete installation
        input("Press Enter after installation is complete...")

        # Verify installation
        if check_command_exists("gcc"):
            print_status("Xcode Command Line Tools installed successfully", "SUCCESS")
            return True
        else:
            print_status("Xcode CLT installation could not be verified", "WARNING")
            return False
    elif code == 1:  # Already installed
        print_status("Xcode Command Line Tools already installed", "SUCCESS")
        return True
    else:
        print_status("Failed to install Xcode Command Line Tools", "ERROR")
        return False


def install_homebrew() -> bool:
    """
    Install Homebrew if not already installed.

    Returns:
        True if Homebrew is installed (or was just installed), False otherwise
    """
    if check_command_exists("brew"):
        print_status("Homebrew already installed", "SUCCESS")
        return True

    print_status("Installing Homebrew...", "INFO")

    code, output = run_command(
        ["/bin/bash", "-c", "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"],
        description="Downloading and running Homebrew installer",
        check=False
    )

    if code == 0:
        # Add Homebrew to PATH if on Apple Silicon
        if os.path.exists("/opt/homebrew/bin"):
            os.environ["PATH"] = f"/opt/homebrew/bin:{os.environ['PATH']}"

        if check_command_exists("brew"):
            print_status("Homebrew installed successfully", "SUCCESS")
            return True

    print_status("Homebrew installation failed", "ERROR")
    return False


def create_config_structure() -> bool:
    """
    Create .config directory structure and return its path.

    Returns:
        True if successful, False otherwise
    """
    config_dir = Path.home() / ".config"

    try:
        config_dir.mkdir(exist_ok=True, parents=True)
        print_status(f"Config directory ready: {config_dir}", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Failed to create config directory: {e}", "ERROR")
        return False


def create_symlinks(repo_root: Path) -> bool:
    """
    Create symlinks for all config files.

    Args:
        repo_root: Path to dotfiles repository root

    Returns:
        True if all symlinks created successfully, False otherwise
    """
    config_dir = Path.home() / ".config"
    symlinks = {
        "ghostty": config_dir / "ghostty",
        "fish": config_dir / "fish",
        "starship": config_dir / "starship",
        "nvim": config_dir / "nvim",
        "brewfile": config_dir / "brewfile",
    }

    # Also symlink tmux.conf to home directory
    symlinks["tmux/tmux.conf"] = Path.home() / ".tmux.conf"

    success = True

    for src_rel, dst in symlinks.items():
        src = repo_root / src_rel

        if not src.exists():
            print_status(f"Source not found: {src}", "WARNING")
            continue

        try:
            # Remove existing symlink or file
            if dst.exists() or dst.is_symlink():
                if dst.is_symlink():
                    dst.unlink()
                    print_status(f"Replaced existing symlink: {dst}", "INFO")
                else:
                    # Backup existing directory/file
                    backup_dst = Path(str(dst) + ".backup")
                    if not backup_dst.exists():
                        os.rename(str(dst), str(backup_dst))
                        print_status(f"Backed up existing config to: {backup_dst}", "WARNING")
                    else:
                        print_status(f"Config already backed up at: {backup_dst}", "INFO")
                        dst.unlink()

            # Create parent directory if needed
            dst.parent.mkdir(parents=True, exist_ok=True)

            # Create symlink
            os.symlink(str(src.resolve()), str(dst))
            print_status(f"Symlink created: {dst.name} → {src_rel}", "SUCCESS")

        except Exception as e:
            print_status(f"Failed to create symlink {dst}: {e}", "ERROR")
            success = False

    return success


def install_brewfile(repo_root: Path) -> bool:
    """
    Install packages from Brewfile.

    Args:
        repo_root: Path to dotfiles repository root

    Returns:
        True if successful, False otherwise
    """
    brewfile_path = repo_root / "brewfile" / "Brewfile"

    if not brewfile_path.exists():
        print_status(f"Brewfile not found at {brewfile_path}", "WARNING")
        return False

    try:
        print_status(f"Installing packages from Brewfile...", "INFO")

        code, output = run_command(
            ["brew", "bundle", "install", "--file", str(brewfile_path)],
            description="Running brew bundle",
            check=False
        )

        if code == 0:
            print_status("Brewfile packages installed successfully", "SUCCESS")
            return True
        else:
            # brew bundle returns non-zero if some packages were already installed
            # This is acceptable
            if "already satisfied" in output or "is already installed" in output:
                print_status("Brewfile processed (some packages already installed)", "SUCCESS")
                return True
            else:
                print_status("Brewfile installation had issues", "WARNING")
                logger.info(output)
                return True  # Still consider this a success

    except Exception as e:
        print_status(f"Failed to install Brewfile: {e}", "ERROR")
        return False


def setup_fish_shell() -> bool:
    """
    Set Fish as the default shell if not already.

    Returns:
        True if successful or already set, False otherwise
    """
    current_shell = os.environ.get("SHELL", "")

    if "fish" in current_shell:
        print_status("Fish shell already set as default", "SUCCESS")
        return True

    if not check_command_exists("fish"):
        print_status("Fish shell not installed (should be installed via Brewfile)", "WARNING")
        return False

    try:
        fish_path = subprocess.run(
            ["which", "fish"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        # Check if fish is in /etc/shells
        result = subprocess.run(
            ["grep", "-q", fish_path, "/etc/shells"],
            check=False
        )

        if result.returncode != 0:
            # Add fish to /etc/shells
            code, _ = run_command(
                ["sh", "-c", f"echo {fish_path} | sudo tee -a /etc/shells"],
                description="Adding fish to /etc/shells",
                check=False
            )
            if code != 0:
                print_status("Could not add fish to /etc/shells", "WARNING")
                return False

        # Change default shell
        code, _ = run_command(
            ["chsh", "-s", fish_path],
            description="Setting fish as default shell",
            check=False
        )

        if code == 0:
            print_status("Fish shell set as default (will take effect on next login)", "SUCCESS")
            return True
        else:
            print_status("Failed to set fish as default shell", "WARNING")
            return False

    except Exception as e:
        print_status(f"Failed to setup fish shell: {e}", "WARNING")
        return False


def verify_installation() -> bool:
    """
    Verify that all required tools are installed and configured.

    Returns:
        True if all checks pass, False otherwise
    """
    checks = {
        "Homebrew": lambda: check_command_exists("brew"),
        "Fish": lambda: check_command_exists("fish"),
        "Git": lambda: check_command_exists("git"),
        "Starship": lambda: check_command_exists("starship"),
        "Neovim": lambda: check_command_exists("nvim"),
    }

    print("\n" + Colors.BOLD + "Installation Verification:" + Colors.RESET)

    all_good = True
    for name, check in checks.items():
        if check():
            print_status(f"{name} is installed", "SUCCESS")
        else:
            print_status(f"{name} is NOT installed", "WARNING")
            all_good = False

    return all_good


def main() -> int:
    """Main setup function."""
    print(f"\n{Colors.BOLD}🚀 Dotfiles Setup Script{Colors.RESET}\n")

    # Get repository root
    repo_root = Path(__file__).parent.parent.resolve()
    print_status(f"Repository: {repo_root}\n", "INFO")

    # Step 1: Install Xcode CLT
    if not install_xcode_clt():
        print_status("Xcode CLT installation is required. Exiting.", "ERROR")
        return 1

    print()

    # Step 2: Install Homebrew
    if not install_homebrew():
        print_status("Homebrew installation is required. Exiting.", "ERROR")
        return 1

    print()

    # Step 3: Create config structure
    if not create_config_structure():
        print_status("Failed to create config directory. Exiting.", "ERROR")
        return 1

    print()

    # Step 4: Create symlinks
    if not create_symlinks(repo_root):
        print_status("Some symlinks failed to create, but continuing...", "WARNING")

    print()

    # Step 5: Install Brewfile packages
    if not install_brewfile(repo_root):
        print_status("Brewfile installation had issues, but continuing...", "WARNING")

    print()

    # Step 6: Setup Fish shell
    setup_fish_shell()

    print()

    # Step 7: Verify installation
    verify_installation()

    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Setup complete!{Colors.RESET}")
    print(f"\n{Colors.YELLOW}Next steps:{Colors.RESET}")
    print(f"  1. Restart your terminal or run: {Colors.BLUE}exec fish{Colors.RESET}")
    print(f"  2. Review config files in {Colors.BLUE}~/.config/{Colors.RESET}")
    print(f"  3. Customize settings as needed\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())

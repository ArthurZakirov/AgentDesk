# 📦 Parked dotfiles experiment

These files were moved out of the dotfiles repository so its active chezmoi scope can focus on zsh. This directory is an archive for review; it is not a chezmoi source directory and runs no installation hooks automatically.

The [installation hook](run_before_10-install-desktop-commander.sh), [LaunchAgent template](private_Library/private_LaunchAgents/com.arthur.desktop-commander-remote.plist.tmpl), and [launch hook](run_after_20-ensure-desktop-commander-launch-agent.sh) preserve the Desktop Commander setup. The [Claude pilot](dot_claude/CLAUDE.md) and [ignore rules](.chezmoiignore.tmpl) are preserved alongside it.

Inspect the archived files with `git ls-files experiments/parked-dotfiles`. Versions and runtime behavior are defined in those sources. Moving these sources does not unload the existing service or remove its installed plist.

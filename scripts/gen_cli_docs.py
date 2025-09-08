#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT
"""Generate CLI documentation from command tree JSON."""

import json
import subprocess
from pathlib import Path
from typing import Any

import mkdocs_gen_files  # type: ignore[import-untyped]

# Configuration
CLI_TREE_JSON_PATH = Path(__file__).parent.parent / "docs" / "templates" / "cli_tree.json"
OUTPUT_MD_PATH = "reference/cli.md"


def parse_cli_tree(cli_tree_json_path: Path) -> list[str]:
    """Parse CLI tree JSON and return flattened list of commands."""
    with open(cli_tree_json_path) as f:
        cli_tree: dict[str, Any] = json.load(f)

    commands: list[str] = []

    def walk(tree: dict[str, Any], prefix: str = "") -> None:
        for cmd, subcmds in tree.items():
            full_cmd = f"{prefix} {cmd}".strip() if prefix else cmd
            commands.append(full_cmd)
            if subcmds:
                subtree = {s: [] for s in subcmds} if isinstance(subcmds, list) else subcmds
                walk(subtree, full_cmd)

    walk(cli_tree)
    return commands


def run_help(command: str) -> str:
    """Run CLI command with --help and return formatted output."""
    result = subprocess.run([*command.split(), "--help"], capture_output=True, text=True, check=True)  # noqa: S603
    return f"```text\n{result.stdout.strip()}\n```\n"


def generate_cli_docs(cli_tree_json_path: Path) -> str:
    """Generate complete CLI documentation."""
    commands = parse_cli_tree(cli_tree_json_path)
    content = "# CLI Reference\n\n"

    for cmd in commands:
        content += f"## {cmd}\n\n{run_help(cmd)}\n"

    return content


def write_docs(content: str) -> None:
    """Write documentation to MkDocs."""
    with mkdocs_gen_files.open(OUTPUT_MD_PATH, "w") as f:
        f.write(content)


def main() -> None:
    """Generate CLI documentation."""
    content = generate_cli_docs(CLI_TREE_JSON_PATH)
    write_docs(content)


main()

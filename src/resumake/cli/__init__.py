# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

import typer

from resumake._version import __version__


def create_app() -> typer.Typer:
    app = typer.Typer(
        name="resumake",
        help="A simple CLI tool to generate resumes from structured data.",
        add_completion=True,
        no_args_is_help=True,
    )

    @app.callback(invoke_without_command=True)
    def main(
        version: bool = typer.Option(False, "--version", "-v", help="Show the application's version and exit."),
    ) -> None:
        """
        Resumake CLI — generate resumes with ease.
        """
        if version:
            typer.echo(f"resumake v{__version__}")
            raise typer.Exit

    return app

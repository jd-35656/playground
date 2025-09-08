# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT
from resumake.cli import create_app


def run() -> None:
    """Entry point for `python -m resumake`."""
    app = create_app()
    app()


if __name__ == "__main__":
    run()

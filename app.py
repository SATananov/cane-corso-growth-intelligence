"""One-line entry point for the Machine Learning Tools exercise alignment.

Usage:
    python app.py
    python app.py --config configs/machine_learning_tools_config.json
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.machine_learning_tools_pipeline import run_machine_learning_tools_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Step 21 Machine Learning Tools pipeline."
    )
    parser.add_argument(
        "--config",
        default="configs/machine_learning_tools_config.json",
        help="Path to a JSON configuration file, relative to the project root or absolute.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_machine_learning_tools_pipeline(Path(args.config))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# Author: Dennis Kendrick - denniskendrick@gmail.com
# Description: This should contain an overall description on what
#              this script performs.
#
# Primary Use Case: A fully functional and modular Python script skeleton for use in
#                   creating new scripts. This script is meant to be used as a
#                   template for creating new scripts.
#
# Usage:
#   This script accepts the following command-line arguments:
#   -c, --config PATH     : Path to a JSON config file to load
#   -f, --foo VALUE       : This is a generic placeholder to show how to add an option
#   -v, --verbose         : Enable verbose debug output
#   -n, --dry-run         : Show what would be done without actually doing it
#   --version             : Print version and exit
#
# Examples:
#   Basic execution:
#     ./python-skeleton.py --foo "bar_value"
#
#   With config file and verbose output:
#     ./python-skeleton.py --config myconfig.json --foo "test" --verbose
#
#   Dry run:
#     ./python-skeleton.py --dry-run --foo "testing"
#
# Config File (JSON):
#   The script loads a JSON config file via --config. Example myconfig.json:
#   {
#     "BAR": "custom value",
#     "debug_mode": true,
#     "max_retries": 3
#   }
#
# Logging:
#   Structured JSON is emitted to stdout. Diagnostics go to stdout via the
#   logger; raw data output (if any) should also go to stdout. Redirect in
#   the shell if you need to separate them.
#
# Execution:
#   uv run python python-skeleton.py --foo bar
#
# Prereqs: Ensure any prereqs are listed
#
# -------------------------------------------------------------------
# OPERATIONS - tasks that the script executes
#   - Runs the execute function
#   - execute then calls the bar function to show how to call a function
# -------------------------------------------------------------------

import json
import logging
import os
import shutil
import signal
import sys
import argparse
from pathlib import Path
from typing import Any, NoReturn

VERSION = "0.0.1"

# Setup logging — handlers are configured in configure_logging()
logger = logging.getLogger(__name__)

scriptname: str = Path(__file__).name

# Required binaries for the script to execute. Modify according to your needs.
REQUIRED_BINARIES: list[str] = ["which"]

#########################################################################
# Logging
#########################################################################


class JSONFormatter(logging.Formatter):
    """Emit log records as single-line JSON to stdout."""

    # Standard LogRecord attributes — excluded from extra field passthrough
    _std_attrs = frozenset(
        {
            "name",
            "msg",
            "args",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "stack_info",
            "lineno",
            "funcName",
            "created",
            "msecs",
            "relativeCreated",
            "thread",
            "threadName",
            "processName",
            "process",
            "message",
            "taskName",
        }
    )

    def format(self, record: logging.LogRecord) -> str:
        entry: dict[str, Any] = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Include any fields passed via extra={}
        for key, value in record.__dict__.items():
            if key not in self._std_attrs:
                entry[key] = value
        if record.exc_info:
            entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(entry)


#########################################################################
# Functions
#########################################################################


def execute(args: argparse.Namespace, config: dict[str, Any]) -> None:
    """Main execution function that runs the primary process."""
    if args.dry_run:
        logger.info("dry run: would execute", extra={"foo": args.foo})
        logger.info("dry run: would call bar()")
        return

    logger.info("executing — not yet implemented", extra={"foo": args.foo})
    bar(config)


def bar(config: dict[str, Any]) -> None:
    """Example function demonstrating config value access."""
    bar_value = config.get("BAR", "BAR not set")
    logger.debug("bar executed", extra={"BAR": bar_value})


#########################################################################
# UTILITY FUNCTIONS SECTION
#########################################################################


def check_prerequisites() -> None:
    """Check that all required binaries are available."""
    missing = [b for b in REQUIRED_BINARIES if not shutil.which(b)]
    if missing:
        logger.critical("missing required binaries", extra={"missing": missing})
        sys.exit(1)
    logger.debug("all prerequisites met")


def check_root() -> None:
    """Check the script is running as root."""
    if os.geteuid() != 0:
        errexit("this script must be run as root")


def errexit(message: str = "unknown error") -> NoReturn:
    """Exit with a fatal error message."""
    logger.critical(message)
    sys.exit(1)


def load_config(config_file: str) -> dict[str, Any]:
    """Load a JSON config file and return its contents."""
    path = Path(config_file)
    if not path.is_file():
        errexit(f"config file not found: {config_file}")
    try:
        with open(path) as f:
            data: dict[str, Any] = json.load(f)
        logger.info("config loaded", extra={"path": config_file})
        return data
    except json.JSONDecodeError as e:
        errexit(f"invalid JSON in config file: {e}")


def debug_env() -> None:
    """Log all environment variables for debugging."""
    for key, value in sorted(os.environ.items()):
        logger.debug("env", extra={"key": key, "value": value})


def signal_handler(signum: int, frame: Any) -> None:
    """Handle OS signals sent to the script."""
    names: dict[int, str] = {
        signal.SIGINT: "INT",
        signal.SIGTERM: "TERM",
        signal.SIGHUP: "HUP",
        signal.SIGQUIT: "QUIT",
        signal.SIGABRT: "ABRT",
        signal.SIGALRM: "ALRM",
    }
    name = names.get(signum, "UNKNOWN")
    if name in ("INT", "TERM", "QUIT", "ABRT"):
        logger.warning("terminated by signal", extra={"signal": name})
        sys.exit(1)
    elif name in ("HUP", "ALRM"):
        logger.warning("signal received", extra={"signal": name})
    else:
        errexit(f"terminating on unknown signal {signum}")


def setup_signal_handlers() -> None:
    """Register signal handlers for common OS signals."""
    for sig in [
        signal.SIGINT,
        signal.SIGTERM,
        signal.SIGHUP,
        signal.SIGQUIT,
        signal.SIGABRT,
        signal.SIGALRM,
    ]:
        signal.signal(sig, signal_handler)


def configure_logging(verbose: bool = False) -> None:
    """Configure structured JSON logging to stdout."""
    level = logging.DEBUG if verbose else logging.INFO
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logging.basicConfig(level=level, handlers=[handler])
    logger.setLevel(level)


def parse_arguments() -> tuple[argparse.ArgumentParser, argparse.Namespace]:
    """Parse command line arguments."""
    p = argparse.ArgumentParser(
        description="Python script skeleton",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    p.add_argument("-c", "--config", help="Path to a JSON config file")
    p.add_argument("-f", "--foo", help="Generic placeholder argument")
    p.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose debug output"
    )
    p.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Show what would be done without acting",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    args = p.parse_args()

    if args.config and not Path(args.config).exists():
        p.error(f"config file not found: {args.config}")

    return p, args


######################################################################
#  Start Script Execution
######################################################################


def main() -> int:
    try:
        _, args = parse_arguments()
        configure_logging(args.verbose)
        setup_signal_handlers()
        check_prerequisites()

        config: dict[str, Any] = {}
        if args.config:
            config = load_config(args.config)
        else:
            logger.debug("no config file specified, using defaults")

        # debug_env()  # uncomment to log all environment variables

        execute(args, config)
        logger.info("process completed successfully")
        return 0

    except KeyboardInterrupt:
        logger.warning("interrupted by user")
        return 1
    except Exception as e:
        logger.critical("unhandled exception", extra={"error": str(e)}, exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

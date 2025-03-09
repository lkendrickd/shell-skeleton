#!/usr/bin/env python3
# Author: Dennis Kendrick - denniskendrick@gmail.com
# Description: This should contain an overall description on what
#              this script performs.
#              
#
# Primary Use Case: A fully functional and modular Python script skeleton for use in
#                   creating new scripts. This script is meant to be used as a
#                   template for creating new scripts.
#
# Usage:
#   This script accepts the following command-line arguments:
#   -c, --config PATH     : Path to a config file to load
#   -f, --foo VALUE       : This is a generic placeholder to show how to add an option
#   -v, --verbose         : Enable verbose debug output
#   --log-file PATH       : Log to the specified file
#   --dry-run             : Show what would be done without actually doing it
#
# Examples:
#   Basic execution:
#     ./python-skeleton.py --foo "bar_value"
#
#   With config file and verbose output:
#     ./python-skeleton.py --config myconfig.py --foo "test" --verbose
#
#   Dry run with logging to file:
#     ./python-skeleton.py --dry-run --foo "testing" --log-file output.log
#
# Note on bar() function:
#   The bar() function is currently a placeholder function that demonstrates
#   how to call functions from the main execution flow. It should be renamed
#   and its logic reworked to achieve a specific task in your implementation.
#   For example, it could be renamed to process_data() and modified to process
#   input files or perform specific calculations.
#
# Config File:
#   The script can load a Python config file using the --config flag.
#   The config file should be a valid Python script that sets variables
#   which will be loaded into the global namespace.
#
#   Example config file (myconfig.py):
#   ```
#   # Configuration settings for python-skeleton.py
#   
#   # This value is accessed by the bar() function
#   BAR = "Custom BAR value from config"
#   
#   # Additional configuration variables can be added as needed
#   DEBUG_MODE = True
#   MAX_RETRIES = 3
#   LOG_LEVEL = "DEBUG"
#   OUTPUT_DIR = "/tmp/output"
#   ```
#
# Arguments Handling:
#   Command-line arguments are parsed using Python's argparse library in the 
#   parse_arguments() function. The resulting args object is used throughout 
#   the script to access argument values.
#
#   To add new command-line arguments:
#   1. Add a new parser.add_argument() line in the parse_arguments() function
#   2. Access your new argument via args.your_argument_name in other functions
#
# Environment Variables:
#   The script can access environment variables through os.environ dictionary.
#   Example usage:
#   ```
#   # Get an environment variable with a default if not set
#   api_key = os.environ.get('API_KEY', 'default_key')
#   
#   # Check if an environment variable exists
#   if 'DEBUG' in os.environ:
#       # Enable debug mode
#       configure_logging(verbose=True)
#   ```
#
#   The print_env() function (commented out in main()) can be used to print
#   all environment variables for debugging purposes.
#
# Error Handling:
#   This script implements comprehensive error handling including:
#   - Command line argument validation
#   - File operation error handling (config file, log file)
#   - Function-level try-except blocks for critical operations
#   - Global exception handling in main() to catch unexpected errors
#   - Proper error codes returned to the shell
#
#   When extending this script, follow these error handling practices:
#   1. Validate inputs before processing
#   2. Use try-except blocks around file operations and external calls
#   3. Log exceptions with appropriate log levels
#   4. Return meaningful error codes from main()
#
# Prereqs: Ensure any prereqs are listed
#
#-------------------------------------------------------------------
# OPERATIONS - tasks that the script executes
#   - Runs the execute function
#   - execute then calls the bar function to show how to call a function
#-------------------------------------------------------------------

import os
import sys
import signal
import argparse
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, NoReturn

# Setup logging
logger = logging.getLogger(__name__)

# Global Vars
scriptname: str = Path(__file__).name
parser: Optional[argparse.ArgumentParser] = None

# Required binaries for the script to execute. Modify according to your needs.
REQUIRED_BINARIES: List[str] = ["which"]

#########################################################################
# Functions
#########################################################################

def execute(args: argparse.Namespace) -> None:
    """Main execution function that runs the primary process"""
    try:
        if args.dry_run:
            logger.info("DRY RUN MODE: Showing what would be executed")
            logger.info(f"Would execute with FOO: {args.foo}")
            logger.info("Would call the bar function")
            return
        
        logger.info("Executing Processes - NOT YET IMPLEMENTED")
        logger.info(f"FOO: {args.foo}")
        bar()
    except Exception as e:
        logger.error(f"Error in execution process: {e}")
        raise

def bar() -> None:
    """Example function to show calling of a function from execute"""
    logger.debug("bar successfully executed")
    # Access BAR from globals explicitly
    global BAR
    bar_value: str = globals().get('BAR', 'BAR not set')
    logger.info(f"BAR: {bar_value}")

#########################################################################
# UTILITY FUNCTIONS SECTION - functions that perform utility tasks
#########################################################################

def check_prerequisites() -> None:
    """Checks for any prerequisite packages or binaries that need to be installed"""
    missing_counter: int = 0
    logger.debug("Checking for prerequisites...")

    for binary in REQUIRED_BINARIES:
        if not shutil.which(binary):
            logger.error(f"Missing required binary: {binary}")
            missing_counter += 1

    if missing_counter != 0:
        logger.critical(f"Error: {missing_counter} required binaries are missing.")
        sys.exit(1)

    logger.debug("All prerequisites are met.")

def check_root() -> None:
    """Checks if the script is being run as root"""
    if os.geteuid() != 0:
        errexit("This script must be run as root")

def errexit(message: str = "Unknown Error") -> NoReturn:
    """Function for exit due to fatal program error
    Accepts 1 arg: string containing descriptive error message"""
    logger.critical(f"{scriptname}: {message}")
    sys.exit(1)

def load_config(config_file: str) -> bool:
    """Loads the config file if it exists"""
    if os.path.isfile(config_file):
        try:
            # Use more explicit approach for clarity
            config_vars: Dict[str, Any] = {}
            with open(config_file) as f:
                exec(f.read(), globals())
            logger.info("Config file loaded")
            return True
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            errexit(f"Error loading config file: {e}")
    else:
        errexit("Config file not found")

def print_env() -> None:
    """Prints all environment variables usually for debugging"""
    for key, value in sorted(os.environ.items()):
        logger.debug(f"{key}={value}")

def signal_handler(signum: int, frame: Any) -> None:
    """Handles signals sent to the script"""
    signal_names: Dict[int, str] = {
        signal.SIGINT: "INT",
        signal.SIGTERM: "TERM",
        signal.SIGHUP: "HUP",
        signal.SIGQUIT: "QUIT",
        signal.SIGABRT: "ABRT",
        signal.SIGALRM: "ALRM"
    }
    
    signal_name: str = signal_names.get(signum, "UNKNOWN")
    
    if signal_name in ["INT", "TERM", "QUIT", "ABRT"]:
        logger.warning(f"{scriptname}: Program terminated by {signal_name} signal")
        sys.exit(1)
    elif signal_name == "HUP":
        logger.warning(f"{scriptname}: Hangup signal received")
    elif signal_name == "ALRM":
        logger.warning(f"{scriptname}: Alarm signal received")
    else:
        errexit(f"{scriptname}: Terminating on unknown signal")

def setup_signal_handlers() -> None:
    """Set up signal handlers for various signals"""
    for sig in [signal.SIGINT, signal.SIGTERM, signal.SIGHUP, 
                signal.SIGQUIT, signal.SIGABRT, signal.SIGALRM]:
        signal.signal(sig, signal_handler)

def usage() -> None:
    """Displays the usage of the script using the argparse help"""
    parser.print_help()

def configure_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level"""
    log_level: int = logging.DEBUG if verbose else logging.INFO
    
    try:
        # Configure root logger
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Set our module's logger level
        logger.setLevel(log_level)
    except Exception as e:
        print(f"ERROR: Failed to configure logging: {e}")
        sys.exit(1)

def parse_arguments() -> Tuple[argparse.ArgumentParser, argparse.Namespace]:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Python script skeleton",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("-c", "--config", help="Path to a config file to load")
    parser.add_argument("-f", "--foo", help="This is a generic placeholder to show how to add an option")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose debug output")
    parser.add_argument("--log-file", help="Log to the specified file")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without actually doing it")
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.config and not os.path.exists(args.config):
        parser.error(f"Config file not found: {args.config}")
    
    if args.log_file:
        log_dir = os.path.dirname(args.log_file)
        if log_dir and not os.path.exists(log_dir):
            parser.error(f"Log file directory does not exist: {log_dir}")
    
    return parser, args

######################################################################
#  Start Script Execution
######################################################################

def main() -> int:
    global parser
    
    try:
        # Parse command line arguments
        parser, args = parse_arguments()
        
        # Configure logging based on verbosity
        configure_logging(args.verbose)
        
        # Add file handler if log file is specified
        if args.log_file:
            try:
                file_handler: logging.FileHandler = logging.FileHandler(args.log_file)
                file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
                logger.addHandler(file_handler)
            except (IOError, PermissionError) as e:
                logger.error(f"Failed to create log file '{args.log_file}': {e}")
                return 1
        
        logger.debug("Starting script execution")
        
        # Set up signal handlers
        setup_signal_handlers()
        
        # Check for required prerequisites
        check_prerequisites()
        
        # Check if config was passed in and set
        if args.config:
            try:
                config: bool = load_config(args.config)
                # You might want to add globals or do something with the config here
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                return 1
        else:
            logger.info("No config file passed in, using default")
        
        # Uncomment below to debug the script environment variables
        # print_env()
        
        # Execute main function
        try:
            execute(args)
        except Exception as e:
            logger.error(f"Error in main execution: {e}")
            return 1
        
        logger.info("Process completed successfully.")
        return 0
        
    except KeyboardInterrupt:
        logger.warning("Script execution interrupted by user")
        return 1
    except Exception as e:
        # Global exception handler for unexpected errors
        logger.critical(f"Unhandled exception: {e}")
        logger.debug("Exception details:", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
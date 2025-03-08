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
# Execution:
# 
# ./python-skeleton.py --foo FOO
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

# Setup logging
logger = logging.getLogger(__name__)

# Global Vars
scriptname = Path(__file__).name

# Required binaries for the script to execute. Modify according to your needs.
REQUIRED_BINARIES = ["which"]

#########################################################################
# Functions
#########################################################################

def execute(args):
    """Main execution function that runs the primary process"""
    if args.dry_run:
        logger.info("DRY RUN MODE: Showing what would be executed")
        logger.info(f"Would execute with FOO: {args.foo}")
        logger.info("Would call the bar function")
        return
    
    logger.info("Executing Processes - NOT YET IMPLEMENTED")
    logger.info(f"FOO: {args.foo}")
    bar()

def bar():
    """Example function to show calling of a function from execute"""
    logger.debug("bar successfully executed")
    # Access BAR from globals explicitly
    global BAR
    bar_value = globals().get('BAR', 'BAR not set')
    logger.info(f"BAR: {bar_value}")

#########################################################################
# UTILITY FUNCTIONS SECTION - functions that perform utility tasks
#########################################################################

def check_prerequisites():
    """Checks for any prerequisite packages or binaries that need to be installed"""
    missing_counter = 0
    logger.debug("Checking for prerequisites...")

    for binary in REQUIRED_BINARIES:
        if not shutil.which(binary):
            logger.error(f"Missing required binary: {binary}")
            missing_counter += 1

    if missing_counter != 0:
        logger.critical(f"Error: {missing_counter} required binaries are missing.")
        sys.exit(1)

    logger.debug("All prerequisites are met.")

def check_root():
    """Checks if the script is being run as root"""
    if os.geteuid() != 0:
        errexit("This script must be run as root")

def errexit(message="Unknown Error"):
    """Function for exit due to fatal program error
    Accepts 1 arg: string containing descriptive error message"""
    logger.critical(f"{scriptname}: {message}")
    sys.exit(1)

def load_config(config_file):
    """Loads the config file if it exists"""
    if os.path.isfile(config_file):
        try:
            # Use more explicit approach for clarity
            config_vars = {}
            with open(config_file) as f:
                exec(f.read(), globals())
            logger.info("Config file loaded")
            return True
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            errexit(f"Error loading config file: {e}")
    else:
        errexit("Config file not found")

def print_env():
    """Prints all environment variables usually for debugging"""
    for key, value in sorted(os.environ.items()):
        logger.debug(f"{key}={value}")

def signal_handler(signum, frame):
    """Handles signals sent to the script"""
    signal_names = {
        signal.SIGINT: "INT",
        signal.SIGTERM: "TERM",
        signal.SIGHUP: "HUP",
        signal.SIGQUIT: "QUIT",
        signal.SIGABRT: "ABRT",
        signal.SIGALRM: "ALRM"
    }
    
    signal_name = signal_names.get(signum, "UNKNOWN")
    
    if signal_name in ["INT", "TERM", "QUIT", "ABRT"]:
        logger.warning(f"{scriptname}: Program terminated by {signal_name} signal")
        sys.exit(1)
    elif signal_name == "HUP":
        logger.warning(f"{scriptname}: Hangup signal received")
    elif signal_name == "ALRM":
        logger.warning(f"{scriptname}: Alarm signal received")
    else:
        errexit(f"{scriptname}: Terminating on unknown signal")

def setup_signal_handlers():
    """Set up signal handlers for various signals"""
    for sig in [signal.SIGINT, signal.SIGTERM, signal.SIGHUP, 
                signal.SIGQUIT, signal.SIGABRT, signal.SIGALRM]:
        signal.signal(sig, signal_handler)

def usage():
    """Displays the usage of the script using the argparse help"""
    parser.print_help()

def configure_logging(verbose=False):
    """Configure logging based on verbosity level"""
    log_level = logging.DEBUG if verbose else logging.INFO
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Set our module's logger level
    logger.setLevel(log_level)

def parse_arguments():
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
    
    return parser, parser.parse_args()

######################################################################
#  Start Script Execution
######################################################################

def main():
    global parser
    
    # Parse command line arguments
    parser, args = parse_arguments()
    
    # Configure logging based on verbosity
    configure_logging(args.verbose)
    
    # Add file handler if log file is specified
    if args.log_file:
        file_handler = logging.FileHandler(args.log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)
    
    logger.debug("Starting script execution")
    
    # Set up signal handlers
    setup_signal_handlers()
    
    # Check for required prerequisites
    check_prerequisites()
    
    # Check if config was passed in and set
    if args.config:
        config = load_config(args.config)
        # You might want to add globals or do something with the config here
    else:
        logger.info("No config file passed in, using default")
    
    # Uncomment below to debug the script environment variables
    # print_env()
    
    # Execute main function
    execute(args)
    
    logger.info("Process completed successfully.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

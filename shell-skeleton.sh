#!/bin/sh
set -eu
# Author: Dennis Kendrick - denniskendrick@gmail.com
# Description: This should contain an overall description on what
#              this script performs.
#              
#
# Primary Use Case: A fully functional and modular sh script skeleton for use in
#                   creating new scripts. This script is meant to be used as a
#                   template for creating new scripts.
#
# Usage:
#   This script accepts the following command-line arguments:
#   -h, --help            : Display usage
#   -v, --verbose         : Enable verbose output
#   -n, --dry-run         : Show what would be done without acting
#   -c, --config PATH     : Path to a shell config file to source
#   -f, --foo VALUE       : Generic placeholder to show how to add an option
#   --version             : Print version and exit
#
# Examples:
#   Basic execution:
#     ./shell-skeleton.sh --foo bar
#
#   With config and verbose:
#     ./shell-skeleton.sh --config myconfig.sh --foo test --verbose
#
#   Dry run:
#     ./shell-skeleton.sh --dry-run --foo testing
#
# Prereqs: Ensure any prereqs are listed
#
#-------------------------------------------------------------------
# OPERATIONS - tasks that the script executes
#   - Runs the execute function
#   - execute then calls the bar function to show how to call a function
#-------------------------------------------------------------------
# Global Vars
#-------------------------------------------------------------------
scriptname="$(basename "$0")"
VERSION="0.0.1"

# Required binaries for the script to execute. Modify according to your needs.
REQUIRED_BINARIES="which"

# Default verbose logging off; enable with -v/--verbose
VERBOSE=0
DRY_RUN=0

# Optional arguments — default to empty
CONFIG=""
FOO=""

#########################################################################
# Functions
#########################################################################

# execute - main execution function
execute() {
    if [ "${DRY_RUN}" -eq 1 ]; then
        verbose "dry run: would execute with FOO=${FOO}"
        verbose "dry run: would call bar"
        return
    fi
    echo "Executing Processes - NOT YET IMPLEMENTED"
    echo "FOO: $FOO"
    bar
}

# bar - is here to show calling of a function from execute
bar() {
    verbose "bar successfully executed"
}

#########################################################################
# UTILITY FUNCTIONS SECTION - functions that perform a utility tasks
#########################################################################

# check_prerequsites - checks for any prerequsites packages or binaries that need installed
check_prerequisites() {
    missing_counter=0
    verbose "Checking for prerequisites..."

    old_ifs="$IFS"
    IFS=':'
    for bin in $REQUIRED_BINARIES; do
        if ! type "$bin" > /dev/null 2>&1; then
            echo "Missing required binary: $bin" >&2
            missing_counter=$((missing_counter + 1))
        fi
    done
    IFS="$old_ifs"

    if [ "$missing_counter" -ne 0 ]; then
        echo "Error: $missing_counter required binaries are missing." >&2
        exit 1
    fi

    verbose "All prerequisites are met."
}

# check_root - checks if the script is being run as root
check_root() {
    if [ "$(id -u)" != "0" ]; then
        errexit "This script must be run as root"
    fi
}

# errexit - message and exit the script
errexit() {
    # Function for exit due to fatal program error
    # Accepts 1 arg: string containing descriptive error message
    echo "${scriptname}: ${1:-"Unknown Error"}" >&2
    exit 1
}

# load_config - sources a shell config file
# WARNING: sources file as shell — ensure trusted input
load_config() {
    if [ -f "${CONFIG}" ]; then
        # shellcheck disable=SC1090
        . "${CONFIG}"
        verbose "Config file loaded"
    else
        errexit "Config file not found"
    fi
}

# debug_env - prints all environment variables for debugging
debug_env() {
    env | sort
}

# signal_exit - handles signals sent to the script
signal_exit() {
    case "$1" in
        INT)
            echo "${scriptname}: Program aborted by user" >&2
            exit;;
        TERM)
            echo "${scriptname}: Program terminated" >&2
            exit;;
        HUP)
            echo "${scriptname}: Hangup signal received" >&2
            ;;
        QUIT)
            echo "${scriptname}: Quit signal received" >&2
            exit;;
        ABRT)
            echo "${scriptname}: Abort signal received" >&2
            exit;;
        ALRM)
            echo "${scriptname}: Alarm signal received" >&2
            ;;
        *)
            errexit "${scriptname}: Terminating on unknown signal";;
    esac
}

# usage - displays the usage of the script
usage() {
    echo "Usage: $scriptname [OPTIONS]"
    echo
    echo "Options:"
    echo "  -h, --help      Display this help"
    echo "  -v, --verbose   Enable verbose output"
    echo "  -n, --dry-run   Show what would be done without acting"
    echo "  -c, --config    Path to a shell config file to source"
    echo "  -f, --foo       Generic placeholder to show how to add an option"
    echo "  --version       Print version and exit"
    echo
    echo "Example: ./$scriptname --foo foovalue"
}

# verbose - prints a verbose message
verbose() {
    if [ "${VERBOSE}" -eq 1 ]; then
        echo "[INFO]: ${1}" >&2
    fi
}

######################################################################
#  Start Script Execution
######################################################################

# Trap various signals
trap "signal_exit TERM" TERM HUP
trap "signal_exit INT"  INT
trap "signal_exit QUIT" QUIT
trap "signal_exit ABRT" ABRT
trap "signal_exit ALRM" ALRM

# This loop will parse the command line arguments add or remove for your needs.
while [ "$#" -gt 0 ]; do
    case "$1" in
        -h|--help)
            usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=1
            shift
            ;;
        -n|--dry-run)
            DRY_RUN=1
            shift
            ;;
        --version)
            echo "$scriptname $VERSION"
            exit 0
            ;;
        -c|--config)
            CONFIG="$2"
            shift 2
            ;;
        -f|--foo)
            FOO="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# check for required prereqs
check_prerequisites

# Uncomment the following line if the script requires root privileges
# check_root

# check is CONFIG was passed in and set
if [ -z "${CONFIG}" ]; then
    verbose "No config file passed in, using default"
else
    load_config
fi

# Uncomment below to debug the script environment variables
#debug_env

execute
verbose "Process completed successfully."
exit 0
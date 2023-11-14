
# Bash Script Skeleton

![Bash Script Skeleton Logo](images/bashskel.webp)

## Description
This bash script provides a robust starting point for creating new bash scripts. It is designed to be modular and easily extendable, making it ideal for a wide range of scripting tasks. This is particularly useful for CI tasks in a CI/CD environment.

## Features
- Command line options parsing
- Config file support
- Prerequisite binary checks
- Verbose logging
- Signal handling
- Templated functions for common tasks

## Usage
By default, you can run the script with the following command:
```bash
./bash-skeleton.sh --foo [value] --config /path/to/config
```
**NOTE**: You may need to chmod the script.

```
chmod +x bash-skeleton.sh
```

### Options
- `-c`, `--config`: Specify the path to the environment configuration file.
- `-h`, `--help`: Display the help message and exit.
- `-f`, `--foo`: An example flag to demonstrate usage.

### Adding New Functions
To extend the script's functionality:
1. Define new functions in the Functions section.
2. If needed, add new command line options in the `getopt` command and handle them in the option parsing loop.

### Modifying Prerequisites
The script checks for required binaries before execution. To modify the prerequisites:
1. Update the `REQUIRED_BINARIES` array at the top of the script with the names of the binaries your script requires.

## Development
- The script is designed to be modular. Add new functions and features as needed.
- It's recommended to test new changes in a controlled environment before deployment.

## Contributions
Contributions to improve this script are welcome. Please adhere to best practices for bash scripting.


# Shell Script Skeleton

![Shell Script Skeleton Logo](images/shellskel.webp)

## Description
This shell script provides a robust starting point for creating new sh scripts. It is designed to be modular and easily extendable, making it ideal for a wide range of scripting tasks. This is particularly useful for CI tasks in a CI/CD environment.  The goal is to have a single script that can be used for multiple tasks that is uniform and easy to maintain.

## Features
- Command line options parsing
- Config file support
- Prerequisite binary checks
- Verbose logging
- Signal handling
- Templated functions for common tasks

## Usage
By default, you can run the script with the following command and the --config to a config file is COMPLETELY OPTIONAL:
```sh
./shell-skeleton.sh --foo [value] --config /path/to/config
```
**NOTE**: You may need to chmod the script.

```sh
chmod +x shell-skeleton.sh
```

## Config

There is a sample config.env file included to show the format of the file.  Again this is completely optional and you can pass in the values via the command line.

### Options
- `-c`, `--config`: Specify the path to the environment configuration file.
- `-h`, `--help`: Display the help message and exit.
- `-f`, `--foo`: An example flag to demonstrate usage.

### Adding New Functions
To extend the script's functionality:
1. Define new functions in the Functions section.
2. If needed, add new command line options in the while options loop.

### Modifying Prerequisites
The script checks for required binaries before execution. To modify the prerequisites:
1. Update the `REQUIRED_BINARIES` at the top of the script with the names of the binaries your script requires.

### Docker Support

The script can be run in a Docker container. To build the container:
```sh
docker build . -t shell-skeleton:latest
```

To run the container:

```sh
docker run -it -v /path/to/local/config:/path/in/container/config shell-skeleton:latest --config /path/in/container/config --foo your_value 
```

## Python Script Skeleton
The Python version offers the same core functionality as the shell script, with additional features and a more structured approach using Python's libraries. This was created because python is just so widely used.

### Usage
Run the Python script with the following command:
```sh
pypython3 pythonskel.py --foo [value] --config /path/to/config.py
```

**Config**
The Python version uses a Python file for configuration.
- Example config.py:
```python
# config.py
BAR = "This value comes from the config file"
# Add other configuration variables as needed
```

### Options
-c, --config: Specify the path to the Python configuration file.
-h, --help: Display the help message and exit.
-f, --foo: An example flag to demonstrate usage.
-v, --verbose: Enable verbose (debug) logging.
--log-file: Specify a file to write logs to.
--dry-run: Show what would be done without actually performing operations.

## Development
- The script is designed to be modular. Add new functions and features as needed.
- It's recommended to test new changes in a controlled environment before deployment.

## Contributions
Contributions to improve this script are welcome. Please adhere to best practices for shell scripting.

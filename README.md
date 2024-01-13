# Conntrack_Wizard

The Conntrack Wizard simplifies conntrack command execution, offering an interactive interface for users to effortlessly manage and analyze connection tracking data. With source and destination input, diverse conntrack commands, and output storage, it enhances efficiency in monitoring and manipulating connection tracking information.


Let's break down the "Conntrack Wizard" script step by step:

Import Necessary Modules:

import subprocess
import os
These modules are used for running shell commands and interacting with the operating system.

Define Execution Function:

def execute_conntrack(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
A function to execute the conntrack command and capture its output or handle errors.

Define Save to File Function:

def save_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
A function to save content to a file.

Define User Input Function:

def get_user_input(prompt):
    return input(prompt).strip()
A function to get user input with a prompt.

Define Main Function:

def main():
    # Get user input for source and destination IP addresses
    src_ip = get_user_input("Enter source IP address: ")
    dst_ip = get_user_input("Enter destination IP address: ")

    # Construct the filename
    filename = f"/var/conntrack_{src_ip}_{dst_ip}.capture"

    while True:
        # Display Conntrack menu
        print("\nConntrack Menu:")
        # (Options 1-10 and Exit)
        choice = get_user_input("Enter your choice (0-10): ")
        # Get additional parameters/options based on the chosen command
        additional_options = get_user_input("Enter additional parameters/options (if any): ")

        # Construct the Conntrack command
        conntrack_command = f"conntrack -{choice} -s {src_ip} -d {dst_ip} {additional_options}"

        # Execute Conntrack command
        result = execute_conntrack(conntrack_command)

        # Save the result to the file
        save_to_file(filename, result)

        print(f"Command executed. Output saved to {filename}")

if __name__ == "__main__":
    main()

#The main function orchestrates the script execution by getting user input for source and destination IP addresses and providing a menu for various conntrack commands. It then constructs and executes the chosen conntrack command with user-provided parameters.

#Script Summary: The script acts as a user-friendly interface for conntrack commands, allowing users to interactively select and execute various commands to inspect or manipulate connection tracking information. It prompts the user for source and destination IP addresses, provides a menu of conntrack commands, and executes the chosen command with additional parameters. The output is saved to a file for further analysis.

#Purpose: The purpose of the script is to simplify the usage of conntrack commands for monitoring and managing connection tracking information. It provides an interactive and user-friendly way to perform various conntrack operations, allowing users to explore and analyze connection tracking data efficiently. The script facilitates customization of conntrack commands and helps users save the command output for future reference or analysis.

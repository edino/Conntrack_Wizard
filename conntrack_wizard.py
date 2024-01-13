# Copyright
# Original author: Edino De Souza
# Repository: https://github.com/edino/Conntrack_Wizard
# License: GPL-3.0 license - https://github.com/edino/TCPFlagsSender/tree/main?tab=GPL-3.0-1-ov-file

#Script Summary: The script acts as a user-friendly interface for conntrack commands, allowing users to interactively select and execute various commands to inspect or manipulate connection tracking information. It prompts the user for source and destination IP addresses, provides a menu of conntrack commands, and executes the chosen command with additional parameters. The output is saved to a file for further analysis.

#Purpose: The purpose of the script is to simplify the usage of conntrack commands for monitoring and managing connection tracking information. It provides an interactive and user-friendly way to perform various conntrack operations, allowing users to explore and analyze connection tracking data efficiently. The script facilitates customization of conntrack commands and helps users save the command output for future reference or analysis.

# BuildDate: 5:53 PM EST 2024-01-13

# A simple way to execute this script is using the following command: curl -s https://raw.githubusercontent.com/edino/TCPFlagsSender/main/conntrack_wizard.py | python3 -

import subprocess
import os

def execute_conntrack(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def save_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def get_user_input(prompt):
    return input(prompt).strip()

def main():
    # Get user input for source and destination IP addresses
    src_ip = get_user_input("Enter source IP address: ")
    dst_ip = get_user_input("Enter destination IP address: ")

    # Construct the filename
    filename = f"/var/conntrack_{src_ip}_{dst_ip}.capture"

    while True:
        # Conntrack menu
        print("\nConntrack Menu:")
        print("\n1. List conntrack or expectation table")
        print("\n2. Get conntrack or expectation")
        print("\n3. Delete conntrack or expectation")
        print("\n4. Reclaim conntrack")
        print("\n5. Create a conntrack or expectation")
        print("\n6. Update a conntrack")
        print("\n7. Show events")
        print("\n8. Flush table")
        print("\n9. Show counter")
        print("\n10. Show statistics")
        print("\n0. Exit")

        choice = get_user_input("Enter your choice (0-10): ")

        if choice == '0':
            break

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

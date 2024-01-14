# Copyright
# Original author: Edino De Souza
# Repository: https://github.com/edino/Conntrack_Wizard
# License: GPL-3.0 license - https://github.com/edino/TCPFlagsSender/tree/main?tab=GPL-3.0-1-ov-file

#Script Summary: The script acts as a user-friendly interface for conntrack commands, allowing users to interactively select and execute various commands to inspect or manipulate connection tracking information. It prompts the user for source and destination IP addresses, provides a menu of conntrack commands, and executes the chosen command with additional parameters. The output is saved to a file for further analysis.

#Purpose: The purpose of the script is to simplify the usage of conntrack commands for monitoring and managing connection tracking information. It provides an interactive and user-friendly way to perform various conntrack operations, allowing users to explore and analyze connection tracking data efficiently. The script facilitates customization of conntrack commands and helps users save the command output for future reference or analysis.

# BuildDate: 10:18 PM EST 2024-01-13

# A simple way to execute this script is using the following command: curl -s https://raw.githubusercontent.com/edino/TCPFlagsSender/main/conntrack_wizard.py | python3 -

import re
import subprocess
import threading

def validate_ip(ip):
    # Regular expression for a valid IP address
    ip_regex = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')

    # Check if the provided IP matches the regex
    if ip_regex.match(ip):
        # Further validate each octet
        octets = ip.split('.')
        for octet in octets:
            if not 0 <= int(octet) <= 255:
                return False
        return True
    else:
        return False

def run_conntrack_command(conntrack_command, src_ip=None, dst_ip=None, output_directory="/var"):
    filename_placeholder = ""
    
    if src_ip:
        filename_placeholder += f"_src-{src_ip}"
    if dst_ip:
        filename_placeholder += f"_dst-{dst_ip}"
    
    filename_placeholder = filename_placeholder.lstrip('_')
    output_filename = f"{output_directory}/conntrack_{filename_placeholder}.capture"

    command = ['conntrack', f'-{conntrack_command}']

    if src_ip:
        command.extend(['-s', src_ip])
    if dst_ip:
        command.extend(['-d', dst_ip])

    try:
        with open(output_filename, 'a') as output_file:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Function to handle KeyboardInterrupt
            def handle_interrupt():
                try:
                    process.communicate()
                except KeyboardInterrupt:
                    print("\nScript interrupted by user.")
                    process.terminate()
                    process.wait()

            # Start the thread to check for KeyboardInterrupt
            interrupt_thread = threading.Thread(target=handle_interrupt)
            interrupt_thread.start()

            # Read and print the output of the command
            for line in process.stdout:
                print(line, end='')
                output_file.write(line)

            # Wait for the process to finish
            process.wait()

            # Join the thread to ensure it has completed
            interrupt_thread.join()

            print(f"Command executed successfully. Output appended to {output_filename}")

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

def main():
    conntrack_commands = {
        'L': 'List connection tracking or expectation table',
        'G': 'Search for and show a particular (matching) entry in the given table',
        'D': 'Delete an entry from the given table',
        'R': 'Reclaim conntrack',
        'I': 'Create a new entry from the given table',
        'U': 'Update an entry from the given table',
        'E': 'Display a real-time event log',
        'F': 'Flush the whole given table',
        'C': 'Show the table counter',
        'S': 'Show the in-kernel connection tracking system statistics',
    }

    print("Available conntrack commands:")
    for key, value in conntrack_commands.items():
        print(f"{key}: {value}")

    try:
        conntrack_command = input("Enter conntrack command: ").upper()

        if conntrack_command not in conntrack_commands:
            print("\nInvalid conntrack command.")
            return

        src_ip = input("\nEnter source IP address (press Enter to skip): ")
        dst_ip = input("\nEnter destination IP address (press Enter to skip): ")

        if src_ip and not validate_ip(src_ip):
            print("\nInvalid source IP address.")
            return
        if dst_ip and not validate_ip(dst_ip):
            print("\nInvalid destination IP address.")
            return

        output_directory = input("\nEnter the directory where the file will be saved (press Enter for default /var): ") or "/var"

        run_conntrack_command(conntrack_command, src_ip, dst_ip, output_directory)

    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
        return

if __name__ == "__main__":
    main()

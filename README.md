# Conntrack_Wizard

The Conntrack Wizard simplifies conntrack command execution, offering an interactive interface for users to effortlessly manage and analyze connection tracking data. With source and destination input, diverse conntrack commands, and output storage, it enhances efficiency in monitoring and manipulating connection tracking information.

Let's break down the "ConntrackWizard.py" script step by step:

Import Necessary Modules:

python
Copy code
import subprocess
import os
These modules are used for running shell commands and handling the file system.

User Input for IP Addresses:

python
Copy code
src_ip = input("Enter source IP address: ")
dst_ip = input("Enter destination IP address: ")
The script prompts the user to enter the source and destination IP addresses.

Construct File Name:

python
Copy code
filename = f"/var/conntrack_{src_ip}_{dst_ip}.capture"
Constructs a filename based on the provided source and destination IP addresses.

Conntrack Command Construction:

python
Copy code
conntrack_command = [
    "conntrack", "-L",  # List conntrack table
    "--src", src_ip,  # Set source IP
    "--dst", dst_ip,  # Set destination IP
    "--output", "xml",  # Output format
]
Constructs the conntrack command with options based on user input.

Execute Conntrack Command:

python
Copy code
result = subprocess.run(conntrack_command, stdout=subprocess.PIPE, text=True)
Executes the conntrack command, capturing the output.

Write to File:

python
Copy code
with open(filename, "w") as file:
    file.write(result.stdout)
Writes the conntrack information to a file with the constructed filename.

Display File Path:

python
Copy code
print(f"Conntrack information saved to: {filename}")
Informs the user about the path where the conntrack information is saved.

Script Summary:
The script takes user input for source and destination IP addresses, constructs a filename based on these IPs, runs the conntrack command with the provided IPs, and saves the output to a file. The file is stored in /var/conntrack_sourceIP_destinationIP.capture.

Purpose:
The purpose of the script is to provide a user-friendly interface to gather and save connection tracking information (conntrack) between a specified source and destination IP address. It simplifies the process of running conntrack commands and organizing the captured data in a file for later reference or analysis.

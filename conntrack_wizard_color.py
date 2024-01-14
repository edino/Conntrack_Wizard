import subprocess
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama

def execute_conntrack(command, verbose=False):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, shell=True)
        output = result.stdout
        if verbose:
            print_colored_output(output)
        return output
    except subprocess.CalledProcessError as e:
        return f"Error: {Fore.RED}{e.stderr}"

def print_colored_output(output):
    # Split output by lines and add color to specific sections
    for line in output.splitlines():
        if "SRC=" in line or "DST=" in line:
            print(Fore.GREEN + line)
        elif "PROTO=" in line:
            print(Fore.BLUE + line)
        else:
            print(line)

def save_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def get_user_input(prompt):
    return input(prompt).strip()

def display_menu(menu_options):
    print("\nMenu:")
    for option in menu_options:
        print(f"{option} - {menu_options[option]}")

def select_menu_option(menu_options, prompt):
    while True:
        display_menu(menu_options)
        choice = get_user_input(prompt)
        if choice in menu_options:
            return choice
        elif choice.lower() == 's':
            return 'skip'
        elif choice.lower() == 'e':
            return 'execute'
        else:
            print("Invalid choice. Please enter a valid option.")

def ask_for_ip_options():
    ip_option = get_user_input("Do you want to provide (1) Both source and destination IP addresses, (2) Only source IP, (3) Only destination IP, or (4) Network Interface? Enter the corresponding number (1-4): ")

    if ip_option == '1':
        src_ip = get_user_input("Enter source IP address: ")
        dst_ip = get_user_input("Enter destination IP address: ")
        return f"-s {src_ip} -d {dst_ip}"
    elif ip_option == '2':
        src_ip = get_user_input("Enter source IP address: ")
        return f"-s {src_ip}"
    elif ip_option == '3':
        dst_ip = get_user_input("Enter destination IP address: ")
        return f"-d {dst_ip}"
    elif ip_option == '4':
        network_interface = get_user_input("Enter Network Interface (e.g., eth0): ")
        return f"-i {network_interface}"
    else:
        print("Invalid option. Please enter a valid number.")
        return ask_for_ip_options()

def main():
    while True:
        # Conntrack menu
        conntrack_commands_menu = {
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
            '0': 'Exit'
        }

        print("\nConntrack Menu:")
        display_menu(conntrack_commands_menu)

        choice = get_user_input("Enter your choice (L, G, D, R, I, U, E, F, C, S, 0): ")

        if choice == '0':
            break

        if choice in conntrack_commands_menu:
            ip_options = ask_for_ip_options()

            # Construct the filename
            filename_placeholder = f"{ip_options.replace(' ', '_')}"
            filename = f"/var/conntrack_{filename_placeholder}.capture"

            # User skipped providing parameters, execute Conntrack command
            conntrack_command = f"conntrack {choice} {ip_options}"
            verbose_option = get_user_input("Do you want to see the output while executing the command? (yes/no): ").lower()
            if verbose_option == 'yes':
                result = execute_conntrack(conntrack_command, verbose=True)
            else:
                result = execute_conntrack(conntrack_command)

            # Save the result to the file
            save_to_file(filename, result)

            print(f"Command executed. Output saved to {filename}")

if __name__ == "__main__":
    main()

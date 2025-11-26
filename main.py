from olympics import*

def parse_command(text, host_dict):

    parts = text.split()

    if len(parts) != 3:
        raise ValueError("Incorrect command parameters")

    command_type = parts[0].strip().lower()
    command_parameter = parts[1].strip()
    filename = parts[2].strip()

    if command_type not in ("country", "year"):
        raise ValueError("Unknown command")

    if not filename.endswith(".txt"):
        raise ValueError("Invalid filename")

    if command_type == "country":

        if not (command_parameter.startswith("'") and command_parameter.endswith("'")):
            raise ValueError("Invalid command parameters")

        country = command_parameter.strip("'")

        output_country_results(filename, host_dict, country)

    elif command_type == "year":
        try:
            year = int(command_parameter)
        except ValueError:
            raise ValueError("Incorrect command parameters")

        output_year_results(filename, host_dict, year)

def command_system():

    host_dict = None

    while host_dict is None:
        host_filename = input("Enter the host data filename: ").strip()

        try:
            host_dict = load_hosts(host_filename)

        except FileNotFoundError:
            print("Invalid host filename")
        except ValueError:
            print("Invalid host file format")
        except Exception:
            print("Invalid host file format")


    while True:
        command = input("Enter a valid command or 'quit' to end the program: ").strip()

        if command.lower() == "quit":
            break

        if not command:
            continue

        try:
            parse_command(command, host_dict)

        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

from olympics import*

def parse_command(text, host_dict):
    text = text.strip()

    if text.lower().startswith("year "):
        parts = text.split()
        if len(parts) != 3:
            raise ValueError("Incorrect command parameters")
        command_type = parts[0].lower()
        year_str = parts[1]
        filename = parts[2]
        if not filename.endswith(".txt"):
            raise ValueError("Invalid filename")
        try:
            year = int(year_str)
        except:
            raise ValueError("Incorrect command parameters")
        output_year_results(filename, host_dict, year)
        return

    if not text.lower().startswith("country "):
        raise ValueError("Unknown command")

    first_quote = text.find("'")
    last_quote = text.rfind("'")

    if first_quote == -1 or last_quote == -1 or last_quote == first_quote:
        raise ValueError("Incorrect command parameters")

    country = text[first_quote+1:last_quote]
    after = text[last_quote+1:].strip()

    if " " in after:
        raise ValueError("Incorrect command parameters")

    filename = after

    if not filename.endswith(".txt"):
        raise ValueError("Invalid filename")

    output_country_results(filename, host_dict, country)


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

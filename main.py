"""
********************************************
CS 1026A Fall 2025
Assignment 3: Olympic Medals
Created by: River Levine LaFramenta
Student ID: rlevinel
Student Number: 251499864
File Created: November 22, 2025
********************************************
This file is used to analyze Olympic medal data from a variety of files.
The user must select a "host file", which includes data about previous host's of the Olympics,
and has the option to analyze the results of a specific Olympic year or a country's performance.
The user will also create a file of their choice, which will store the data pulled through the program.
"""

#Import functions from olympics.py
from olympics import*

#Determines if the user input is a 'year' or 'country' command
def parse_command(text, host_dict):
    #Remove whitespace
    text = text.strip()
    #Logic for the 'year' command
    if text.lower().startswith("year "):
        parts = text.split()
        #Needs to contain 3 parts (command, year, and filename)
        if len(parts) != 3:
            raise ValueError("Incorrect command parameters")
        command_type = parts[0].lower()
        year_str = parts[1]
        filename = parts[2]
        #Validate file extension
        if not filename.endswith(".txt"):
            raise ValueError("Invalid filename")
        #Ensure that year is an integer
        try:
            year = int(year_str)
        except:
            raise ValueError("Incorrect command parameters")
        #Call function to output year results
        output_year_results(filename, host_dict, year)
        return
    #Logic for 'Country' command
    if not text.lower().startswith("country "):
        raise ValueError("Unknown command")
    #Find single quotes
    first_quote = text.find("'")
    last_quote = text.rfind("'")
    #Make sure quotes exist and are different indexes
    if first_quote == -1 or last_quote == -1 or last_quote == first_quote:
        raise ValueError("Incorrect command parameters")
    #Get country name and filename
    country = text[first_quote+1:last_quote]
    after = text[last_quote+1:].strip()
    #Ensure filename does not contain spaces
    if " " in after:
        raise ValueError("Incorrect command parameters")

    filename = after
    #Validate file extension
    if not filename.endswith(".txt"):
        raise ValueError("Invalid filename")
    #Call function to output country results
    output_country_results(filename, host_dict, country)

#Main code
def command_system():

    host_dict = None
    #Loop to load host file
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

    #Prompt user for commands until they quit
    while True:
        command = input("Enter a valid command or 'quit' to end the program: ").strip()

        if command.lower() == "quit":
            break

        #Ignore empty inputs(User pressed ENTER)
        if not command:
            continue
        #Parse and execute command
        try:
            parse_command(command, host_dict)
        #Print error messages
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

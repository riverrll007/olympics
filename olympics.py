#Loads host data from a text file into a dictionary
def load_hosts(filename):
    #Empty dictionary to store results
    host_dict = {}
    try:
        #Go through file line by line
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(',')
                #Checks for format: Year, City, Country, Season
                if len(parts) != 4:
                    continue
                #Remove whitespace
                year_str = parts[0].strip()
                city = parts[1].strip()
                country = parts[2].strip()
                season = parts[3].strip()
                #Convert year to integer
                try:
                    year = int(year_str)
                except ValueError:
                    raise ValueError('Invalid host file format.')
                #Store daya for years 2000+
                if year >= 2000:
                    host_dict[year] = [city, country, season]

    except FileNotFoundError:
        #Raise to be handled by caller
        raise
    #Ensure a valid record was loaded
    if not host_dict:
        raise ValueError("Invalid host file format.")
    return host_dict

#Parse file with medal counts and return a dictionary
def load_medals(filename):
     medals_dict = {}
     try:
         with open(filename, "r") as file:
             #Skip the header line
             try:
                 next(file)
             except StopIteration:
                 #Return empty dict if file is empty
                 return medals_dict

             for line in file:
                 parts = line.strip().split(',')
                 #Ensure country, gold, silver, and bronze are in the file
                 if len(parts) < 4:
                     continue

                 country = parts[0].strip()
                 try:
                     #Convert medal amounts to integers
                     gold = int(parts[1].strip())
                     silver = int(parts[2].strip())
                     bronze = int(parts[3].strip())
                 except ValueError:
                     raise ValueError('Medal count is not an integer.')
                 #If a 5th column exists, use it for total
                 if len(parts) == 5:
                     try:
                         total_medals = int(parts[4].strip())
                     except ValueError:
                         #Backup if 5th column isnt a valid number
                         total_medals = gold + silver + bronze
                 #Calulate total medals if 5th row doesnt exist
                 else:
                     total_medals = gold + silver + bronze
                 #Store data
                 medals_dict[country] = [gold, silver, bronze, total_medals]
     except FileNotFoundError:
         raise
     return medals_dict
#Load medal data for a specific year
def try_load_medals(year):
    #Create filename based on year
    filename = f"medals{year}.csv"
    try:
        medals_dict = load_medals(filename)
        return medals_dict
    except FileNotFoundError:
        #Return None to show data is missing for this year
        return None
    except ValueError:
        return None
        #Return None if specific file doesnt work

#Create a file listing hosting and medal appearances for a country
def output_country_results(filename, host_dict, country):
    try:
        #Identify years hosted by country
        hosted_games = []
        #Cycle through main host dictionary
        for year in host_dict:
            data = host_dict[year]
            #Unpack list
            host_country = data[1]
            host_season = data[2]
            host_city = data[0]
            #Match the users country input
            if host_country.lower() == country.lower():
                hosted_games.append([year, host_season, host_city])
        #Sort chronologically
        hosted_games.sort(key=lambda x: x[0])
        #Identify medal appearances for the country
        medal_appearances = []
        #Get known Olympic years and sort them
        all_years = sorted(host_dict.keys())

        for year in all_years:
            #Get medal data for each known olympic year
            medals_data = try_load_medals(year)
            #If data exists and the country participated
            if medals_data and country in medals_data:
                medals = medals_data[country]
                medal_appearances.append((year, medals[0], medals[1], medals[2], medals[3]))
        #Output to file
        with open(filename, "w") as file:
            file.write(f"{country}\n")
            file.write("\n")
            #Output hosting info
            if not hosted_games:
                file.write("No Olympics hosted in this country.\n")
            else:
                file.write("Olympics hosted in this country:\n")
                #Format spacing
                file.write(f"{'Year':<5}   {'Type':<6}   {'City'}\n")

                for entry in hosted_games:
                    year, season, city = entry
                    file.write(f"{year:<5}   {season:<6}   {city.strip()}\n")
            file.write("\n")
            #Output medal info
            if not medal_appearances:
                file.write("No Olympic appearances by this country.\n")
            else:
                file.write("Olympic appearances by this country:\n")
                file.write(f"{'Year':<5}   {'Gold':<4}   {'Silver':<6}   {'Bronze':<6}   {'Total'}\n")

                num_appearances = len(medal_appearances)
                for i in range(num_appearances):
                    appearance = medal_appearances[i]
                    year, gold, silver, bronze, total = appearance
                    #Output row with proper format
                    file.write(f"{year:<5}   {gold:<4}   {silver:<6}   {bronze:<6}   {total:<5}")
                    #Add newline if its not the last line
                    if i < num_appearances - 1:
                        file.write("\n")

                file.write("\n")
    except Exception as e:
        print(f"Error writing country results to file {filename}: {e}")

#Create a file for a specific year's host and top medalists
def output_year_results(filename, host_dict, year):

    year_str = str(year)
    year_int = int(year)
    #Get data from dictionaries
    host_info = host_dict.get(year_int)
    medals_data = try_load_medals(year_int)

    try:
        with open(filename, "w") as file:
            #Check if year exists in host records
            if host_info is None:
                file.write(f"No Olympics were held in {year_str}")
                return
            #Get and write host details
            city, country, season = host_info
            file.write(f"Year: {year_str}\n")
            file.write(f"Host: {city}, {country}\n")
            file.write(f"Type: {season}\n")
            file.write("\n")
            #Check if medal data exists for specific year
            if medals_data is None:
                file.write(f"No medals data file available for {year_str}")
                return
            #Map catagories based on index in the medal list
            medal_types = [("gold", 0), ("silver", 1), ("bronze", 2), ("total", 3)]
            num_medal_types = len(medal_types)
            current_index = 0
            #Loop through medal types to find the highest scorer
            for medal_info in medal_types:
                m_type = medal_info[0]
                index = medal_info[1]

                max_count = -1
                max_countries = []
                #Find max value and county/countries(with ties)
                for country_name in medals_data:
                    medals = medals_data[country_name]
                    count = medals[index]
                    #Find new highscore
                    if count > max_count:
                        max_count = count
                        max_countries = [country_name]
                    #Deal with ties
                    elif count == max_count and max_count != -1:
                        max_countries.append(country_name)
                #Format output
                countries = " and ".join(max_countries)
                output = f"Most {m_type} medals: {max_count} by {countries}"
                file.write(output)
                #Add newline between catagories only if its not the last one
                if current_index < num_medal_types - 1:
                    file.write("\n")

                current_index += 1

    except Exception as e:
        print(f"Error writing year results to file {filename}: {e}")

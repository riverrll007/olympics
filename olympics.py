def load_hosts(filename):
    host_dict = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) != 4:
                    continue
                year = parts[0].strip()
                city = parts[1].strip()
                country = parts[2].strip()
                season = parts[3].strip()
                try:
                    year = int(year)
                except ValueError:
                    raise ValueError('Year must be an integer.')

                if year >= 2000:
                    host_dict[year] = [city, country, season]

    except FileNotFoundError:
        raise
    return host_dict

def load_medals(filename):
     medals_dict = {}
     try:
         with open(filename, "r") as file:
             for line in file:
                 parts = line.strip().split(',')
                 if len(parts) != 4 or len(parts) != 5:
                     continue
                 country = parts[0].strip()
                 try:
                     gold = int(parts[1].strip())
                     silver = int(parts[2].strip())
                     bronze = int(parts[3].strip())
                 except ValueError:
                     raise ValueError('Medals must be a number.')

                 total_medals = gold + silver + bronze
                 medals_dict[country] = [gold, silver, bronze, total_medals]
     except FileNotFoundError:
         raise
     return medals_dict

def try_load_medals(year):
    filename = f"medals_{year}.csv"
    try:
        medals_dict = load_medals(filename)
        return medals_dict
    except FileNotFoundError:
        return None
    except ValueError:
        return None

def output_country_results(filename, host_dict, country):
    hosted_games = []

    for year in host_dict:
        data = host_dict[year]

        host_country = data[1]
        host_season = data[2]
        host_city = data[0]

        if host_country.lower() == country.lower():
            hosted_games.append([year, host_season, host_city])
    hosted_games.sort()

    medal_appearances = []
    for year in hosted_games:
        medals_data = try_load_medals(year)
        if medals_data and country in medals_data:
            medals = medals_data[country]
            medal_appearances.append((year, medals[0], medals[1]. medals[2], medals[3]))

    try:
        with open(filename, "w") as file:
            file.write(f"{country}\n")
            file.write("\n")
            if not hosted_games:
                file.write("No Olympics hosted in this country.\n")
            else:
                file.write("Olympics hosted in this country.\n")
                file.write(f"{"year":<5} | {"season":<6} | {"city"}\n")

            f.write("\n")

            if not medal_appearances:
                file.write("No Olympic appearances by this country.\n")
            else:
                file.write("Olympic appearances by this country.\n")
                file.write(f"{"year":<5} | {"Gold":<4} | {"Silver":<6} | {"Bronze":<6} | {"Total"}\n")

                for i in range(len(medal_appearances)):
                    appearance = medal_appearances[i]
                    year, gold, silver, bronze, total = appearance
                    file.write(f"{year:<5} | {gold:<4} | {silver:<6} | {bronze:<6} | {total}")

                    if i < (len(medal_appearances) - 1):
                        file.write("\n")
    except Exception as e:
        print(f"Error writing results to file {filename}: {e}")

def output_year_results(filename, host_dict, year):

    host_info = host_dict[year]
    medals_data = try_load_medals(year)

    try:
        with open(filename, "w") as file:
            if host_info == None:
                file.write("No Olympics hosted in this year.\n")
                return

            city, country, season = host_info
            file.write(f"Year: {year}\n")
            file.write(f"City: {city}, {country}\n")
            file.write(f"Type: {season}\n")
            file.write("\n")

            if medals_data is None:
                file.write(f"No medals data file available for {year}\n")
                return

            medal_types = [("gold", 0), ("silver", 1), ("bronze", 2), ("total", 3)]

            num_medal_types = len(medal_types)
            counter = 0

            for medal in medal_types:
                m_type = medal[0]
                index = medal[1]

                max_count = -1
                max_countries = []

                for country_name in medal:
                    medals = medal[country_name]
                    count = medals[index]
                    if count > max_count:
                        max_count = count
                        max_countries = [country_name]
                    elif count == max_count and max_count != -1:
                        max_countries.append(country_name)
                countries = " and ".join(max_countries)
                output = f"Most {m_type} medals: {max_count} by {countries}"
                file.write(output)

                if count < num_medal_types - 1:
                    file.write("\n")

                count += 1

    except Exception as e:
        print(f"Error writing results to file {filename}: {e}")

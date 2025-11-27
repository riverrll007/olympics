def load_hosts(filename):
    host_dict = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) != 4:
                    continue
                year_str = parts[0].strip()
                city = parts[1].strip()
                country = parts[2].strip()
                season = parts[3].strip()
                try:
                    year = int(year_str)
                except ValueError:
                    continue
                    
                if year >= 2000:
                    host_dict[year] = [city, country, season]

    except FileNotFoundError:
        raise

    return host_dict

def load_medals(filename):
     medals_dict = {}
     try:
         with open(filename, "r") as file:
             try:
                 next(file)
             except StopIteration:
                 return medals_dict

             for line in file:
                 parts = line.strip().split(',')
                 if len(parts) < 4:
                     continue

                 country = parts[0].strip()
                 try:
                     gold = int(parts[1].strip())
                     silver = int(parts[2].strip())
                     bronze = int(parts[3].strip())
                 except ValueError:
                     continue
                 if len(parts) == 5:
                     try:
                         total_medals = int(parts[4].strip())
                     except ValueError:
                         total_medals = gold + silver + bronze
                 else:
                     total_medals = gold + silver + bronze
                 medals_dict[country] = [gold, silver, bronze, total_medals]
     except FileNotFoundError:
         raise
     return medals_dict

def try_load_medals(year):
    filename = f"medals{year}.csv"
    try:
        medals_dict = load_medals(filename)
        return medals_dict
    except FileNotFoundError:
        return None
    except ValueError:
        return None

def output_country_results(filename, host_dict, country):
    try:
        hosted_games = []

        for year in host_dict:
            data = host_dict[year]

            host_country = data[1]
            host_season = data[2]
            host_city = data[0]

            if host_country.lower() == country.lower():
                hosted_games.append([year, host_season, host_city])
        hosted_games.sort(key=lambda x: x[0])

        medal_appearances = []

        all_years = sorted(host_dict.keys())

        for year in all_years:
            medals_data = try_load_medals(year)
            if medals_data and country in medals_data:
                medals = medals_data[country]
                medal_appearances.append((year, medals[0], medals[1], medals[2], medals[3]))

        with open(filename, "w") as file:
            file.write(f"{country}\n")
            file.write("\n")
            if not hosted_games:
                file.write("No Olympics hosted in this country.\n")
            else:
                file.write("Olympics hosted in this country:\n")
                file.write(f"{'Year':<5}   {'Type':<6}   {'City'}\n")

                for entry in hosted_games:
                    year, season, city = entry
                    file.write(f"{year:<5}   {season:<6}   {city.strip()}\n")
            file.write("\n")

            if not medal_appearances:
                file.write("No Olympic appearances by this country.\n")
            else:
                file.write("Olympic appearances by this country:\n")
                file.write(f"{'Year':<5}   {'Gold':<4}   {'Silver':<6}   {'Bronze':<6}   {'Total'}\n")

                num_appearances = len(medal_appearances)
                for i in range(num_appearances):
                    appearance = medal_appearances[i]
                    year, gold, silver, bronze, total = appearance
                    file.write(f"{year:<5}   {gold:<4}   {silver:<6}   {bronze:<6}   {total:<5}")

                    if i < num_appearances - 1:
                        file.write("\n")

                file.write("\n")
    except Exception as e:
        print(f"Error writing country results to file {filename}: {e}")

def output_year_results(filename, host_dict, year):

    year_str = str(year)
    year_int = int(year)

    host_info = host_dict.get(year_int)
    medals_data = try_load_medals(year_int)

    try:
        with open(filename, "w") as file:
            if host_info is None:
                file.write(f"No Olympics were held in {year_str}")
                return

            city, country, season = host_info
            file.write(f"Year: {year_str}\n")
            file.write(f"Host: {city}, {country}\n")
            file.write(f"Type: {season}\n")
            file.write("\n")

            if medals_data is None:
                file.write(f"No medals data file available for {year_str}")
                return

            medal_types = [("gold", 0), ("silver", 1), ("bronze", 2), ("total", 3)]
            num_medal_types = len(medal_types)
            current_index = 0

            for medal_info in medal_types:
                m_type = medal_info[0]
                index = medal_info[1]

                max_count = -1
                max_countries = []

                for country_name in medals_data:
                    medals = medals_data[country_name]
                    count = medals[index]
                    if count > max_count:
                        max_count = count
                        max_countries = [country_name]
                    elif count == max_count and max_count != -1:
                        max_countries.append(country_name)
                countries = " and ".join(max_countries)
                output = f"Most {m_type} medals: {max_count} by {countries}"
                file.write(output)

                if current_index < num_medal_types - 1:
                    file.write("\n")

                current_index += 1

    except Exception as e:
        print(f"Error writing year results to file {filename}: {e}")

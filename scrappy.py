# Name: Luan Tu
# Student ID: 218277558
# -----------------------------------------------------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import lxml

# Extract:
# 1. Country name (done)
# 2. Capital (done)
# 3. Native languages (done)
# 4. Area (done)
# 5. Population (done)
# 6. GDP (PPP) (done)

# Scrape multiple pages-------------------------------------------------------------------------------------------------
link = ["https://en.wikipedia.org/wiki/Canada"
    , "https://en.wikipedia.org/wiki/China"
    , "https://en.wikipedia.org/wiki/United_States"
    , "https://en.wikipedia.org/wiki/South_Korea"
    , "https://en.wikipedia.org/wiki/United_Kingdom"
    , "https://en.wikipedia.org/wiki/France"
    , "https://en.wikipedia.org/wiki/Turkey"
    , "https://en.wikipedia.org/wiki/Italy"
    , "https://en.wikipedia.org/wiki/Vietnam"
        ]

country_name = []
capital = []
population = []
GDP = []
area_real_info = []
language = []

for i in link:
    soup = bs(requests.get(i).text, "lxml")
    page_table = soup.find("table", {"class": "infobox ib-country vcard"})
    #  Country name ----------------------------------------------------------------------------------------------------
    country_name_tem = soup.find("span", {"class": "mw-page-title-main"}).text
    country_name.append(country_name_tem)

    # Capital Info -----------------------------------------------------------------------------------------------------
    capital_tem = page_table.find("td", {"class": "infobox-data"}).find("a").text
    capital.append(capital_tem)

    # Languages Info ---------------------------------------------------------------------------------------------------
    lang_row = page_table.find_all("tr")
    for lang_item in lang_row:
        lang_finder = lang_item.text.find('language')
        if lang_finder != -1:
            if country_name_tem == "United States":
                us_lang_finder = lang_item.find_next("tr").find_next("td").text
                language.append(us_lang_finder)
            else:
                _infobox = lang_item.find("td", {"class": "infobox-data"}).text
                lang_tem = _infobox.replace("\n", "").split("[")
                language_value = lang_tem[0]
                language.append(language_value)
            break

    # Population Info --------------------------------------------------------------------------------------------------
    population_row = page_table.find("th", string="Population").find_next("td", {"class": "infobox-data"})
    population_info = population_row.get_text().split()
    population_temp = population_info[0].split("[")
    population_tem = population_temp[0].replace(',', '')
    population.append(int(population_tem))

    # GDP Info ---------------------------------------------------------------------------------------------------------
    gdp_row = page_table.find("th", {"class": "infobox-label"}).find_next("a", string="GDP")
    if gdp_row is None:
        gdp_tem = "$0"
    else:
        gdp_info = gdp_row.find_all_next("td", {"class": "infobox-data"})
        gdp_value = gdp_info[1].text.split()
        gdp = (gdp_value[0] + " " + gdp_value[1]).split("[")
        gdp_tem = gdp[0].replace("$", "").split("t")
        gdp_holder = gdp_tem[0]
        gdp_value_holder = int(float(gdp_holder) * 1e12)

        GDP.append(gdp_value_holder)

    # Area Info ---------------------------------------------------------------------------------------------------------
    area_row = page_table.find_all("tr", {"class": "mergedtoprow"})
    for i in area_row:
        area_temp = i.text.find("Area")
        if area_temp != -1:
            if country_name_tem == "Canada":
                ca_area = i.find_next("tr").text.split()
                ca_area_tem = ca_area[2].split("area")
                ca_area_holder = ca_area_tem[1].replace(',', '')
                area_real_info.append(int(ca_area_holder))
            elif country_name_tem == "United States":
                us_area = i.find_next("tr").text.split()
                us_area_tem = us_area[5].split("(")
                us_area_holder = us_area_tem[1].replace(',', '')
                area_real_info.append(int(us_area_holder))
            else:
                area = i.find_next("tr").text.split()
                area_tem = area[1]
                # area_value = area_tem[1]
                area_value_tem = area_tem.split("l")
                area_value = area_value_tem[1].split("[")
                area_value_holder = area_value[0].replace(',', '')
                area_real_info.append(int(area_value_holder))

data = {
    "Country": country_name,
    "Language": language,
    "Capital": capital,
    "Population": population,
    "GDP (PPP)": GDP,
    "Area (km2)": area_real_info
}

df = pd.DataFrame(data)
print(df.to_string() + "\n")

# Highest Info ---------------------------------------------------------------------------------------------------------
country_with_highest_population = df.loc[df['Population'].idxmax()]['Country']
country_with_highest_gdp = df.loc[df['GDP (PPP)'].idxmax()]['Country']
country_with_highest_area = df.loc[df['Area (km2)'].idxmax()]['Country']

print(f"Country with the highest population: {country_with_highest_population}")
print(f"Country with the highest GDP: {country_with_highest_gdp}")
print(f"Country with the highest Area: {country_with_highest_area}" + "\n")

# Correlation Info -----------------------------------------------------------------------------------------------------
area_population_corr = round(df['Area (km2)'].corr(df['Population']), 2)
area_gdp_corr = round(df['Area (km2)'].corr(df['GDP (PPP)']), 2)
population_gdp_corr = round(df['Population'].corr(df['GDP (PPP)']), 2)

print(f"Correlation coefficient between Area and Population: {area_population_corr}")
print(f"Correlation coefficient between Area and GDP: {area_gdp_corr}")
print(f"Correlation coefficient between Population and GDP: {population_gdp_corr}")

print("\n\nMade by Luan Tu - 218277558")
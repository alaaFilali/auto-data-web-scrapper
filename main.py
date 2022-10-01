from bs4 import BeautifulSoup
import requests
import pandas as pd

URL = "https://www.auto-data.net"

soup = BeautifulSoup(requests.get(URL).text, "html.parser")

brands = soup.findAll(name="a", class_="marki_blok")

cars_list = []
# just change this number to scrape a certain brand
for brand in brands[:2]:
    car_info_list = []
    soup_2 = BeautifulSoup(requests.get(URL + brand["href"]).text, "html.parser")
    brand_models = soup_2.findAll(name="a", class_="modeli")

    for model in brand_models[:1]:
        soup_3 = BeautifulSoup(requests.get(URL + model["href"]).text, "html.parser")
        brand_generation = soup_3.findAll(name="a", class_="position")

        for generation in brand_generation[:1]:
            soup_4 = BeautifulSoup(requests.get(URL + generation["href"]).text, "html.parser")

            cars = soup_4.findAll(name="tr", class_="i")

            for car in cars[:1]:
                car_ = car.find(name="a")
                en_url = str(car_["href"]).replace("bg", "en")
                soup_5 = BeautifulSoup(requests.get(URL + en_url).text, "html.parser")

                cars_info = soup_5.find(name="table", class_="cardetailsout car2").findAll(name="td")

                for info in cars_info[:10]:
                    car_info_list.append(info.text)

                if "year" not in car_info_list[5]:
                    car_info_list.insert(5, 0)
                    car_info_list.pop()

                if len(car_info_list[8]) > 3:
                    car_info_list[8] = 0
                if len(car_info_list[9]) > 3:
                    car_info_list[9] = 0

                cars_list.append(car_info_list)
                car_info_list = []

cars_df = pd.DataFrame(cars_list,
                       columns=['Brand',
                                'Model',
                                'Generation',
                                'Modification (Engine)',
                                'Start of production',
                                'End of production',
                                'Powertrain Architecture',
                                'Body type',
                                'Seats',
                                'Doors'])

# Exporting the dataframe to a csv file
# don't forget to change the name every time you scrape a new brand
cars_df.to_csv('auto-data-report-alfa-romeo-test.csv')

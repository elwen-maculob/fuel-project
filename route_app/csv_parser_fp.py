#separate py file to read and store csv to RAM for fetching and fuel calculation
import csv
import os
from django.conf import settings

FUEL_STATION_LIST=[] #list to store in RAM

class FuelData:
    def __init__(self):
        self.file_path = os.path.join(settings.BASE_DIR, 'fuel_prices.csv')
        self.parse_csv_file()

    def parse_csv_file(self):
        global FUEL_STATION_LIST
        if FUEL_STATION_LIST:
            return

        try:
            with open(self.file_path, mode='r', encoding='utf-8') as filehandle:
                parser = csv.DictReader(filehandle)
                for row in parser:
                    fuelstation = {
                        "station_name": row['Truckstop Name'],
                        "address": row['Address'],
                        "city": row['City'],
                        "state": row['State'],
                        "price_per_gallon": float(row['Retail Price'])
                    }
                    FUEL_STATION_LIST.append(fuelstation)
            print(f"Successfully stored {len(FUEL_STATION_LIST)} fuel stations into memory!")
        except Exception as e:
            print(f"Error reading CSV file: {e}")
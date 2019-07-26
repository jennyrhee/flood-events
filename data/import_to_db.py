import sqlite3
import os
import pandas as pd


conn = sqlite3.connect('storms.db')
c = conn.cursor()

locations_pass_count = 0
fatalities_pass_count = 0
for root, dirs, files in os.walk("."):
    path = root.split(os.sep)
    for f in files:
        if '.csv' in f:
            print('Starting import of:', f)
            if 'details' in f:
                df = pd.read_csv('details/' + f)
                df.to_sql('details', conn, if_exists='append', index=False)
            elif 'locations' in f:
                df = pd.read_csv('locations/' + f)
                try:
                    df.to_sql('locations', conn, if_exists='append', index=False)
                except sqlite3.IntegrityError:
                    # Most of the pertinent details are in the details table so ignore for now
                    locations_pass_count += 1
                    pass
            else:
                df = pd.read_csv('fatalities/' + f)
                try:
                    df.to_sql('fatalities', conn, if_exists='append', index=False)
                except sqlite3.IntegrityError:
                    # Most of the pertinent details are in the details table so ignore for now
                    fatalities_pass_count += 1
                    pass
            print('Completed import of:', f, '\n')

print('Completed import of csv files to database.')
print(f'Passed count for locations: {locations_pass_count}')
print(f'Passed count for fatalities: {fatalities_pass_count}')
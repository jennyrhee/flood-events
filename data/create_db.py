import sqlite3

conn = sqlite3.connect('data/storms.db')
c = conn.cursor()

c.execute('PRAGMA foreign_keys = ON;')

c.execute('''
          CREATE TABLE details (
           BEGIN_YEARMONTH integer,
           BEGIN_DAY integer,
           BEGIN_TIME integer,
           END_YEARMONTH integer,
           END_DAY integer,
           END_TIME integer,
           EPISODE_ID integer,
           EVENT_ID integer PRIMARY KEY,
           STATE text,
           STATE_FIPS integer,
           YEAR integer,
           MONTH_NAME text,
           EVENT_TYPE text,
           CZ_TYPE text,
           CZ_FIPS integer,
           CZ_NAME text,
           WFO text,
           BEGIN_DATE_TIME date,
           CZ_TIMEZONE text,
           END_DATE_TIME date,
           INJURIES_DIRECT integer,
           INJURIES_INDIRECT integer,
           DEATHS_DIRECT integer,
           DEATHS_INDIRECT integer,
           DAMAGE_PROPERTY text,
           DAMAGE_CROPS text,
           SOURCE text,
           MAGNITUDE integer,
           MAGNITUDE_TYPE text,
           FLOOD_CAUSE text,
           CATEGORY blob,
           TOR_F_SCALE text,
           TOR_LENGTH real,
           TOR_WIDTH integer,
           TOR_OTHER_WFO text,
           TOR_OTHER_CZ_STATE text,
           TOR_OTHER_CZ_FIPS integer,
           TOR_OTHER_CZ_NAME text,
           BEGIN_RANGE integer,
           BEGIN_AZIMUTH text,
           BEGIN_LOCATION text,
           END_RANGE integer,
           END_AZIMUTH text,
           END_LOCATION text,
           BEGIN_LAT real,
           BEGIN_LON real,
           END_LAT real,
           END_LON real,
           EPISODE_NARRATIVE text,
           EVENT_NARRATIVE text,
           DATA_SOURCE text,
           FOREIGN KEY (EPISODE_ID) REFERENCES locations(EPISODE_ID)
          );
          ''')

c.execute('''
          CREATE TABLE locations (
           YEARMONTH integer,
           EPISODE_ID integer PRIMARY KEY,
           EVENT_ID integer,
           LOCATION_INDEX integer,
           RANGE real,
           AZIMUTH text,
           LOCATION text,
           LATITUDE real,
           LONGITUDE real,
           LAT2 integer,
           LON2 integer,
           FOREIGN KEY(EVENT_ID) REFERENCES details(EVENT_ID)
          );
          ''')

c.execute('''
          CREATE TABLE fatalities (
           FAT_YEARMONTH integer,
           FAT_DAY integer,
           FAT_TIME integer,
           FATALITY_ID integer PRIMARY KEY,
           EVENT_ID integer,
           FATALITY_TYPE text,
           FATALITY_DATE date,
           FATALITY_AGE integer,
           FATALITY_SEX text,
           FATALITY_LOCATION text,
           EVENT_YEARMONTH integer,
           FOREIGN KEY(EVENT_ID) REFERENCES details(EVENT_ID)
          );
          ''')

conn.commit()
conn.close()
import sqlite3

conn = sqlite3.connect('data/storms.db')
c = conn.cursor()

c.execute('PRAGMA foreign_keys = ON;')

c.execute('''
          CREATE TABLE details (
           last_date_modified date,
           last_date_certified date,
           episode_id integer,
           event_id integer PRIMARY KEY,
           state text,
           state_fips integer,
           year integer,
           month_name text,
           event_type text,
           cz_type text,
           cz_fips integer,
           cz_name text,
           wfo text,
           begin_date_time date,
           cz_timezone text,
           end_date_time date,
           injuries_direct integer,
           injuries_indirect integer,
           deaths_direct integer,
           deaths_indirect integer,
           damage_property integer,
           damage_crops integer,
           source text,
           magnitude real,
           magnitude_type text,
           flood_cause text,
           category blob,
           tor_f_scale text,
           tor_length real,
           tor_width integer,
           tor_other_wfo text,
           tor_other_cz_state text,
           tor_other_cz_fips integer,
           tor_other_cz_name text,
           episode_title text,
           episode_narrative text,
           event_narrative text,
           FOREIGN KEY(episode_id) REFERENCES locations(episode_id)
          );
          ''')

c.execute('''
          CREATE TABLE locations (
           episode_id integer PRIMARY KEY,
           event_id integer,
           location_index text,
           range real,
           azimuth text,
           location text,
           lat real,
           lon real,
           FOREIGN KEY(event_id) REFERENCES details(event_id)
          );
          ''')

c.execute('''
          CREATE TABLE fatalities (
           fatality_id integer PRIMARY KEY,
           event_id integer,
           fatality_type text,
           fatality_date date,
           fatality_age integer,
           fatality_sex text,
           fatality_location text,
           FOREIGN KEY(event_id) REFERENCES details(event_id)
          );
          ''')

conn.commit()
conn.close()
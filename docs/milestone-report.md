# Predicting flood events in Louisiana

Springboard Capstone 1 Milestone Report

By Jenny Rhee

---

## Problem Statement

The goal of this capstone project is to predict flood events in Louisiana. Building this model can potentially assist cities and the general population in preparation for flooding. People will likely have experience with flooding, but the prevalence is expected to increase with climate change. It is important to begin understanding the rising trends.

## Data

The National Weather Service provides [storm data](https://catalog.data.gov/dataset/ncdc-storm-events-database) containing statistics on personal injuries and damage estimates from 1950 to present. There are 34 different storm events including various types of floods, hurricanes, thunderstorms, hail, etc. There are 51 columns including damage, injuries, deaths, etc. I used [Python scripts](https://github.com/jennyrhee/storm-events/tree/master/src/preparation) to download all 213 csv files, create a database, and injest the data into the database. Additional supporting data includes historical meteorological data to analyze any potential correlations. NOAA's National Centers for Environmental Information has [Daily Summaries](https://www.ncdc.noaa.gov/cdo-web/datatools/findstation/) data at numerous stations across the United States (Figure 1). This data included air temperature, precipitation, and wind speed.

![](img/stations.png)
**Figure 1**. Locations of weather stations in Louisiana.

## Data Cleaning Summary

### Storm Events Data

There were several entries for parish that weren't exact parish names, mainly including a region within the parish (e.g., East Cameron vs. Cameron). The FIPS DataFrame was used to check the FIPS code for each of the entries and compared with the actual parish FIPS codes. One parish, Sabine and Natchitoches, had coordinates that could be checked using the [coordinates2politics API](http://www.datasciencetoolkit.org/coordinates2politics/) was used to find the parish based on coordinates; Sabine was returned. Some of the entries had invalid FIPS codes (from comparing with the Louisiana parish Wikipedia page). The names were changed to remove the region and contain only the parish. There were 52 remaining rows with null parishes. The coordinates2politics API was again used to try and find the parish. 14 rows returned no parish data and were dropped. Finally, the parishes were mapped to the correct FIPS code to create a FIPS column. There were a few rows with null FIPS, but they were counties outside of Louisiana and were dropped.

The property damage column consisted of strings with nulls, 0, or values appended by K (thousand), M (million), and B (billion). They were converted into the correct numerical values.

There were 16,946 rows in the final DataFrame.

### Meteorological Data

There were 11 variables chosen that were thought to be variables of interest: average daily wind speed, precipitation, average of hourly temperature values, maximum temperature, minimum temperature, direction of fastest 2-minute wind, direction of fastest 5-second wind, fastest 2-minute wind speed, and fastest 5-second wind speed. The initial dataset had 214,708 rows.

A new DataFrame was created with name, latitude, and longitude from the original DataFrame, and duplicates were dropped. Using multi-processing (`pandarallel`), the coordinates2politics API was used to query for each parish based on the coordinates of each station. This DataFrame was merged with the original DataFrame, and the station and elevation columns were dropped.

The station data was aggregated to represent the parish in its entirety by taking the mean of all data points for stations within each station for each date. This resulted in 162,229 rows. This DataFrame was merged with the storm events DataFrame.

### Combined Storm Events and Meteorological DataFrame

The average of hourly temperature values variable was dropped because there was a lot of missing data (~74%). For rows with null storm events data, a new event type called "None" was created indicating that no event happened on these days. There were 2,202 flood event types (Coastal Flood, Flash Flood, and Flood), but only 812 rows with complete meteorological data.

5,000 samples were sampled for none events that occurred in parishes and years that a flood event occurred. A new feature representing the previous 7-day total precipitation was created. Rows were dropped if there were less than 4 previous days of data. Another feature representing region was created with possible values being Northwest, Northeast, Central, Southwest, and Southeast. Finally, a season feature was created (winter, spring, summer, fall). The final DataFrame had 5,812 rows.

## Exploratory Analysis Summary

There were 668 flash floods, 132 floods, and 11 coastal floods in the dataset (Figure 2).

![flood counts](img/flood_counts.png)
**Figure 2**. Counts of each flood event type.

Precipitation will likely be the most important feature (Figure 3). As expected, no events generally have the least amount of precipitation while flash floods have the most amount of precipitation.

![precipitation distribution](img/precip_box.png)
**Figure 3**. Distribution of precipitation by event.

Interestingly, coastal floods have the least amount of previous 7-day precipitation (Figure 4). Coastal flooding is when a coastal process (e.g., waves, tides, storm surge) produces a flood on normally dry land areas ([Source](https://www.researchgate.net/publication/259740986_Coastal_Hazards_and_Climate_Change_A_Guidance_Manual_for_Local_Government_in_New_Zealand)). Additionally, there are only 11 coastal flood events in the dataset. The small sample size and the fact that these events happen in typically dry lands could be a reason why previous 7-day precipitation is lower than no events.

![previous 7 day precipitation distribution](img/precip_7d_box.png)
**Figure 4**. Distribution of previous 7-day precipitation by event.

Wind speed is another interesting feature to consider (Figure 5). Coastal flood has a higher average wind speed than the other event types. This is intuitive because these events are caused by coastal processes such as waves, tides, and storm surges, which are strongly influenced by wind.

![wind distribution](img/wind.png)
**Figure 5**. Distribution of wind speed by event.

There different methods were used to find correlation coefficients depending on the variable types being compared (Figure 8). Pearson's correlation was used for continuous vs. continuous variables [-1, 1]. Point biserial correlation was used for categorical vs. continuous variables [-1, 1]. Cramer's V was used for categorical vs. categorical variables [0, 1].

![correlation matrix](img/corr_matrix.png)
**Figure 6**. Correlation matrix for all features.

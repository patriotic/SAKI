# Project Plan

## Summary

<!-- Describe your data science project in max. 5 sentences. -->
This project analyzes how weather condition relates to the speed limit on roads in the Bonn city area. Moreover, it analyzes the traffic fine occurrences due to exceeding the speed limit and its relation to temperature, wind, and precipitation in particular dates in 2020 from January to December.

## Rationale

<!-- Outline the impact of the analysis, e.g. which pains it solves. -->
The analysis helps to identify patterns in driving behavior related to weather conditions by combining the speeding fine dataset with weather data. Authorities can allocate resources such as police patrols or traffic cameras to areas that are more prone to accidents during certain weather conditions. This information can be used to improve road safety by allocating resources more effectively, improving driver education through campaigns, and reducing the incidence of speeding during certain weather conditions.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: Bußgelder fließender Verkehr 2020
* Metadata URL: [https://mobilithek.info/offers/-4621475474583083551](https://mobilithek.info/offers/-4621475474583083551)
* Data URL: [https://opendata.bonn.de/sites/default/files/Speed violations Bonn2020.csv](https://opendata.bonn.de/sites/default/files/GeschwindigkeitsverstoesseBonn2020.csv)
* Data Type: CSV

This dataset contains information on fines for speeding in the Bonn City area. It includes the date, time, place, fines, and offense number.

### Datasource2: NASA Prediction Of Worldwide Energy Resources
* Metadata URL: [https://power.larc.nasa.gov/data-access-viewer](https://power.larc.nasa.gov/data-access-viewer)
* Data URL: [https://drive.google.com/file/d/1E3OD_pLfRaeJX0T_kphVByg-k1eQx37W/view?usp=sharing](https://drive.google.com/file/d/1E3OD_pLfRaeJX0T_kphVByg-k1eQx37W/view?usp=sharing)
* Data Type: CSV

This weather dataset is generated from the POWER project using the following options:
* Date: Jan 01, 2020 to Dec 31, 2020
* Temporal: Daily
* Location: Bonn
* Parameters: Temperature at 2 Meters, Precipitation, Wind Speed at 10 Meters.

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Automate data pipeline [#1][i1]
2. Project deployment [#2][i2]
3. Data preprocessing [#3][i3]
4. Merge the datasets [#4][i4]
5. Analyze the data [#5][i5]
6. Data visualization [#6][i6]

[i1]: https://github.com/patriotic/SAKI/issues/1
[i2]: https://github.com/patriotic/SAKI/issues/2
[i3]: https://github.com/patriotic/SAKI/issues/3
[i4]: https://github.com/patriotic/SAKI/issues/4
[i5]: https://github.com/patriotic/SAKI/issues/5
[i6]: https://github.com/patriotic/SAKI/issues/6

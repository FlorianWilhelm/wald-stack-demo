The `cameri_weather.csv` was downloaded from [opendatasoft] using

```commandline
curl -X 'GET' \                                                                                                                                                                                                                                  wald-stack
  'https://public.opendatasoft.com/api/v2/catalog/datasets/noaa-daily-weather-data/exports/csv?refine=name:CAMERI' \
  -H 'accept: */*' > seeds/cameri_weather.csv
```

Since the weather data was not always available on every day, following changes were made:

- 2015-09-07 -> 2015-09-06
- 2017-09-04 -> 2017-09-03
- 2018-09-03 -> 2018-09-02


It's public domain.

[opendatasoft]: https://public.opendatasoft.com/explore/dataset/noaa-daily-weather-data/

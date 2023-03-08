The `cameri_weather.csv` was downloaded from [opendatasoft] using

```commandline
curl -X 'GET' \                                                                                                                                                                                                                                  wald-stack
  'https://public.opendatasoft.com/api/v2/catalog/datasets/noaa-daily-weather-data/exports/csv?refine=name:CAMERI' \
  -H 'accept: */*' > seeds/cameri_weather.csv
```

It's public domain.

[opendatasoft]: https://public.opendatasoft.com/explore/dataset/noaa-daily-weather-data/

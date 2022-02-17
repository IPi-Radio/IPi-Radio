## expected structure of `radiostations.json`:

```json
{
    "station name": {
        "time": "hh:mm",
        "url": "",
        "favicon": "",
        "codec": "",
        "bitrate": 0,
        "countrycode": "",
        "language": ""
    },
    (...)
}
```

- `time`: time to play this station, when automation is enabled; setting to `default` will use that station as fallback | optional
- `url`: url of the audiostream
- `favicon`: url to the icon of the radio station | optional
- `codec`: format of the audiostream (usually MP3 or AAC) | optional
- `birate`: must be integer | optional
- `countrycode` and `language` | optional
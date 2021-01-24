# Air quality monitoring

> When should I open my window for fresh air?
> Here is the answer!

This repository provides a ready to install app for
air quality monitoring with an [SGP30 Air Quality Sensor](https://www.sparkfun.com/products/16531)
and a raspberry pi.

## Setup

You will need:

- [SGP30 Air Quality Sensor](https://www.sparkfun.com/products/16531)
- A Raspberry Pi

### Flash already built image

If you just want this to work, you can install the latest image
from the [latest build](https://github.com/randombenj/air-quality-monitoring/actions?query=workflow%3A%22OS+image%22)
and [flash it to an sd card](https://raspberrypi.stackexchange.com/a/932).

### Install from source

You may want to use [poetry](https://python-poetry.org/) for an easyer installation.

If you already have a Raspberry Pi set up, you can install the package
from source like this:

```sh
# get the source
git clone git@github.com:randombenj/air-quality-monitoring.git
cd air-quality-monitoring/qualitair

# install dependencies
poetry install

# run it!
poetry shell
cd ..
python -m qualitair
```


## Desktop notification

If you want to get a desktop notification (on Ubuntu) when to open windows,
you can simply add this cronjob:

```
* * * * * CO2=$(curl -s http://RASPI_IP:8080/\?limit=1 | jq '.measurements[0].co2') && test $CO2 -gt 1100 && XDG_RUNTIME_DIR=/run/user/$(id -u) notify-send "Open windows!" "CO2: $CO2"
```

Note that you will need to install [jq](https://stedolan.github.io/jq/) for this to work.

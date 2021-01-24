"""
A data gathering daemon to read data from
the SGP30 sensor
"""
import logging
import asyncio
from sgp30 import SGP30

from qualitair.db import Measurement


class DataDaemon():
    def __init__(self):
        self._sensor = SGP30()
        self._run = True

    def quit(self):
        self._run = False

    async def run(self):
        logging.info("initialize the sensor")
        self._sensor.start_measurement()

        while self._run:
            result = self._sensor.get_air_quality()
            logging.info(result)

            await Measurement.create(
                value=result.equivalent_co2,
                type="co2_ppm"
            )
            await asyncio.sleep(1)

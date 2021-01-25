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
        # as the `self._sensor.start_measurement()` would be
        # blocking, it is reimplemented in the loop
        # and will only start recording measurements
        # when the sensor is heated up.
        self._sensor.command('init_air_quality')
        is_inited = False
        testsamples = 0

        while self._run:
            result = self._sensor.get_air_quality()
            logging.info(result)

            if is_inited:
                await Measurement.create(
                    co2=result.equivalent_co2,
                    voc=result.total_voc
                )
            else:
                testsamples = testsamples + 1
                if result.equivalent_co2 != 400 or result.total_voc != 0 or testsamples > 20:
                    is_inited = True

            await asyncio.sleep(1)

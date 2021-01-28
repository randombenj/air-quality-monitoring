"""
A data gathering daemon to read data from
the SGP30 sensor
"""
import logging
import asyncio
import board
import adafruit_dht
from sgp30 import SGP30

from qualitair.db import Measurement


class DataDaemon():
    def __init__(self):
        self._sgp30_sensor = SGP30()
        self._dht22_sensor = adafruit_dht.DHT22(board.D4)
        self._run = True

    def quit(self):
        self._run = False

    def __read_sensor_values(self):
        co2 = -1
        voc = -1
        temperature = float('nan')
        humidity = float('nan')
        try:
            result = self._sgp30_sensor.get_air_quality()
            co2 = result.equivalent_co2
            voc = result.total_voc

            temperature = self._dht22_sensor.temperature
            humidity = self._dht22_sensor.humidity

            logging.info(f"co3 ppm: {co2}, cov: {voc}, temparature: {temperature}, humidity: {humidity}")
        except Exception as err:
            logging.exception("Error reading sensor", err)

        return co2, voc, temperature, humidity

    async def run(self):
        logging.info("initialize the sensor")
        # as the `self._sensor.start_measurement()` would be
        # blocking, it is reimplemented in the loop
        # and will only start recording measurements
        # when the sensor is heated up.
        self._sgp30_sensor.command('init_air_quality')

        is_inited = False
        testsamples = 0

        while self._run:
            co2, voc, temperature, humidity = self.__read_sensor_values()

            if is_inited:
                try:
                    await Measurement.create(
                        co2=co2,
                        voc=voc,
                        temperature=temperature,
                        humidity=humidity
                    )
                except Exception as err:
                    logging.exception("Error saving to database", err)
            else:
                testsamples = testsamples + 1
                if co2 != 400 or voc != 0 or testsamples > 20:
                    logging.debug("Initialized sensor")
                    is_inited = True

            await asyncio.sleep(1)

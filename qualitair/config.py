import os


DATABASE = os.environ.get("DATABASE", "sqlite://qualitair.db")

# delay to query the sensors (in seconds)
QUERY_DELAY = int(os.environ.get("QUERY_DELAY", 10))
# wether to also use the dht22 sensor
ENABLE_DHT22 = bool(os.environ.get("ENABLE_DHT22", True))
# the gpio pin which the dht22 is connected to
DHT22_PIN = os.environ.get("DHT22_PIN", "4")
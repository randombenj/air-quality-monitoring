from tortoise.models import Model
from tortoise import Tortoise, fields

from qualitair.config import DATABASE


async def init():
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(
        db_url=DATABASE,
        modules={'models': ["qualitair.db"]}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

async def quit():
    # close all connections cleanly
    # https://tortoise-orm.readthedocs.io/en/latest/setup.html#cleaningup
    await Tortoise.close_connections()


class Measurement(Model):
    id = fields.IntField(pk=True)
    co2 = fields.IntField()
    voc = fields.IntField()
    # sometimes the reading of the dht22 sensor fails
    # this is why they are allowed to be null
    temperature = fields.FloatField(null=True)
    humidity = fields.FloatField(null=True)
    timestamp = fields.data.DatetimeField(auto_now=True)

    def to_json(self):
        return {
            "id": self.id,
            "co2": self.co2,
            "voc": self.voc,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "timestamp": self.timestamp.isoformat()
        }

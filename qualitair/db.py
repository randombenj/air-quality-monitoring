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


class Measurement(Model):
    id = fields.IntField(pk=True)
    value = fields.FloatField()
    type = fields.TextField()
    timestamp = fields.data.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.type} @ {self.value::%Y-%m-%d %H:%M:%S}: {self.value:.2f}"


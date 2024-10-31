from peewee import SqliteDatabase, Model, CharField, DateTimeField
from peewee import IntegrityError
from time import time as unix_time
from math import floor


# initialize db
db = SqliteDatabase("app.db")


class BaseModel(Model):
    """Model class which the Results class will extend."""
    class Meta:
        database = db


class Results(BaseModel):
    location = CharField(unique=True, null=False)
    lat = FloatField(null=False)
    long = FloatField(null=False)
    time = BigIntegerField(default=floor(unix_time()), null=False)
    aqi = IntegerField(null=False)
    earthquake_data

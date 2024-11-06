from peewee import *
import datetime


# initialize db
db = SqliteDatabase("app.db")


class BaseModel(Model):
    """Model class which the Results class will extend."""
    class Meta:
        database = db


class Results(BaseModel):
    # all attributes for the db table
    id = AutoField(primary_key=True)
    location = CharField(null=False)

    # generates the date of all api data that was saved
    date_saved = DateField(null=False)

    # these attributes hold the api results data
    aqi = IntegerField(null=False)
    earthquakes = CharField(null=False)
    flood = CharField(null=False)


# connect to db and create table called Results
db.connect()
db.create_tables([Results])

# clears database so no repeat data is generated
# Results.delete().execute()

def display_id_location():
    """ This will return all locations, data saved, and their primary id so user can determine
    what location they want to see more information on"""

    display_list = []
    id_location = Results.select()

    for i in id_location:
        display_list.append(f'ID: {i.id} | {i.location} | {i.date_saved}')

    return display_list


def save_api_info(city_state, earthquake_result, aqi_result, flood_result):
    """ When user clicks the "safe results link", this function will be called to save
    location, date saved, and all api results data to the app.db database

    Note: Since the earthquake list can't be saved as a list, the join function is used to
    the earthquake list to one big string."""

    earthquake_str = '@'.join(earthquake_result) # join list with @ between... makes using sep='@' easier when
                                                # displaying to user
    new_entry = Results(
                        location=city_state,
                        date_saved=datetime.date.today(),
                        aqi=aqi_result,
                        earthquakes=earthquake_str,
                        flood=flood_result)
    new_entry.save()


def get_api_info(db_id):
    """ retrieves the databases table row by id number.
    the user enters what id they want to access data from
    and this function returns a dictionary of its entry.

    Note: the saved earthquake string is turned back to a list using the split function """

    result = Results.get_by_id(db_id)
    earthquake_list = result.earthquakes.split('@') # turns joined string back to a list where the seperator is @
    return {'location': result.location,
            'date': result.date_saved,
            'aqi': result.aqi,
            'earthquake': earthquake_list,
            'flood': result.flood
            }











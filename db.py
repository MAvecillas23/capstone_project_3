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

    # generates date api_data was saved
    date_saved = DateField(null=False)

    # these attributes hold the api results data
    aqi = IntegerField(null=False)
    earthquakes = CharField(null=False)
    flood = CharField(null=False)


# connect to db and create table called Results
db.connect()
db.create_tables([Results])

# clears database so no repeat data is generated
# uncomment below when officially done
# Results.delete().execute()



# the idea is that this will return all locations and their primary id so user can determine
# what location they want to see information on
def display_id_location():
    display_list = []
    id_location = Results.select()

    for i in id_location:
        display_list.append(f'{i.id}      {i.location}     {i.date_saved}')


    return display_list


# save all api_data, and location and generate the date data was saved
def save_api_info(city_state, earthquake_result, aqi_result, flood_result):

    earthquake_str = '@'.join(earthquake_result) # join list with @ between... makes using sep='@' easier when
                                                # displaying to user
    new_entry = Results(
                        location=city_state,
                        date_saved=datetime.date.today(),
                        aqi=aqi_result,
                        earthquakes=earthquake_str,
                        flood=flood_result)
    new_entry.save()



# retrieves the table row by id number.
# the idea is that user enters what id they want to access data from
# and returns a dictionary of its respective field.
# will make displaying information easier in bookmarks page
def get_api_info(db_id):
    result = Results.get_by_id(db_id)
    earthquake_list = result.earthquakes.split('@') # turns joined string back to a list where the seperator is @
    return {'location': result.location,
            'date': result.date_saved,
            'aqi': result.aqi,
            'earthquake': earthquake_list,
            'flood': result.flood
            }

# deletes an entry when user enters an id to delete
def delete_entry(db_id):
    Results.delete().where(Results.id == db_id).execute()










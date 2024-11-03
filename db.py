from peewee import *
from peewee import IntegrityError
from time import time as unix_time
from math import floor
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
    location = CharField(unique=True, null=False)

   # do we need lat long?
    # lat = FloatField(null=False)
    # long = FloatField(null=False)

    #time = BigIntegerField(default=floor(unix_time()), null=False)  #what is this?

    date_saved = DateField(null=False)

    # these attributes hold the api results data
    aqi = IntegerField(null=False)
    earthquakes = CharField(null=False)
    flood = CharField(null=False)


# connect to db and create table called Results
db.connect()
db.create_tables([Results])

# clears database so no repeat data is generated
Results.delete().execute()



# Test data to ensure functions are outputting desired data
earthquake1 = ['1', '2', '3']
air_index1 = 2
flooding1 = 'not safe'
location1 = 'Minneapolis, MN'
blah1 = ['g', 'r', 'l']
blah2 = 5
blah3 = 'safe'
blah4 = 'Blah, Indiana'


# main function is for test purposes
# remove for final product
def main():
    save_api_info(location1, earthquake1, air_index1, flooding1)
    save_api_info(blah4, blah1, blah2, blah3)

    test_info = get_api_info(2)
    test_info2 = get_api_info(1)

    print(test_info)
    print(test_info2)

    display_id_location()


# the idea is that this will return all locations and their primary id so user can determine
# what location they want to see information on
def display_id_location():
    display_list = []
    id_location = Results.select()

    for i in id_location:
        display_list.append(f'{i.id}      {i.location}     {i.date_saved}')

    # for testing... remove in final product
    print(display_list)

    return display_list


# save all api_data, and location and generate the date data was saved
def save_api_info(city_state, earthquake_result, aqi_result, flood_result):
    new_entry = Results(
                        location=city_state,
                        date_saved=datetime.date.today(),
                        aqi=aqi_result,
                        earthquakes=earthquake_result,
                        flood=flood_result)
    new_entry.save()



# retrieves the table row by id number.
# the idea is that user enters what id they want to access data from
# and returns a dictionary of its respective field.
# will make displaying information easier in bookmarks page
def get_api_info(db_id):
    result = Results.get_by_id(db_id)

    return {'location': result.location,
            'date': result.date_saved,
            'aqi': result.aqi,
            'earthquake': result.earthquakes,
            'flood': result.flood
            }





# remove in final product
if __name__ == '__main__':
    main()








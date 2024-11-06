import requests
import unittest
from unittest import TestCase
from unittest.mock import patch, Mock
from peewee import SqliteDatabase

import geocoding as gc
import air_pollution_api as ap
import earthquake_api as eq
import api_flood as af
import db


class TestGeocoding(TestCase):

    def test_valid_location(self):
        """Test if a valid location returns valid coordinates."""
        location = "Minneapolis, MN"
        expected_coords = [44.9774859, -93.2643669]
        coords = gc.getCoordinates(location)
        self.assertEqual(coords, expected_coords)

    def test_invalid_location(self):
        """Test if an invalid location input raises a LocationNotFoundError."""
        location = "Ddsiaofjdmiofrejaif oiijcidojcsaoicdmo#$@!$#!$"
        self.assertRaises(gc.LocationNotFoundError, gc.getCoordinates, location)


class TestAirQualityAPI(TestCase):
    # NOTE: set environment variables before running any API test cases!

    @classmethod
    def setUpClass(cls):
        # uses AQI for Minneapolis
        cls.mock_response_ok = {"list": [{"main": {"aqi": 2}}]}
        cls.mock_response_err = {"cod": 404, "message": "city not found"}

    @patch("air_pollution_api.requests.get")
    def test_valid_request(self, mock_get):
        """Test if a valid request to the air quality API receives
        a valid response.
        """
        # create a mock response object and set its body
        mock_response = Mock()
        mock_response.json.return_value = self.mock_response_ok
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Minneapolis coords
        coordinates = [44.9774859, -93.2643669]
        aqi = ap.get_air_pollution(coordinates)

        self.assertEqual(aqi, 2)

    @patch("air_pollution_api.requests.get")
    def test_invalid_request(self, mock_get):
        """Test if an invalid request raises AirPollutionAPIError."""
        mock_response = Mock()
        mock_response.json.return_value = self.mock_response_err
        mock_response.raise_for_status.side_effect = requests.HTTPError(
            "404 Client Error"
        )
        mock_get.return_value = mock_response

        coordinates = [0, 0]

        # use the context manager to "catch" any exceptions
        with self.assertRaises(ap.AirPollutionAPIError) as context:
            ap.get_air_pollution(coordinates)

        # and access them from the context object
        self.assertIn("Unable to fetch air quality data", str(context.exception))

    @patch.dict("os.environ", {}, clear=True)
    def test_missing_api_key(self):
        """Test if an AirPollutionAPIError is raised when no API key is set."""
        coordinates = [45, -93]

        with self.assertRaises(ap.AirPollutionAPIError) as context:
            ap.get_air_pollution(coordinates)

        self.assertIn("Did you set OWM_API_KEY?", str(context.exception))


class TestEarthquakeAPI(TestCase):
    # NOTE: set environment variables before running any API test cases!

    @classmethod
    def setUpClass(cls):
        cls.coordinates = [45, -93]
        cls.mock_response_ok = {
            "metadata": {"count": 2},
            "features": [
                {
                    "properties": {
                        "place": "128km SSW of Poland",
                        "mag": 2.4,
                        "time": 1388620296020,
                    }
                }
            ],
        }
        cls.mock_good_data = [
            "128km SSW of Poland | Earthquake Date: 2014-01-01 | Magnitude: 2.4"
        ]

    @patch("earthquake_api.requests.get")
    def test_valid_request(self, mock_get):
        """Test if a valid request to the earthquake API receives
        a valid response.
        """
        mock_response = Mock()
        mock_response.json.return_value = self.mock_response_ok
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response = eq.earthquake_main(*self.coordinates)

        self.assertEqual(response, self.mock_good_data)


class TestFloodAPI(TestCase):
    # NOTE: set environment variables before running any API test cases!

    @classmethod
    def setUpClass(cls):
        cls.coordinates = [45, -93]
        cls.mock_response_ok = {"result": {"flood.s_fld_haz_ar": [{"fld_zone": "A"}]}}

    @patch("api_flood.requests.get")
    def test_valid_request(self, mock_get):
        """Test if a valid request to the earthquake API receives
        a valid response.
        """
        mock_response = Mock()
        mock_response.json.return_value = self.mock_response_ok
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response = af.get_flood_risk(*self.coordinates)

        self.assertEqual(response, "NOT SAFE")
        

# use in-memory DB for testing
test_db = SqliteDatabase(":memory:")


class TestDatabase(TestCase):

    @classmethod
    def setUpClass(cls):
        # set up the test DB with our schema
        # keyword args ensure that Results will be bound to the test DB
        cls.database = test_db  # class-scope reference to the test DB
        db.db = cls.database  # override app.db with in-memory test DB
        db.db.bind([db.Results], bind_refs=False, bind_backrefs=False)
        db.db.connect()
        db.db.create_tables([db.Results])

    @classmethod
    def tearDownClass(cls):
        cls.database.close()

    def setUp(self):
        # begin() begins a transaction with manual committing
        self.database.begin()

    def tearDown(self):
        # roll back changes made during tests
        self.database.rollback()

    def test_get_api_info(self):
        db.save_api_info("Somewhere City", ["earthquake", "otherquake"], 100, "SAFE")
        saved_entry = db.Results.get(db.Results.location == "Somewhere City")
        retrieved_data = db.get_api_info(saved_entry.id)

        self.assertEqual(retrieved_data["location"], "Somewhere City")
        self.assertEqual(retrieved_data["earthquake"], ["earthquake", "otherquake"])

    def test_save_api_info(self):
        db.save_api_info("Somewhere City", ["earthquake", "otherquake"], 100, "SAFE")
        saved_entry = db.Results.get(db.Results.location == "Somewhere City")

        self.assertEqual(saved_entry.location, "Somewhere City")
        self.assertEqual(saved_entry.aqi, 100)
        self.assertEqual(
            saved_entry.earthquakes, "earthquake@otherquake"
        )  # how the earthquake list is represented in the DB
        self.assertEqual(saved_entry.flood, "SAFE")

    def test_display_id_location(self):
        db.save_api_info("City 1", [], 10, "SAFE")
        db.save_api_info("City 2", ["earthquake"], 30, "unknown flood risk")
        output = db.display_id_location()

        self.assertIn("City 1", output[0])
        self.assertIn("City 2", output[1])


if __name__ == "__main__":
    unittest.main()

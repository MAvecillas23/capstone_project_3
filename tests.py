import requests
import unittest
from unittest import TestCase
from unittest.mock import patch, Mock

import geocoding as gc
import air_pollution_api as ap
import earthquake_api as eq
import api_flood as af


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

        with self.assertRaises(ap.AirPollutionAPIError) as context:
            ap.get_air_pollution(coordinates)

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
            "Location: 128km SSW of Poland Date: 2014-01-01Magnitude: 2.4"
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

        self.assertEqual(response, "not safe")


if __name__ == "__main__":
    unittest.main()

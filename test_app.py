import requests
import json
import unittest


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://127.0.0.1:5000"

    def test_insert_data(self):
        data = {
            "dim": [
                {"key": "device", "val": "mobile"},
                {"key": "country", "val": "US"}
            ],
            "metrics": [
                {"key": "webreq", "val": 70},
                {"key": "timespent", "val": 302}
            ]
        }
        response = requests.post(f"{self.base_url}/v1/insert", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Data inserted successfully."})

    def test_query_data(self):
        data = {
            "dim": [
                {"key": "device", "val": "mobile"},
                {"key": "country", "val": "US"}
            ]
        }
        response = requests.post(f"{self.base_url}/v1/query", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"webreq": 70, "timespent": 302})

    def test_query_data_non_existing_dimensions(self):
        data = {
            "dim": [
                {"key": "device", "val": "desktop"},
                {"key": "country", "val": "IN"}
            ]
        }
        response = requests.post(f"{self.base_url}/v1/query", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "No data found for the specified dimensions."})


if __name__ == '__main__':
    unittest.main()

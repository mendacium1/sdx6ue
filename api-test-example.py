import unittest
import requests

class TestRecipeAPI(unittest.TestCase):
    API_URL = "http://localhost:8080/recipes"

    def test_get_all_recipes(self):
        response = requests.get(self.API_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

if __name__ == '__main__':
    unittest.main()

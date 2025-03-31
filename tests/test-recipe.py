import unittest
import requests
import time

class TestRecipeAPI(unittest.TestCase):
    BASE_URL = "http://localhost:8080"
    RECIPES_URL = f"{BASE_URL}/recipes"
    HEALTH_URL = f"{BASE_URL}/health"

    def setUp(self):
        self.wait_for_service()
        self.sample_recipe = {
            "name": "Spaghetti Bolognese",
            "description": "A classic Italian pasta dish",
            "ingredients": ["spaghetti", "ground beef", "tomato sauce"]
        }

    def wait_for_service(self, timeout=20):
        print("Waiting for /health endpoint to return 200...")
        for _ in range(timeout):
            try:
                response = requests.get(self.HEALTH_URL)
                if response.status_code == 200:
                    print("Service is up!")
                    return
            except requests.exceptions.ConnectionError:
                pass
            time.sleep(1)
        raise RuntimeError("Timed out waiting for the service to become ready.")

    def test_create_and_fetch_recipe(self):
        # Create a new recipe
        post_response = requests.post(self.RECIPES_URL, json=self.sample_recipe)
        self.assertEqual(post_response.status_code, 200)

        created_recipe = post_response.json()
        self.assertIn("ID", created_recipe)
        self.assertEqual(created_recipe["name"], self.sample_recipe["name"])
        self.assertEqual(created_recipe["description"], self.sample_recipe["description"])
        self.assertEqual(created_recipe["ingredients"], self.sample_recipe["ingredients"])

        created_id = created_recipe["ID"]

        # Fetch all recipes
        get_response = requests.get(self.RECIPES_URL)
        self.assertEqual(get_response.status_code, 200)

        recipes = get_response.json()
        self.assertIsInstance(recipes, list)

        found = any(
            r["ID"] == created_id and r["name"] == self.sample_recipe["name"]
            for r in recipes
        )
        self.assertTrue(found, "Created recipe not found in recipe list")

if __name__ == '__main__':
    unittest.main()


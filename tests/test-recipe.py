import unittest
import requests
import time

class TestRecipeAPI(unittest.TestCase):
    BASE_URL = "http://localhost:8080" # Basis-URL der API
    RECIPES_URL = f"{BASE_URL}/recipes" # Endpoint für Rezepte
    HEALTH_URL = f"{BASE_URL}/health" # Healthcheck-Endpoint

    def setUp(self):
        self.wait_for_service() # Warte auf API-Verfügbarkeit
        self.sample_recipe = { # Beispielrezept
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
        # Rezept erstellen
        post_response = requests.post(self.RECIPES_URL, json=self.sample_recipe)
        self.assertEqual(post_response.status_code, 200)

        created_recipe = post_response.json()
        self.assertIn("ID", created_recipe)
        self.assertEqual(created_recipe["name"], self.sample_recipe["name"])
        self.assertEqual(created_recipe["description"], self.sample_recipe["description"])
        self.assertEqual(created_recipe["ingredients"], self.sample_recipe["ingredients"])

        created_id = created_recipe["ID"]

        # Alle Rezepte abrufen
        get_response = requests.get(self.RECIPES_URL)
        self.assertEqual(get_response.status_code, 200)

        recipes = get_response.json()
        self.assertIsInstance(recipes, list)

        # Geprüft: Rezept mit richtiger ID vorhanden
        found = any(
            r["ID"] == created_id and r["name"] == self.sample_recipe["name"]
            for r in recipes
        )
        self.assertTrue(found, "Created recipe not found in recipe list")

    def test_create_multiple_recipes_and_fetch_all(self):
        recipes_to_create = [
            {"name": "Pizza Margherita", "description": "Classic pizza", "ingredients": ["flour", "tomato", "cheese"]},
            {"name": "Caesar Salad", "description": "Fresh salad", "ingredients": ["lettuce", "chicken", "parmesan"]}
        ]

        for recipe in recipes_to_create:
            r = requests.post(self.RECIPES_URL, json=recipe)
            self.assertEqual(r.status_code, 200)

        get_response = requests.get(self.RECIPES_URL)
        self.assertEqual(get_response.status_code, 200)

        all_recipes = get_response.json()
        self.assertGreaterEqual(len(all_recipes), 2)  # Es sollten mindestens 2 drin sein

    def test_fetch_single_recipe_by_id(self):
        r = requests.post(self.RECIPES_URL, json=self.sample_recipe)
        self.assertEqual(r.status_code, 200)
        recipe_id = r.json()["ID"]

        r2 = requests.get(f"{self.RECIPES_URL}/{recipe_id}")
        self.assertEqual(r2.status_code, 200)
        fetched = r2.json()
        self.assertEqual(fetched["name"], self.sample_recipe["name"])


if __name__ == '__main__':
    unittest.main(verbosity=2) # Testlauf starten


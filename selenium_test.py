import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

localhost = "http://127.0.0.1:5000"

class TestSelenium(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.base_url = localhost

    def tearDown(self):
        self.driver.quit()

    # Test landing page is login
    def test_home_page(self):
        self.driver.get(self.base_url)
        self.assertIn("Login", self.driver.title)  # Check title of HTML
        heading = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(heading.text, "Welcome to ChatSome!")

if __name__ == '__main__':
    unittest.main()
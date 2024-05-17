import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    # Test for valid registration
    def test_registration(self):
        driver = self.driver
        driver.get(f"{self.base_url}/register")
        driver.find_element(By.ID, "uName").send_keys("test_user")
        driver.find_element(By.ID, "password").send_keys("password")
        driver.find_element(By.ID, "retypePassword").send_keys("password")
        driver.find_element(By.ID, "submit-btn").click()

        # Wait for redirection to the login page
        WebDriverWait(driver, 10).until(EC.title_contains("Login"))

        # Check that it is redirected to the login page
        self.assertIn("Login", driver.title)


if __name__ == '__main__':
    unittest.main()
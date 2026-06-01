from .base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from utils.browser import make_chrome_browser
import pytest
from unittest.mock import patch
from selenium.webdriver.common.keys import Keys


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def testing(self):
        browser = make_chrome_browser()
        browser.get(self.live_server_url)
        

    @patch('recipes.views.PER_PAGES', new=2)
    def test_recipe_search_input_finds_correct_recipes(self):
        recipes = self.make_recipe_in_batch()
        self.browser.get(self.live_server_url)
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a new experience..."]')
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)
        self.sleep(5)
        

from typing import Callable, Any
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait 


def build_driver(url:str):
    """
    Builds and connects a driver to a given url
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    return driver


def set_keys_for_item(item, *args):
    """
    Given an item and keys, send them to the item one by one
    """
    for arg in args:
        item.send_keys(arg)
    

def find_items_matching_all(driver,tag_name: str,  attributes: dict[str, str] = dict()):
    """
    Given current driver state, find all items with a said tag_name and an attribute matching any of requested attributes 
    """
    matches = []
    for item in driver.find_elements(By.TAG_NAME, tag_name):
        item_matches = True
        for k, v in attributes.items():
            value = item.get_attribute(k)
            if value is None or value != v:
                item_matches = True 
                break 
        if item_matches:
            matches.append(item)
    return matches


def click_by_action(driver, element):
    """
    Use action to click on a given element
    """
    ActionChains(driver).click(on_element=element).perform()


def sleep(driver, timeout: float, condition: Callable[[Any],bool]):
    """
    Wait for a condition or timeout
    Do NOT use time.sleep() but a driver sleep.
    """
    WebDriverWait(driver, timeout).until(condition)

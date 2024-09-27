from operations import *

driver = build_driver("https://www.google.fr")
WebDriverWait(driver, 12.1).until(lambda x:False)


#for item in find_items_matching_all(driver, "textarea", {"title": "Rechercher"}):
#    item.send_keys("Paris")
#    WebDriverWait(12.1).until(False)
#    item.send_keys(Keys.ENTER)

    
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

# build options 
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--start-maximized")
# launch driver
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(2)
start_url = "https://fr.yahoo.com/"
driver.get(start_url)
with open("./test.html","wb") as f:
    f.write(driver.page_source.encode("utf-8"))
driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Start a new browser session
driver = webdriver.Chrome()  # or any other webdriver you prefer, e.g., Firefox, Edge, etc.

# Open a webpage
driver.get("https://example.com")

try:
    # Wait for the element to be clickable (you can change the timeout as needed)
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='your_element_id']"))
    )
    
    # Once the element is clickable, click it
    element.click()
    
    # You can perform further actions after clicking the element
    
finally:
    # Close the browser session
    driver.quit()

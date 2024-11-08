from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def check_class_availability():
    # Set up Selenium with headless Chrome if you want it to run in the background
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Replace '/path/to/chromedriver' with the path to your downloaded ChromeDriver
    service = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = 'https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=A&catalogNbr=340&honors=F&promod=F&searchType=all&subject=CSE&term=2251'
    driver.get(url)

    # Wait for the page to load JavaScript content
    time.sleep(5)

    # Now we can try to find the elements
    try:
        # Example: Adjust this selector as needed based on your HTML structure
        classes = driver.find_elements(By.CLASS_NAME, 'class-results-cell')
        for class_div in classes:
            seat_info = class_div.text
            print(seat_info)  # Modify as per the exact format you want to extract
    except Exception as e:
        print(f"Error locating class data: {e}")
    finally:
        driver.quit()

check_class_availability()

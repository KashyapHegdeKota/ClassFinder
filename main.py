from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def check_class_availability(classCode):
    # Set up Selenium with Chrome without headless mode for debugging
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # Set up ChromeDriver path
    service = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Construct the URL
    classNum = classCode[3:]
    classTitle = classCode[:3].upper()
    url = f'https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=A&catalogNbr={classNum}&honors=F&promod=F&searchType=all&subject={classTitle}&term=2251'
    driver.get(url)

    # Wait for the page to load JavaScript content
    time.sleep(1)  # Adjust time as needed

    output_string = ""  # Initialize an empty string to store output
    seen_courses = set()  # Track unique class numbers

    try:
        # Find all rows of class data within the main results div
        class_rows = driver.find_elements(By.CLASS_NAME, 'focus')
        
        for row in class_rows:
            # Initialize a dictionary to store details of each class
            class_info = {
                'Course': row.find_element(By.XPATH, "//*[@id=\"class-results\"]/div/div[5]/div[1]").text,
                'Title': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[2]').text,
                'Number': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[4]').text,
                'Instructor': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[5]').text,
                'Days': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[6]').text,
                'Start': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[8]').text,
                'End': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[10]').text,
                'Location': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[11]').text,
                'Dates': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[12]').text,
                'Units': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[13]').text,
                'Seats': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[14]').text,
            }
            # Check if this course number has already been processed
            if class_info['Number'] not in seen_courses:
                seen_courses.add(class_info['Number'])  # Mark this class as seen
                # Append the class info to the output string
                output_string += "Class Info:\n"
                for key, value in class_info.items():
                    output_string += f"{key}: {value}\n"
                output_string += "-" * 40 + "\n"

    except Exception as e:
        print(f"Error locating class data: {e}")
    finally:
        driver.quit()

    return output_string

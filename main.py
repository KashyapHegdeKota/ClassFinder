from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def check_class_availability(classCode):
    # Set up Selenium with Chrome without headless mode for debugging
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

    classCode_list = [None]*6
    indx =0
    for i in classCode.upper():
        classCode_list[indx] = i
        indx+=1
    classNum = classCode_list[3]+classCode_list[4]+classCode_list[5]
    classTitle = classCode_list[0]+classCode_list[1]+classCode_list[2]
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'user-agent={user_agent}')

    
    # Replace './chromedriver.exe' with the path to your downloaded ChromeDriver
    service = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = f'https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=A&catalogNbr={classNum}&honors=F&promod=F&searchType=all&subject={classTitle}&term=2251'
    driver.get(url)

    # Wait for the page to load JavaScript content
    time.sleep(1)  # Adjust time as needed to allow content to load fully

    class_list = []  # This will hold all class dictionaries

    try:
        # Find all rows of class data within the main results div
        class_rows = driver.find_elements(By.CLASS_NAME, 'focus')  # Using 'focus' or 'class-results-cell' for each entry
        
        for row in class_rows:
            # Initialize a dictionary to store details of each class
            class_info = {
                'Course':row.find_element(By.XPATH, "//*[@id=\"class-results\"]/div/div[5]/div[1]").text,
                'Title': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[2]').text,
                'Number': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[3]').text,
                'Instructor': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[4]').text,
                'Days': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[5]').text,
                'Start': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[6]').text,
                'End': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[7]').text,
                'Location': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[8]').text,
                'Dates': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[9]').text,
                'Units': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[10]').text,
                'Seats': row.find_element(By.XPATH, '//*[@id="class-results"]/div/div[2]/div[11]').text,

            }
            
            # Append the class info to the list
            class_list.append(class_info)

    except Exception as e:
        print(f"Error locating class data: {e}")
    finally:
        driver.quit()

    # Print the grouped information
    for class_info in class_list:
        print("Class Info:")
        for key, value in class_info.items():
            print(f"{key}: {value}")
        print("-" * 40)

check_class_availability('cse230') 
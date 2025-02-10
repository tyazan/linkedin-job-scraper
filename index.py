import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

# Set the path to the ChromeDriver executable
path = './chromedriver-win32/chromedriver.exe'

# Create a new Service object
service = Service(path)

# Start the service
service.start()

# Create a new ChromeDriver instance using the service object
driver = webdriver.Chrome(service=service)

#options = webdriver.ChromeOptions()
#options.add_argument("--headless")
#driver = webdriver.Chrome(options=options, service=service)

# Maximize Window
driver.maximize_window() 
driver.minimize_window() 
driver.maximize_window() 
driver.switch_to.window(driver.current_window_handle)
driver.implicitly_wait(10)

# Enter to the site
driver.get('https://www.linkedin.com/login');
time.sleep(2)

# User Credentials
# Reading txt file where we have our user credentials
with open('user_credentials.txt', 'r',encoding="utf-8") as file:
    user_credentials = file.readlines()
    user_credentials = [line.rstrip() for line in user_credentials]
user_name = user_credentials[0] # First line
password = user_credentials[1] # Second line
driver.find_element("xpath", '//*[@id="username"]').send_keys(user_name)
driver.find_element("xpath", '//*[@id="password"]').send_keys(password)
time.sleep(1)

# Login button
driver.find_element(By.XPATH, '//button[@data-litms-control-urn="login-submit"]').click()
driver.implicitly_wait(30)

# Access to the Jobs button and click it
driver.find_element("xpath", '//*[@id="global-nav"]/div/nav/ul/li[3]/a').click()
time.sleep(3)

# Go to search results directly via link
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3733045302&distance=25&f_TPR=r86400&geoId=101282230&keywords=full%20stack%20engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER")
time.sleep(2)
links=[]
for i in range(2,13):
    str_log = f"Fethcing the links in page {str(i-1)}"
    print(str_log)
    jobs_block = driver.find_element(By.CLASS_NAME, "scaffold-layout__list")
    jobs_list= jobs_block.find_elements(By.CSS_SELECTOR, '.scaffold-layout__list-item')

    
    for job in jobs_list:

        all_links = job.find_elements(By.TAG_NAME, 'a')
        for a in all_links:
            if str(a.get_attribute('href')).startswith("https://www.linkedin.com/jobs/view") and a.get_attribute('href') not in links: 
                links.append(a.get_attribute('href'))
                print('Found ' + a.get_attribute('href') + ' links for job offers')

            else:
                pass
        # scroll down for each job element
        driver.execute_script("arguments[0].scrollIntoView();", job)
    # go to next page:
    xpath_str  = f"//button[@aria-label='Page {str(i)}']"
    print(xpath_str)
    driver.find_element("xpath", xpath_str).click()

str_result_fetching_data=f"Found {len(links)} links for job offers"
time.sleep(3)

print('Found ' + str(len(links)) + ' links for job offers')

# Create a dictionary with the column names and data
data = {'Index': range(1, len(links)+1),
        'Job link': links}

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel('job_list_links_germany.xlsx', index=False)



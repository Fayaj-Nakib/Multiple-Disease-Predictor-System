import random
import time
from telnetlib import EC

from pyhtmlreport import Report
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

report = Report()


service = Service("F:\chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service)

#driver: WebDriver = webdriver.Chrome(executable_path="F:\chromedriver\chromedriver.exe")
report.setup(
report_folder=r'Reports',
module_name='Device',
release_name='Test V1',
selenium_driver=driver
)
driver.get('http://192.168.31.220:8501')


time.sleep(5)

# Test Case 01
try:
    report.write_step(
    'Go to Landing Page',
    status=report.status.Start,
    test_number=1
    )
    #assert (driver.title == 'multiple_disease_prediction · Streamlit')
    report.write_step(
    'Landing Page loaded Successfully.',
    status=report.status.Pass,
    screenshot=True
    )
except AssertionError:
    report.write_step(

    'Landing Page loaded Successfully.',
    status=report.status.Fail,
    screenshot=True
    )
except Exception as e:
    report.write_step(
    'Something went wrong!</br>{e}',
    status=report.status.Warn,
    screenshot=True
)


# Test Case 02
try:
    report.write_step(
        'Signup for a user',
        status=report.status.Start,
        test_number=2
    )

        # Wait for the element to be present in the DOM

    driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/ul/li[3]/a').click()

    driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div/div/div/section[2]/div[1]/div[1]/div/div[3]/div/div[1]/div/input').send_keys('apu')
    driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div/div/div/section[2]/div[1]/div[1]/div/div[4]/div/div[1]/div/input').send_keys('123')

    # Click on the button
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[1]/div[1]/div/div[5]/div/button')))
    button.click()



    report.write_step(
        'Successfully Signup ',
        status=report.status.Pass,
        screenshot=True
    )

except AssertionError:
    report.write_step(
        'Failed to Signup',
        status=report.status.Fail,
        screenshot=True
    )

except Exception as e:
    report.write_step(
        f'Something went wrong!</br>{e}',
        status=report.status.Warn,
        screenshot=True
    )

# Test Case 03
try:
    report.write_step(
    'Login for a user',
    status=report.status.Start,
    test_number=3
    )
    driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/ul/li[2]/a').click()

    driver.find_element(By.XPATH,'/html/body/div/div[1]/div[1]/div/div/div/section[1]/div[1]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/input').send_keys('aa')
    driver.find_element(By.XPATH,'/html/body/div/div[1]/div[1]/div/div/div/section[1]/div[1]/div[2]/div/div[1]/div/div[3]/div/div[1]/div/input').send_keys('123')

    driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div/div/div/section[1]/div[1]/div[2]/div/div[1]/div/div[4]/div/label/input').click()

    report.write_step(
    'Successfully login ',
    status=report.status.Pass,
    screenshot=True
    )
except AssertionError:
    report.write_step(
    'Failed to login',
    status=report.status.Fail,
    screenshot=True
    )
except Exception as e:
    report.write_step(
    'Something went wrong!</br>{e}',
    status=report.status.Warn,

    screenshot=True
    )

# Test Case 04
try:
    report.write_step(
    ' Diabetes Prediction ',
    status=report.status.Start,
    test_number=4
    )

    driver.find_element(By.XPATH,
    '/html/body/div/div/div/div/div/ul/li[1]/a').click()

    report.write_step(
    'Successfully ',
    status=report.status.Pass,
    screenshot=True
    )
except AssertionError:
    report.write_step(
    '',
    status=report.status.Fail,
    screenshot=True
    )
except Exception as e:
    report.write_step(
    'Something went wrong!</br>{e}',
    status=report.status.Warn,
    screenshot=True
    )

# Test Case 05
try:
    report.write_step(
    '  Heart Disease Prediction ',
    status=report.status.Start,
    test_number=5
    )

    driver.find_element(By.XPATH,
    '/html/body/div/div/div/div/div/ul/li[2]/a').click()

    report.write_step(
    'Successfully ',
    status=report.status.Pass,
    screenshot=True
    )
except AssertionError:
    report.write_step(
    'Failed ',
    status=report.status.Fail,
    screenshot=True
    )
except Exception as e:
    report.write_step(
    'Something went wrong!</br>{e}',
    status=report.status.Warn,
    screenshot=True
    )

# Test Case 06
try:
    report.write_step(
    '  Parkinsons Prediction ',
    status=report.status.Start,
    test_number=6
    )

    driver.find_element(By.XPATH,
    '/html/body/div/div/div/div/div/ul/li[3]/a').click()

    report.write_step(
    'Successfully',
    status=report.status.Pass,
    screenshot=True
    )
except AssertionError:
    report.write_step(
    'Failed ',
    status=report.status.Fail,
    screenshot=True
    )
except Exception as e:
    report.write_step(
    'Something went wrong!</br>{e}',
    status=report.status.Warn,
    screenshot=True
    )

# Test Case 07
try:
    report.write_step(
    '  Lung Cancer Prediction ',
    status=report.status.Start,
    test_number=7
    )

    driver.find_element(By.XPATH,'/html/body/div/div/div/div/div/ul/li[4]/a').click()

    report.write_step(
    'Successfully ',
    status=report.status.Pass,
    screenshot=True
    )
except AssertionError:
    report.write_step(
    'Failed ',
    status=report.status.Fail,
    screenshot=True
    )
except Exception as e:
    report.write_step(
    'Something went wrong!</br>{e}',
    status=report.status.Warn,
    screenshot=True
    )

# Test Case 08
try:
    report.write_step(
    ' profile ',
    status=report.status.Start,
    test_number=8
    )

    driver.find_element(By.XPATH,
    '/html/body/div/div/div/div/div/ul/li[5]').click()

    report.write_step(
    'Successfully',
    status=report.status.Pass,
    screenshot=True
    )
except AssertionError:
    report.write_step(
    'Failed',
    status=report.status.Fail,
    screenshot=True
    )
except Exception as e:
    report.write_step(
    'Something went wrong!</br>{e}',
    status=report.status.Warn,
    screenshot=True
    )
#finally:
report.generate_report()
driver.quit()
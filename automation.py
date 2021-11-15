from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# create a webdriver object and set options for headless browsing
options = Options()
# options.headless = True
driver = webdriver.Chrome('./chromedriver.exe', options=options)
department_url = 'https://engineering.nyu.edu/academics/departments/chemical-and-biomolecular-engineering'
driver.get(department_url)
faculty_page = driver.find_element_by_xpath(
    '//a[contains(@href,"people")]').click()
links = driver.find_elements_by_xpath(
    '//a[contains(@href,"/faculty/")]')
# links = [elem.get_attribute('href') for elem in link]

links_arr = []
for link in links:
    links_arr.append(link.get_attribute('href'))

# with open("bios_url.txt", 'w') as f:
for link in links_arr:
    driver.get(link)
    bio = driver.find_element_by_class_name('content-body')
    print(bio.text)
    break

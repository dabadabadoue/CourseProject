from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# create a webdriver object and set options for headless browsing
options = Options()
options.headless = True
driver = webdriver.Chrome('./chromedriver.exe', options=options)
department_url = 'https://engineering.nyu.edu/academics/departments/chemical-and-biomolecular-engineering/people'
driver.get(department_url)
# faculty_page = driver.find_element_by_xpath(
#     '//a[contains(@href,"people")]').click()
links = driver.find_elements_by_xpath(
    '//a[contains(@href,"/faculty/")]')

image_alts = driver.find_elements_by_tag_name("img")
image_alts_text = []
for image_alt in image_alts:
    cur_alt = image_alt.get_attribute("alt")
    if cur_alt is not None:
        image_alts_text.append((''.join(filter(str.isalnum, cur_alt))).lower())

links = driver.find_elements_by_tag_name("a")
links_arr = []
all_links_arr = []
all_links_normal = []
for link in links:
    cur_link = link.get_attribute('href')
    if cur_link is not None:
        links_arr.append((''.join(filter(str.isalnum, cur_link))).lower())
        all_links_arr.append((''.join(filter(str.isalnum, cur_link))).lower())
        all_links_normal.append((cur_link).lower())

faculty_links = []
# # possible faculty keywords: faculty, people, staff
faculty_keywords = ["faculty", "staff", "people"]
faculty_links = []
i = 1
for alt in image_alts_text:
    cur_link = [s for s in links_arr if (alt in s and alt != "")]
    if type(cur_link) == list:
        cur_link = list(set(cur_link))
        cur_faculty_link = []
        for word in faculty_keywords:
            cur_faculty_link = [s for s in cur_link if word in s]
            if cur_faculty_link is not None:
                for link in cur_faculty_link:
                    faculty_links.append(link)
    else:
        faculty_links.append(cur_link)

faculty_links = list(filter(None, faculty_links))
if len(faculty_links) > 0:
    print("Page is a faculty webpage")
else:
    print("Page is not a faculty webpage")


final_arr = []
for i in range(len(all_links_arr)):
    if all_links_arr[i] in faculty_links:
        final_arr.append(all_links_normal[i])

final_arr = list(set(final_arr))


with open("bios_url.txt", 'w') as f:
    for link in final_arr:
        f.write(link)
        f.write('\n')

# code for getting bios from each bio url
with open("bios.txt", 'w') as f:
    for link in final_arr:
        driver.get(link)
        bio = driver.find_element_by_class_name('content-body')
        f.write(link)
        f.write('\n')
        bio_text = bio.text
        bio_text = bio_text.split('\n')
        non_empty_lines = [line for line in bio_text if line.strip() != ""]
        bio_without_empty_lines = ""
        for line in non_empty_lines:
            bio_without_empty_lines += line + "\n"
        f.write(bio_without_empty_lines)
        f.write('\n')
        f.write('\n')

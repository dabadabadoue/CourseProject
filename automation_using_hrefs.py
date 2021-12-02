from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# create a webdriver object and set options for headless browsing
options = Options()
options.headless = True
driver = webdriver.Chrome('./chromedriver.exe', options=options)
department_url = 'https://cse.engin.umich.edu/people/faculty/'
driver.get(department_url)
# faculty_page = driver.find_element_by_xpath(
#     '//a[contains(@href,"people")]').click()
links = driver.find_elements_by_xpath(
    '//a[contains(@href,"/faculty/")]')


images = driver.find_elements_by_tag_name("img")
image_src_text = []
for image_src in images:
    cur_src = image_src.get_attribute("src")
    if cur_src is not None:

        # cur_src = (''.join(filter(str.isalnum, cur_src))).lower()
        # print(cur_src)
        last_slash_idx = cur_src.rfind('/')
        last_dot_idx = cur_src.rfind('.')
        cur_src = cur_src[last_slash_idx:last_dot_idx]
        cur_src = (''.join(filter(str.isalnum, cur_src))).lower()
        image_src_text.append(cur_src)
        # image_alts_text.append((''.join(filter(str.isalnum, cur_src))).lower())
# print("num images: " + str(len(image_src_text)))
links = driver.find_elements_by_tag_name("a")
links_arr = []
all_links_arr = []
all_links_normal = []
faculty_keywords = ["faculty", "staff", "people"]
for link in links:
    cur_link = link.text
    url = link.get_attribute('href')
    if cur_link is not None and url is not None:
        cur_url = (''.join(filter(str.isalnum, url))).lower()
        for word in faculty_keywords:
            if(word in cur_url):
                links_arr.append(
                    (''.join(filter(str.isalnum, cur_link))).lower())
                all_links_normal.append(url)

faculty_links = []
# # possible faculty keywords: faculty, people, staff

i = 1
temp_names = []
for src in image_src_text:
    cur_link = [s for s in links_arr if (src in s and src != "")]
    if(not cur_link):
        cur_link = [s for s in links_arr if (src[1:] in s and src != "")]
    for link in cur_link:
        temp_names.append(link)
        # print(link)
    # if type(cur_link) == list:
    #     cur_link = list(set(cur_link))
    #     cur_faculty_link = []
    #     for word in faculty_keywords:
    #         cur_faculty_link = [s for s in cur_link if word in s]
    #         if cur_faculty_link is not None:
    #             for link in cur_faculty_link:
    #                 faculty_links.append(link)
    # else:
    #     faculty_links.append(cur_link)
temp_names = list(set(temp_names))

print(temp_names)
print("num faculty: " + str(len(temp_names)))
faculty_links = list(filter(None, faculty_links))
if len(temp_names) > 0:
    print("Page is a faculty webpage")
else:
    print("Page is not a faculty webpage")

driver.close()

# final_arr = []
# for i in range(len(all_links_normal)):
#     # if all_links_arr[i] in faculty_links:
#     final_arr.append(all_links_normal[i])

# final_arr = list(set(final_arr))


# with open("faculty_urls.txt", 'w') as f:
#     for link in all_links_normal:
#         f.write(link)
#         f.write('\n')

with open("faculty_names.txt", 'w') as f:
    for link in temp_names:
        f.write(link)
        f.write('\n')

# # code for getting bios from each bio url
# with open("bios.txt", 'w') as f:
#     for link in final_arr:
#         driver.get(link)
#         bio = driver.find_element_by_class_name('content-body')
#         f.write(link)
#         f.write('\n')
#         bio_text = bio.text
#         bio_text = bio_text.split('\n')
#         non_empty_lines = [line for line in bio_text if line.strip() != ""]
#         bio_without_empty_lines = ""
#         for line in non_empty_lines:
#             bio_without_empty_lines += line + "\n"
#         f.write(bio_without_empty_lines)
#         f.write('\n')
#         f.write('\n')

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

images = driver.find_elements_by_tag_name("img")
image_alts_text = []
image_srcs = []
for image in images:
    cur_alt = image.get_attribute("alt")
    cur_src = image.get_attribute("src")
    if cur_alt is not None:
        image_alts_text.append((''.join(filter(str.isalnum, cur_alt))).lower())
    if cur_src is not None:

        # cur_src = (''.join(filter(str.isalnum, cur_src))).lower()
        # print(cur_src)
        last_slash_idx = cur_src.rfind('/')
        last_dot_idx = cur_src.rfind('.')
        cur_src = cur_src[last_slash_idx:last_dot_idx]
        cur_src = (''.join(filter(str.isalnum, cur_src))).lower()
        image_srcs.append(cur_src)

links = driver.find_elements_by_tag_name("a")
links_arr = []
all_links_arr = []
all_links_normal = []
important_link_text_arr = []
idxs = []
i = 0
faculty_keywords = ["faculty", "staff", "people"]
for link in links:
    important_link_text = link.text
    url = link.get_attribute('href')
    if url is not None and important_link_text is not None:
        cur_url = (''.join(filter(str.isalnum, url))).lower()
        for word in faculty_keywords:
            if(word in cur_url):
                links_arr.append((''.join(filter(str.isalnum, url))).lower())
                all_links_arr.append(
                    (''.join(filter(str.isalnum, url))).lower())
                all_links_normal.append(url)
                important_link_text_arr.append(
                    (''.join(filter(str.isalnum, important_link_text))).lower())
                idxs = i
                i += 1


# # possible faculty keywords: faculty, people, staff

faculty_links = []
faculty_names = []
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
i = 0
for src in image_srcs:
    src_list = [s for s in important_link_text_arr if (src in s and src != "")]
    if(not src_list):
        src_list = [s for s in important_link_text_arr if (
            src[1:] in s and src != "")]
    for src in src_list:
        faculty_names.append(src)
        faculty_links.append(links_arr[i])
        all_links_arr.append(all_links_arr[i])
        all_links_normal.append(all_links_normal[i])


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

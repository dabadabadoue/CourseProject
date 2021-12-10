from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


# create a webdriver object and set options for headless browsing
options = Options()
options.headless = True
driver = webdriver.Chrome('./chromedriver.exe', options=options)
department_url = 'https://www.cs.purdue.edu/people/faculty/index.html'
driver.get(department_url)


class FacultyMember():
    def __init__(self, url, alphanum_url, img_alt, img_src, link_text, swapped_link_text, link_element):
        self.url = url
        self.alphanum_url = alphanum_url
        self.img_alt = img_alt
        self.img_src = img_src
        self.link_text = link_text
        self.swapped_link_text = swapped_link_text
        self.link_element = link_element


images = driver.find_elements_by_tag_name("img")
image_alts_text = []
image_srcs = []
for image in images:
    cur_alt = image.get_attribute("alt")
    cur_src = image.get_attribute("src")
    if cur_alt is not None:
        image_alts_text.append((''.join(filter(str.isalnum, cur_alt))).lower())
    if cur_src is not None:
        last_slash_idx = cur_src.rfind('/')
        last_dot_idx = cur_src.rfind('.')
        cur_src = cur_src[last_slash_idx:last_dot_idx]
        cur_src = (''.join(filter(str.isalnum, cur_src))).lower()
        image_srcs.append(cur_src)

faculty_links = driver.find_elements_by_xpath(
    '//a[contains(@href,"/faculty/")]')
faculty_links.extend(driver.find_elements_by_xpath(
    '//a[contains(@href,"/staff/")]'))
faculty_links.extend(driver.find_elements_by_xpath(
    '//a[contains(@href,"/people/")]'))

all_links = driver.find_elements_by_tag_name("a")

faculty_links_arr = []
rest_links_arr = []
all_links_normal = []
link_text_arr = []
link_text_swapped_arr = []
matches = []
idxs = []
i = 0

faculty_arr = []
maybe_faculty_arr = []
for link in faculty_links:
    important_link_text = link.text
    url = link.get_attribute('href')
    if url is not None and important_link_text is not None:
        cur_url = (''.join(filter(str.isalnum, url))).lower()
        important_link_text = (
            ''.join(filter(str.isalnum, important_link_text))).lower()
        comma_idx = important_link_text.find(",")
        swapped_link_text = "0"
        if comma_idx != -1:
            swapped_link_text = (''.join(filter(
                str.isalnum, important_link_text[comma_idx:] + important_link_text[:comma_idx]))).lower()
        faculty = FacultyMember(
            url, cur_url, "0", "0", important_link_text, swapped_link_text, link)
        faculty_arr.append(faculty)


titles = ["professor", "lecturer", "chair",
          "teacher", "instructor", "educator", "dean"]

faculty_urls = []

num_matches = 0
final_arr = []
titles_arr = []
for alt in image_alts_text:
    for faculty in faculty_arr:
        if alt != "" and alt in faculty.alphanum_url:
            faculty.img_alt = alt
            num_matches += 1
            final_arr.append(faculty.url)
            faculty_arr.remove(faculty)
            continue

        if alt != "" and alt in faculty.link_text:
            faculty.img_alt = alt
            num_matches += 1
            final_arr.append(faculty.url)
            faculty_arr.remove(faculty)
            continue

        if alt != "" and alt in faculty.swapped_link_text:
            faculty.img_alt = alt
            num_matches += 1
            final_arr.append(faculty.url)
            faculty_arr.remove(faculty)
            continue

for src in image_srcs:
    for faculty in faculty_arr:
        if src != "" and src in faculty.alphanum_url:
            faculty.img_src = src
            num_matches += 1
            final_arr.append(faculty.url)
            faculty_arr.remove(faculty)
            continue

        if src != "" and src in faculty.link_text:
            faculty.img_src = src
            num_matches += 1
            final_arr.append(faculty.url)
            faculty_arr.remove(faculty)
            continue

        if src != "" and src in faculty.swapped_link_text:
            faculty.img_src = src
            num_matches += 1
            final_arr.append(faculty.url)
            faculty_arr.remove(faculty)
            continue


for link in all_links:
    url = link.get_attribute('href')
    if url is not None and "pdf" not in url and "txt not in url" and "citation" not in url and "mailto" not in url:
        parent_element = link.find_element_by_xpath('..')
        grand_parent_element = parent_element.find_element_by_xpath(
            '..')
        found_url = False
        try:
            stuff = grand_parent_element.find_element_by_xpath(
                ".//div").text.lower()
            for title in titles:
                if title in stuff:
                    titles_arr.append(url)
                    found_url = True
                    break
        except NoSuchElementException:
            try:
                stuff = grand_parent_element.find_element_by_xpath(
                    ".//span").text.lower()
                for title in titles:
                    if title in stuff:
                        titles_arr.append(url)
                        found_url = True
                        break
            except NoSuchElementException:
                found_url = False
                # try:
                #     stuff = grand_parent_element.find_element_by_xpath(
                #         ".//p").text.lower()
                #     for title in titles:
                #         if title in stuff:
                #             titles_arr.append(url)
                #             found_url = True
                #             break
                # except NoSuchElementException:
                #     found_url = False

        if found_url is False:
            stuff = grand_parent_element.get_attribute(
                "innerHTML").strip().lower()
            for title in titles:
                if title in stuff:
                    stuff_idx = stuff.find(title)
                    if stuff_idx != -1:
                        tag_idx = stuff[stuff_idx:].find("<")
                        if tag_idx != -1:
                            starting_tag = stuff[tag_idx:]
                            if starting_tag[2] == "a":
                                titles_arr.append(url)
                                break

# for url1 in faculty_urls:
#     for url2 in faculty_urls:
#         if url1 in url2:
#             faculty_urls.remove(url1)

final_arr = list(set(filter(None, final_arr)))
titles_arr = list(set(filter(None, titles_arr)))

# print(final_arr)
# print(titles_arr)
for link in final_arr:
    if link not in titles_arr:
        final_arr.remove(link)
    #     print("not in " + link)
    # else:
    #     print("in " + link)

final_arr.extend(titles_arr)
final_arr = list(set(filter(None, final_arr)))

if len(final_arr) > 0:
    print("Page is a Directory Webpage")
else:
    print("Page is Not a Directory Webpage")


with open("bio_urls.txt", 'w') as f:
    for url in final_arr:
        f.write(url)
        f.write('\n')

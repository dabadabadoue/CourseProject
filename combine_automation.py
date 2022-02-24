from selenium.common.exceptions import NoSuchElementException


# faculty memeber struct to make data access easy
class FacultyMember():
    def __init__(self, url, alphanum_url, img_alt, img_src, link_text, swapped_link_text, link_element):
        self.url = url
        self.alphanum_url = alphanum_url
        self.img_alt = img_alt
        self.img_src = img_src
        self.link_text = link_text
        self.swapped_link_text = swapped_link_text
        self.link_element = link_element

# checks if given url from find_pages is a directory page
# returns list of all found faculty urls on page


def is_directory_page(driver, department_url):
    driver.get(department_url)
    # gets all images, saves alts and srcs to array
    images = driver.find_elements_by_tag_name("img")
    image_alts_text = []
    image_srcs = []
    for image in images:
        cur_alt = image.get_attribute("alt")
        cur_src = image.get_attribute("src")
        if cur_alt is not None:
            image_alts_text.append(
                (''.join(filter(str.isalnum, cur_alt))).lower())
        # parsing to get important data from url
        if cur_src is not None:
            last_slash_idx = cur_src.rfind('/')
            last_dot_idx = cur_src.rfind('.')
            cur_src = cur_src[last_slash_idx:last_dot_idx]
            cur_src = (''.join(filter(str.isalnum, cur_src))).lower()
            image_srcs.append(cur_src)

    # gets all links on page containing relevant keywords
    faculty_links = driver.find_elements_by_xpath(
        '//a[contains(@href,"faculty")]')
    faculty_links.extend(driver.find_elements_by_xpath(
        '//a[contains(@href,"staff")]'))
    faculty_links.extend(driver.find_elements_by_xpath(
        '//a[contains(@href,"people")]'))

    # gets all links on page
    all_links = driver.find_elements_by_tag_name("a")

    faculty_arr = []
    for link in faculty_links:
        # gets text contained in href
        important_link_text = link.get_attribute('innerHTML').strip()
        arrow_idx = important_link_text.find("<")
        if arrow_idx != -1:
            important_link_text = important_link_text[:arrow_idx]
        if important_link_text is None or important_link_text == "":
            important_link_text = link.text
        # gets the url from the href
        url = link.get_attribute('href')
        if url is not None and important_link_text is not None:
            # add relevant data to Faculty Member struct
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

    num_matches = 0
    final_arr = []
    titles_arr = []

    # seeing if img alts found exist in array faculty member objects
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

    # seeing if img srcs found exist in array faculty member objects
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

    # looking through all links, checks to see if "titles" exist within object being checked
    for link in all_links:
        url = link.get_attribute('href')
        # filtering urls
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

    # removes duplicates and None
    final_arr = list(set(filter(None, final_arr)))
    titles_arr = list(set(filter(None, titles_arr)))

    final_arr.extend(titles_arr)
    # removes duplicates and None
    final_arr = list(set(filter(None, final_arr)))

    # removes urls that are just the given url
    main_url_hashtag = department_url + "#"

    for link in final_arr:
        if main_url_hashtag in link or department_url == link:
            final_arr.remove(link)

    return final_arr

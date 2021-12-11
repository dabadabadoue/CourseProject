from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import combine_automation

import itertools
import threading
import time
import sys

done = False
# here is the animation


def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    # sys.stdout.write('\rDone!     ')


if __name__ == '__main__':
    # create a webdriver object and set options for headless browsing
    options = Options()
    options.headless = True
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome('./chromedriver.exe', options=options)
    department_url = input("Enter Department URL to find Directory Page: ")
    print('Finding Potential Directory Pages...\n')
    driver.get(department_url)

    faculty_links = driver.find_elements_by_xpath(
        '//a[contains(@href,"faculty")]')
    faculty_links.extend(driver.find_elements_by_xpath(
        '//a[contains(@href,"staff")]'))
    faculty_links.extend(driver.find_elements_by_xpath(
        '//a[contains(@href,"people")]'))

    faculty_synonyms = ["faculty", "staff", "people"]

    directory_links = []
    for link in faculty_links:
        important_link_text = link.get_attribute('innerHTML').strip()
        arrow_idx = important_link_text.find("<")
        if arrow_idx != -1:
            important_link_text = important_link_text[:arrow_idx]
        # important_link_text = link.text
        if important_link_text is None or important_link_text == "":
            important_link_text = link.text

        url = link.get_attribute('href')
        if url is not None and important_link_text is not None:
            # cur_url = (''.join(filter(str.isalnum, url))).lower()
            important_link_text = (
                ''.join(filter(str.isalnum, important_link_text))).lower()
            for word in faculty_synonyms:
                if word in important_link_text:
                    directory_links.append(url)

    directory_links = list(set(filter(None, directory_links)))

    i = 1
    all_bios = []
    for link in directory_links:
        print("Potential Directory Page " + str(i) + ": " + link)
        done = False
        t = threading.Thread(target=animate)
        t.daemon = True
        t.start()
        final_arr = combine_automation.is_directory_page(driver, link)
        done = True
        if len(final_arr) > 0:
            sys.stdout.flush()
            # sys.stdout.write("\rPage " + str(i) + " is a Directory Webpage, see page_" +
            #                  str(i) + "_faculty_pages.txt for faculty webpages\n\n")
            sys.stdout.write("\rPage " + str(i) +
                             " is a Directory Webpage\n\n")
            # with open("page_" + str(i) + "_faculty_pages.txt", 'w') as f:
            #     for url in final_arr:
            #         f.write(url)
            #         f.write('\n')
            all_bios.extend(final_arr)
        else:
            sys.stdout.flush()
            sys.stdout.write("\rPage " + str(i) +
                             " is not a Directory Webpage\n\n")
        i += 1
    driver.quit()
    all_bios = list(set(filter(None, all_bios)))

    with open("faculty_pages.txt", 'w') as f:
        for url in all_bios:
            f.write(url)
            f.write('\n')

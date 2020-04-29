from selenium import webdriver
import time
import getpass
import traceback
from tqdm import tqdm

def sleep(seconds):
    for x in tqdm(seconds):
        time.sleep(1)

def tear_down(driver):
    driver.quit()

def get_videos(driver):
    driver.get("https://www.midjobs.com/user/earn/youtube.aspx")
    print('getting links')
    sleep(range(2))
    links = driver.find_elements_by_class_name("YouTubeLink")
    return links

def watch_videos(ytlinks, driver):
    for link in ytlinks:
        print("watching ... " + link)
        driver.get(link)

        sleep(range(10))
        required_frame = driver.find_element_by_xpath('//*[@id="player"]')
        driver.switch_to.frame(required_frame) 

        ytbtn = driver.find_element_by_xpath("//button[@aria-label='Play']")
        ytbtn.click()
        sleep(range(50))
        print("")


def main():
    u = input('username? ')
    p = getpass.getpass(prompt='password? ')
    total_videos = int(input('input # of total videos to watch: '))
    driver = webdriver.Chrome()
    driver.get("https://www.midjobs.com/login.aspx")

    try:
        username_field = driver.find_element_by_xpath('//*[@id="ctl00_MainContentPlaceHolder_ctl00_Username"]')
        password_field = driver.find_element_by_xpath('//*[@id="ctl00_MainContentPlaceHolder_ctl00_Password"]')
        login_btn = driver.find_element_by_xpath('//*[@id="ctl00_MainContentPlaceHolder_ctl00_LoginButton"]')

        username_field.send_keys(u)
        password_field.send_keys(p)
        login_btn.click()

        ytlinks = []
        ctr = 0
        while ctr < total_videos:
            links = get_videos(driver)
            for i in range(len(links)):
                src = links[i].get_attribute("href")
                if src not in ytlinks:
                    ytlinks.append(links[i].get_attribute("href"))
                ctr += 1

        print("")
        print("=========================")
        print("= watching " + str(len(ytlinks)) + " video/s...=")
        print("=========================")
        print("")

        watch_videos(ytlinks,driver)

        print("done. exiting ...")
        sleep(range(2))
        tear_down(driver)
    except Exception:
        traceback.print_exc()
        tear_down(driver)


if __name__ == '__main__':
    main()

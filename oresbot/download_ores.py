import requests
from requests import Request
import time
from time import gmtime, strftime
import json
import os
from os.path import dirname
import sys
if __name__ == '__main__':

    if sys.platform is 'win32' or sys.platform is 'cygwin' or os.name is 'nt':
        # C:\Users\genieelecpsim\Downloads
        default_path = "C:\\Users\\"
        driver_name = "geckodriver.exe"
        default_user_path = default_path + os.environ['USERNAME']
        download_pth = default_user_path + "\\" + "BotDownloads"
        exe_path = dirname(__file__)+"\\"+driver_name
    else:
        default_path = "/"
        driver_name = "geckodriver"
        default_user_path = "/home"
        download_pth = "/home/BotDownloads"
        exe_path = dirname(__file__) + "/" + driver_name

    today = strftime("%d/%m/%Y", gmtime())
    day = int(today.split("/")[0])
    month = int(today.split("/")[1])
    year = int(today.split("/")[2])
    for i in range(2):
        day = int(day) - 1
        month = int(month)
        year = int(year)
        # If the day's bigger than 0, we don't have to change the month
        if day > 0:
            if day >= 10:
                day = str(day)
            else:
                day = "0"+str(day)
            if month >= 10:
                month = str(month)
            else:
                month = "0"+str(month)
        else:
            # If it is lesser or equal than 0, we have to change the entire date.
            # We go back of 1 month first.
            month -= month
            # If it's January, March, May, July, Augustus, October or December, we set day to 31.
            if month in [1, 3, 5, 7, 8, 10, 12]:
                day = 31
            # If it's April, June, September or November, we set day to 30.
            elif month in [4, 6, 9, 11]:
                day = 30
            # If none of the first two conditions are met, it means we are in February. Thus, we have to check if we're
            # on a bissextile year by checking if year % 4 equals to 0. If it is, we set day to 29
            elif year % 4 == 0:
                day = 29
            # If not, we set day to 28.
            else:
                day = 28
            # Finally, we have to refactor the date to get it as a string and in the correct format.
            if day >= 10:
                day = str(day)
            else:
                day = "0"+str(day)
            if month >= 10:
                month = str(month)
            else:
                month = "0"+str(month)
        if i == 0:
            end_day = str(str(year)+"/"+month+"/"+day)
        if i == 1:
            start_day = str(str(year)+"/"+month+"/"+day)

    # Opening file to read credentials from
    with open('credentials.json') as data_file:
        data = json.load(data_file)
    # Retrieving values from the corresponding JSON key
    username = data['id']
    password = data['pw']
    url = data['url']
    urllogin = data['urllogin']

    """
    Just Selenium stuff - not used anymore
    # Creating driver
    driver = webdriver.Firefox(executable_path=exe_path)
    driver.get(url)
    login_box = driver.find_element_by_name('username')
    pw_box = driver.find_element_by_name('password')
    auth_btn = driver.find_element_by_name('submit')

    login_box.send_keys(username)
    pw_box.send_keys(password)
    auth_btn.click()

    # Locating and clicking on the "UMONS" header
    try:
        # This method will make the driver driver wait, for a maximum of 5 seconds, for an element to be located.
        umons_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            'h3#ui-accordion-groupAccordeon-header-1'
                                            '.ui-accordion-header'
                                            '.ui-helper-reset'
                                            '.ui-state-default'
                                            '.ui-accordion-icons'
                                            '.ui-corner-all')))
        umons_menu.click()
    except TimeoutError:
        print("umons_menu not found (timeout)")
        with open("download_ores.log", "wb") as log:
            print(today, ": umons_menu not found (timeout)")
    # The list of all EAN"s
    try:
        EAN_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, "group_12")
            )
        )
        time.sleep(1)
    except TimeoutError:
        print("EAN_select not found (timeout)")
        with open("download_ores.log", "wb") as log:
            print(today, ": EAN_select not found (timeout)")

    EAN_listview = EAN_select.find_element_by_tag_name("div")

    # Gray EAN's
    gray_list = EAN_listview.find_elements_by_class_name("meterlink")
    # Green EAN's
    green_list = EAN_listview.find_elements_by_class_name("meterlinktrue")"""

    filename = ""

    try:
        # Everything has to be in the same browser session, so we start a new one by using the "with" keyword, to make
        # sure it will be automatically closed when we'll exit the "with" block.
        with requests.Session() as s:
            # Request to log in. It's a POST request using basic authentification.
            login_req = s.post(urllogin, data={'username': username, 'password': password}, stream=True)
            # The link to the array of EAN and their values.
            page_with_list = s.get("https://www.ores-smartmetering.be/smores/resources/meter/group/12?_=1493990362446")
            # Once we've retrieved the list, we have to convert it into proper JSON.
            html_to_parse = page_with_list.json()
            gray_list = []
            green_list = []
            for element in html_to_parse:
                # If their "eco" key corresponds to a "True" value, we will put them into the "green_list"
                if element['eco']:
                    green_list.append(element)
                # If not, we will put them into the gray-list.
                else:
                    gray_list.append(element)


            # Treatments are the same for both lists:
            for ean in gray_list:
                # First we retrieve the (html)ID of the current EAN.
                ean_id = ean['id']
                # Then we pass it to the direct download link
                dl_url = "https://ores-smartmetering.be/smores/resources/meterdata/csv/meter/" \
                      "%s?startDate=%sT22:00:00"\
                      "Z&endDate=%sT22:00:00Z&period=MINUTES_15" \
                         % (ean_id, start_day.replace("/", "-"), end_day.replace("/", "-"))
                # Once the link is created, we prepare a GET request from it.
                download_req = Request('GET', dl_url)
                # Of course, we want to keep the authentication alive, so we will have to create some cookies, so the
                # connection will be able to consume them.
                cook = {}
                for (key, val) in s.cookies.items():
                    cook[key] = val
                # Executing the GET request
                r = s.get(dl_url, cookies=cook)
                # Formatting the file name.
                day_for_file = start_day.replace("/", "-")
                filename = ean['ean'] + "_gris_" + day_for_file + ".csv"
                # If we are authenticated, we open a new file with the download_path + the filename, and write the bytes
                # we retrieved from the GET request.
                if r.status_code == 200:
                    with open(os.path.join(download_pth, filename), "wb") as file:
                        for bits in r.iter_content():
                            file.write(bits)
                # We then sleep a bit so the server won't be overloaded.
                time.sleep(0.5)

            for ean in green_list:
                ean_id = ean['id']
                dl_url = "https://ores-smartmetering.be/smores/resources/meterdata/csv/meter/" \
                         "%s?startDate=%sT22:00:00" \
                         "Z&endDate=%sT22:00:00Z&period=MINUTES_15" \
                         % (ean_id, start_day.replace("/", "-"), end_day.replace("/", "-"))
                download_req = Request('GET', dl_url)
                cook = {}
                for (key, val) in s.cookies.items():
                    cook[key] = val
                r = s.get(dl_url, cookies=cook)
                day_for_file = start_day.replace("/", "-")
                filename = ean['ean'] + "_vert_" + day_for_file + ".csv"
                if r.status_code == 200:
                    with open(os.path.join(download_pth, filename), "wb") as file:
                        for bits in r.iter_content():
                            file.write(bits)
                time.sleep(0.5)

    finally:
        # If we have an error, do nothing.
        pass

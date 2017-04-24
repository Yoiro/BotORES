from selenium import webdriver
import shutil
import time
from time import gmtime, strftime
import json
import os
from os.path import dirname
import sys

if __name__ == '__main__':

    default_path = ""
    if sys.platform is 'win32' or sys.platform is 'cygwin' or os.name is 'nt':
        default_path = "C:\\Users\\"
        driver_name = "geckodriver.exe"
    else:
        driver_name = "geckodriver"
        if sys.platform is 'darwin':
            default_path = ""
        if sys.platform is 'linux':
            default_path = "home\\"


    default_user_path = default_path + os.environ['USERNAME']
    download_pth = default_user_path + "\\" + "BotDownloads"

    with open('credentials.json') as data_file:
        data = json.load(data_file)

    username = data['id']
    password = data['pw']
    url = data['url']

    # Creating Firefox Profile
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", download_pth)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                           ("text/csv,"
                            "application/x-msexcel,"
                            "application/excel,"
                            "application/x-excel,"
                            "application/vnd.ms-excel,"
                            "image/png,"
                            "image/jpeg,"
                            "text/html,"
                            "text/plain,"
                            "application/msword,"
                            "application/xml"))

    # Creating driver
    driver = webdriver.Firefox(executable_path=dirname(__file__)+"\\"+driver_name, firefox_profile=profile)

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
            end_day = str(day+"/"+month+"/"+str(year))
        if i == 1:
            start_day = str(day+"/"+month+"/"+str(year))

    # Connecting to Ores' website
    driver.get(url)
    login_box = driver.find_element_by_name('username')
    pw_box = driver.find_element_by_name('password')
    auth_btn = driver.find_element_by_name('submit')

    login_box.send_keys(username)
    pw_box.send_keys(password)
    auth_btn.click()

    # Waiting for the new page to load
    time.sleep(4)

    # Locating and clicking on the "UMONS" header
    umons_menu = driver.find_element_by_css_selector(
        "h3#ui-accordion-groupAccordeon-header-1"
        ".ui-accordion-header"
        ".ui-helper-reset"
        ".ui-state-default"
        ".ui-accordion-icons"
        ".ui-corner-all")
    umons_menu.click()
    # Waiting for browser's response
    time.sleep(3)
    # The list of all EAN"s
    EAN_listview = driver.find_element_by_id("group_12").find_element_by_tag_name("div")
    # Gray EAN's
    gray_list = EAN_listview.find_elements_by_class_name("meterlink")
    # Green EAN's
    green_list = EAN_listview.find_elements_by_class_name("meterlinktrue")

    filename = ""

    i = 0
    for ean in gray_list:
        # Click on the right EAN to get its information.
        gray_list[i].click()
        time.sleep(4)
        # Locating the part of the page where we'll be able to click to download file
        main_div = driver.find_element_by_id("content")
        tabs_div = main_div.find_element_by_id("tabs")
        # Div where the relevant UI's lying
        ui_div = tabs_div.find_element_by_id("tabs-1")
        # Getting to the tab (date's user input)
        row_input = ui_div.find_element_by_tag_name("table") \
            .find_element_by_tag_name("tbody") \
            .find_element_by_tag_name("tr")
        # Getting all the columns
        table_cols = row_input.find_elements_by_tag_name("td")
        switch = table_cols[0]
        datepicker = table_cols[1]
        timestamp = table_cols[2]
        download_btn = table_cols[3]
        # Loading the wanted date
        start_picker = datepicker.find_element_by_id("chartStartDatePicker")
        end_picker = datepicker.find_element_by_id("chartEndDatePicker")
        start_picker.clear()
        start_picker.send_keys(start_day)
        end_picker.clear()
        end_picker.send_keys(end_day)
        datepicker.find_element_by_name("refresh").click()
        time.sleep(4)
        # Getting the right timestamp
        timestamp.find_element_by_id("min15").click()
        time.sleep(2)
        # Downloading file
        download_btn.find_element_by_name("export").click()
        time.sleep(4)
        day_for_file = start_day.replace("/", "-")
        filename = ean.text.split("-")[0]+"_gris_"+day_for_file+".csv"
        for file in os.listdir(download_pth):
            if file.startswith("export") and file.endswith(".csv"):
                newfile = os.path.join(download_pth, filename)
                shutil.move(os.path.join(download_pth, file), newfile)
                print(os.listdir(download_pth))
        i += 1

    i = 0
    for ean in green_list:
        # Click on the right EAN to get its information.
        green_list[i].click()
        time.sleep(4)

        # Locating the part of the page where we'll be able to click to download file
        main_div = driver.find_element_by_id("content")
        tabs_div = main_div.find_element_by_id("tabs")
        # Div where the relevant UI's lying
        ui_div = tabs_div.find_element_by_id("tabs-1")
        # Getting to the tab (date's user input)
        row_input = ui_div.find_element_by_tag_name("table") \
            .find_element_by_tag_name("tbody") \
            .find_element_by_tag_name("tr")
        # Getting all the columns
        table_cols = row_input.find_elements_by_tag_name("td")
        switch = table_cols[0]
        datepicker = table_cols[1]
        timestamp = table_cols[2]
        download_btn = table_cols[3]
        # Loading the wanted date
        start_picker = datepicker.find_element_by_id("chartStartDatePicker")
        end_picker = datepicker.find_element_by_id("chartEndDatePicker")
        start_picker.clear()
        start_picker.send_keys(start_day)
        end_picker.clear()
        end_picker.send_keys(end_day)
        datepicker.find_element_by_name("refresh").click()
        time.sleep(4)
        # Getting the right timestamp
        timestamp.find_element_by_id("min15").click()
        time.sleep(2)
        # Downloading file
        download_btn.find_element_by_name("export").click()
        time.sleep(4)
        day_for_file = start_day.replace("/", "-")
        filename = ean.text.split("-")[0] + "_vert_" + day_for_file + ".csv"
        for file in os.listdir(download_pth):
            if file.startswith("export") and file.endswith(".csv"):
                newfile = os.path.join(download_pth, filename)
                shutil.move(os.path.join(download_pth, file), newfile)
                print(os.listdir(download_pth))
        i += 1


    driver.close()

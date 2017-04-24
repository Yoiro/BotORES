if __name__ == '__main__':
    from selenium import webdriver
    import time
    from time import gmtime, strftime
    import json
    import sys
    import os
    from os.path import dirname
    import re

    with open('credentials.json') as data_file:
        data = json.load(data_file)

    username = data['id']
    password = data['pw']
    url = data['url']

    print(sys.platform)

    driver_name = "geckodriver.exe" if sys.platform is "win32" else "geckodriver-v0.15.0-linux64.tar.gz"
    # os.path.join(dirname(__file__), driver_name)

    driver = webdriver.Firefox()
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
    end_day = strftime("%d/%m/%Y", gmtime())
    day = int(end_day.split("/")[0])
    month = int(end_day.split("/")[1])
    year = int(end_day.split("/")[2])
    day -= 1
    if day >= 10:
        day = str(day)
    else:
        day = "0"+str(day)
    if month >=10:
        month = str(month)
    else:
        month = "0"+str(month)
    start_day = str(day+"/"+month+"/"+str(year))

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
    i = 0
    # Locating the part of the page where we'll be able to click to download file
    main_div = driver.find_element_by_id("content")
    tabs_div = main_div.find_element_by_id("tabs")
    # Div where the relevant UI's lying
    ui_div = tabs_div.find_element_by_id("tabs-1")
    # Getting to the tab (date's user input)
    row_input = ui_div.find_element_by_tag_name("table")\
        .find_element_by_tag_name("tbody")\
        .find_element_by_tag_name("tr")
    # Getting all the columns
    table_cols = row_input.get_elements_by_tag_name("td")
    switch = table_cols[0]
    datepicker = table_cols[1]
    timestamp = table_cols[2]
    download_btn = table_cols[3]
    # Loading the wanted date
    datepicker.find_element_by_id("chartStartDatePicker").send_keys(start_day)
    datepicker.find_element_by_id("chartEndDatePicker").send_keys(end_day)
    datepicker.find_element_by_name("refresh").click()
    time.sleep(4)
    # Getting the right timestamp
    # Downloading file

    for ean in gray_list:
        gray_list[i].click()
        time.sleep(4)
        driver.find_element_by_css_selector("input#chartStartDatePicker.hasDatePicker").send_keys(start_day)
        driver.find_element_by_css_selector("input#chartEndDatePicker.hasDatePicker").send_keys(end_day)
        i += 1

    """
    i = 0
    for ean in green_list:
        green_list[i].click()
        time.sleep(4)
        driver.find_element_by_css_selector("input#chartStartDatePicker.hasDatePicker").send_keys(start_day)
        driver.find_element_by_css_selector("input#chartEndDatePicker.hasDatePicker").send_keys(end_day)
        i += 1"""

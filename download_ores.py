if __name__ == '__main__':
    from selenium import webdriver
    import time
    from time import gmtime, strftime
    import json
    import re

    with open('credentials.json') as data_file:
        data = json.load(data_file)

    username = data['id']
    password = data['pw']
    url = data['url']

    driver = webdriver.Firefox()
    driver.get(url)
    login_box = driver.find_element_by_name('username')
    pw_box = driver.find_element_by_name('password')
    auth_btn = driver.find_element_by_name('submit')

    login_box.send_keys(username)
    pw_box.send_keys(password)
    auth_btn.click()

    # Waiting for the new page to load
    time.sleep(3)
    end_day = strftime("%d/%m/%Y", gmtime())
    print(end_day)
    day = int(end_day.split("/")[0])
    month = int(end_day.split("/")[1])
    year = int(end_day.split("/")[2])
    day = day-1
    if day >= 10:
        day = str(day)
    else:
        day = "0"+str(day)
    if month >=10:
        month = str(month)
    else:
        month = "0"+str(month)
    start_day = str(day+"/"+month+"/"+str(year))
    print(start_day, end_day)

    # Locating the "UMONS" header
    umons_menu = driver.find_element_by_css_selector(
        "h3#ui-accordion-groupAccordeon-header-1"
        ".ui-accordion-header"
        ".ui-helper-reset"
        ".ui-state-default"
        ".ui-accordion-icons"
        ".ui-corner-all")
    umons_menu.click()
    EAN_listview = driver.find_element_by_id("group_12")
    time.sleep(3)
    gray_list = driver.find_elements_by_class_name("meterlink")
    green_list = driver.find_elements_by_class_name("meterlinktrue")
    for ean in gray_list:
        driver.find_element_by_link_text(ean.text).click()
        time.sleep(2)
        driver.find_element_by_css_selector("input#chartStartDatePicker.hasDatePicker").send_keys(start_day)
        driver.find_element_by_css_selector("input#chartEndDatePicker.hasDatePicker").send_keys(end_day)

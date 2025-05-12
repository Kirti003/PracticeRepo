from selenium import webdriver
from selenium.webdriver.common.by import By

def test_sort(browserInstance):
    driver = browserInstance
    browserSortedList = []

    driver.get("https://rahulshettyacademy.com/seleniumPractise/#/offers")
    driver.maximize_window()

    # click on column header  - to sort the list which may or may not be available in app

    driver.find_element(By.XPATH, "//span[text()='Veg/fruit name']").click()

    veggieWebElement = driver.find_elements(By.XPATH, "//tr/td[1]")

    for veg in veggieWebElement:
        browserSortedList.append(veg.text)

    originalBrowserSortedList = browserSortedList.copy()
    # Sort this list
    browserSortedList.sort()

    assert originalBrowserSortedList == browserSortedList

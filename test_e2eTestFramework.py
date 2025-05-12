import json
import pytest

from pageObjects import login
from pageObjects.login import LoginPage

test_data_path = '../Data/test_e2eTestFramework.json'
with open(test_data_path) as f:
    test_data = json.load(f)
    test_list = test_data["data"]

@pytest.mark.smoke
# warning appear on execution to register the scope of custom tag smoke and 'Default fixture loop scope unset'
# create pytest.ini file at project level
@pytest.mark.parametrize("test_list_item",test_list)
def test_e2e(browserInstance,test_list_item):
    # Only fixtures are allowed in pytest function arguments
    driver = browserInstance


    driver.get("https://rahulshettyacademy.com/loginpagePractise/")
    loginPage = LoginPage(driver)   # Create class obj, constructor argument has to sent through with object
 #   loginPage.login()           # Call the method
    # After login we are sure that we are going to shop page so we create object for shop page here and return it
    # It will eliminate 1 step in main method  loginPage.login()
    print(loginPage.getTitle())

# After login user will navigate to shop page. Rather then creating object here. Create object in login n return
#shopPage = ShopPage(driver) no need create object using login class n call shop class obj
    shop_page = loginPage.login(test_list_item["userEmail"],test_list_item["userPassword"])
    shop_page.add_product_to_cart(test_list_item["productName"])
    #shop_page.goToCart()
    checkout_confirmation = shop_page.goToCart()
    checkout_confirmation.checkout()
    checkout_confirmation.enter_delivery_address("ind")
    checkout_confirmation.validate_order()
# to create json at current folder level and ini at project level right click. Enter file name with.json and .ini at the end
# conftest is pythonfile only
# utils file -> right click -> directory at project level. With in that right click new python file 'browserutils'
# pytest -n 10 //pytest-xdist plugin you need to run in parallel
# pytest --html reports/report.html  // To generate reports
# create folder for the folder where you are running ur scripts by right click -> directory
# python -m pytest -n 2 --html reports/report.html (copy path by right ckick) paste in browser
# python -m pytest -n 2 -m smoke --browser_name edge --html reports/report.html
# To run tc in parallel with tag using browser and generating reports
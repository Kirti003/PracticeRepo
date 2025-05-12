import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
driver = None
# To register the options url: https://doc.pytest.org/en/stable/example/simple.html
def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome", help="browser selection")

@pytest.fixture(scope="function")
def browserInstance(request):
    global driver
    browser_name = request.config.getoption("--browser_name")
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        chrome_prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False
        }
        options.add_experimental_option('prefs', chrome_prefs)
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
    elif browser_name == "edge":
        driver = webdriver.Edge()
        driver.maximize_window()

    driver.implicitly_wait(5)
    driver.get("https://rahulshettyacademy.com/loginpagePractise/")
    yield driver #Before test function execution
    driver.close()  #post your test function execution

@pytest.hookimpl( hookwrapper=True )
def pytest_runtest_makereport(item):

    pytest_html = item.config.pluginmanager.getplugin( 'html' )
    outcome = yield
    report = outcome.get_result()
    extra = getattr( report, 'extra', [] )

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr( report, 'wasxfail' )
        if (report.skipped and xfail) or (report.failed and not xfail):
            reports_dir = os.path.join( os.path.dirname( __file__ ), 'reports' )
            file_name = os.path.join( reports_dir, report.nodeid.replace( "::", "_" ).replace("/","_") + ".png" )
            print( "file name is " + file_name )
            _capture_screenshot( file_name )
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append( pytest_html.extras.html( html ) )
        report.extras = extra

def _capture_screenshot(file_name):
    driver.get_screenshot_as_file(file_name)


# To remove error or to activate driver in above function. Declare one driver n top initially it is none
# inside fixture declare driver as global and once it is active. it's value is reusable in other methods as well


# using command on command line user can provide browser name
# python -m pytest test_e2e_TestFramework.py --browser_name chrome is a part of request.
# request is a default parameter globally available for every fixure
# First register the options before we give options on terminal
   # service_obj = Service()
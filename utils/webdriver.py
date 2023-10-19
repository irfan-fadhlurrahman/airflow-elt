import os
import uuid

from typing import Protocol
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# For setting options arguments in the webdriver
class OptionsArgs(Protocol):
    def set_options(self):
        pass

class NonHeadlessOptionsArgs:
    def set_options(self, options: Options) -> Options:
        options.add_argument("--start-maximized")
        return options

class HeadlessOptionsArgs:
    def set_options(self, options: Options) -> Options:
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-notifications')
        options.add_argument("--start-maximized")
        return options


# For setting desired capabilities of the webdriver
class Capabilities(Protocol):
    def set_capabilities(self):
        pass

@dataclass
class SimpleCapabilities:
    browser_name: str
    browser_version: str
    platform_name: str
    
    def set_capabilities(self, options: Options) -> Options:
        if self.browser_name:
            options.set_capability('browserName', self.browser_name)
        if self.browser_version:
            options.set_capability('browserVersion', self.browser_version)
        if self.platform_name:
            options.set_capability('platformName', self.platform_name)

        return options


# To create webdriver with options and desired capabilities
class WebDriver(Protocol):
    def init_driver(self):
        pass

@dataclass
class RemoteWebDriver:
    host_url: str
    options: Options
    options_args: OptionsArgs
    capabilities: Capabilities
      
    def get_options(self) -> Options:
        options = self.options_args.set_options(self.options)
        if self.capabilities is not None:
            options = self.capabilities.set_capabilities(options)
            
        return options
    
    def init_driver(self) -> webdriver.remote.webdriver.WebDriver:
        return webdriver.Remote(
            command_executor=self.host_url, 
            options=self.get_options()
        )

@dataclass
class LocalChromeWebDriver:
    """
    * Before using this class for the first time, 
    please execute containers/apscheduler/init_chromedriver.sh 
    to get chromedriver that has same version as chrome browser.
    * Only support headless mode.
    """
    executable_path: str
    options_args: OptionsArgs
    
    def init_driver(self) -> webdriver.remote.webdriver.WebDriver:
        return webdriver.Chrome(
            service=Service(self.executable_path), 
            options=self.options_args.set_options(
                webdriver.ChromeOptions()
            )
        )


# Shortcut
WEBDRIVER_OPTIONS_DICT = {
    "firefox": webdriver.FirefoxOptions(),
    "chrome": webdriver.ChromeOptions()
}
OPTIONS_ARGS_DICT = {
    "non_headless": NonHeadlessOptionsArgs(),
    "headless": HeadlessOptionsArgs()
}

def remote_driver(browser: str, options: str, version: str = None) -> webdriver.remote.webdriver.WebDriver:
    driver = RemoteWebDriver(
        host_url='http://selenium-hub:4444',
        options=WEBDRIVER_OPTIONS_DICT[browser],
        options_args=OPTIONS_ARGS_DICT[options],
        capabilities=SimpleCapabilities(
            browser_name=browser,
            browser_version=version,
            platform_name='linux'
        )
    ).init_driver()
    driver.set_window_size(1366, 768)
    
    return driver

def _get_chromedriver(folder_path: str):
    os.system(f"""
        mkdir -p {folder_path}
        
        CHROME_VERSION=$(google-chrome-stable --product-version)
        CHROMEDRIVER_DOWNLOAD_LINK="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION/linux64/chromedriver-linux64.zip"

        wget -qnv $CHROMEDRIVER_DOWNLOAD_LINK -O {folder_path}/chromedriver-linux64.zip
        unzip -qq -d {folder_path}/ {folder_path}/chromedriver-linux64.zip    
    """)

def local_chrome_driver() -> webdriver.chrome.webdriver.WebDriver:
    folder_path = f".wdm/{str(uuid.uuid4())}"
    _get_chromedriver(folder_path)
    driver = LocalChromeWebDriver(
        executable_path=f"{folder_path}/chromedriver-linux64/chromedriver",
        options_args=OPTIONS_ARGS_DICT["headless"],
    ).init_driver()
    driver.set_window_size(1366, 768)
    
    return driver
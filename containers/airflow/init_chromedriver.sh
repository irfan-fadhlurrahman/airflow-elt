#!/bin/bash

CHROME_VERSION=$(google-chrome-stable --product-version)
CHROMEDRIVER_DOWNLOAD_LINK="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chromedriver-linux64.zip"

# Download
wget ${CHROMEDRIVER_DOWNLOAD_LINK} -O containers/apscheduler/chromedriver-linux64.zip

# Unzip
unzip -d containers/apscheduler/ containers/apscheduler/chromedriver-linux64.zip
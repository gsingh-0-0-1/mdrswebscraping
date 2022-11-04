import numpy as np
from bs4 import BeautifulSoup
import requests
import html2text
from termcolor import colored

import utils
from recursive_scrape import webItem

TOP_URL = "http://mdrs.marssociety.org/previous-field-seasons/"

DATABASE = webItem(TOP_URL, None)
DATABASE.fetchSelfData()
DATABASE.getChildren(filterfunc = utils.defaultWordFilter)
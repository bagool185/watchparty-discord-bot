""" Suppress annoying 'Unverified HTTPS request' warnings when using localhost """
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
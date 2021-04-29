import requests
import urllib3
import getpass
import json
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ip_add = "<your-ip-here>"
params= {"username": "joe", "password": getpass.getpass()}
now = datetime.now()
dt_string = now.strftime("%d%m%Y_%H:%M:%S")

session = requests.Session()
try:
    login = session.post(f"https://{ip_add}/rest/v10.04/login", params=params, verify=False)
    print(f"This is the login code: {login.status_code}")
    hostname_request = session.get(f"https://{ip_add}/rest/v10.04/system", verify=False)
    hostname = hostname_request.json()["hostname"]
    response = session.get(f"https://{ip_add}/rest/v10.04/fullconfigs/running-config", verify=False)
    config = response.json()
    with open(f'{hostname}_{dt_string}config.json', 'w') as outputfile:
        json.dump(config, outputfile, indent=4)
finally:
    logout = session.post(f"https://{ip_add}/rest/v10.04/logout")
    print(f"This is the logout code: {logout.status_code}")
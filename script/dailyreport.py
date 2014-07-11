
import requests

p = {'sendemail': 1}

requests.get("http://127.0.0.1/admin/stat/", params=p)


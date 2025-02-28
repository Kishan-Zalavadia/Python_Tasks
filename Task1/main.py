import requests
import os

version  = requests.__version__
user_request = input("write your request version: ")
if(version == user_request or user_request == ""):
    print("your requirement is satisfied")
else:
    os.system(f"pip install requests=={user_request}")   
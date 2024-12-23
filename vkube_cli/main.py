import os
# sys.path.append(os.getcwd())
import subprocess
import json
from config.credentials import get_logined_username_in_mac
# from config.credentials import check_auth_field

def main():

    username = get_logined_username_in_mac("https://index.docker.io/v1/")
    print(username)

if __name__ == "__main__":
    main()

    

    
    
import os
# sys.path.append(os.getcwd())
import subprocess
import json
from config.credentials import check_and_login
# from config.credentials import check_auth_field

def main():

    check_and_login()

if __name__ == "__main__":
    main()

    

    
    
import click
import os
import json
import subprocess
from subprocess import CalledProcessError

def check_auth_field():
    
    # 将 JSON 字符串解析为 Python 字典
    credentials_file = os.path.expanduser("~/.docker/config.json")
    if os.path.exists(credentials_file):
        with open(credentials_file, 'r') as f:
            data = json.load(f)

    # 检查 "auths" 字段是否存在
    if "auths" not in data:
        print("The 'auths' field does not exist.")
        return False
    if 'https://index.docker.io/v1/' not in data["auths"]:
        print("The 'https://index.docker.io/v1/' field does not exist.")
        return False
    return True

        

def save_credentials(registry, username, password):
    """Save the credentials to a local file (simulate Docker login)."""
    credentials_file = os.path.expanduser("~/.docker/config.json")

    if os.path.exists(credentials_file):
        with open(credentials_file, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    

    # with open("config.json", 'w') as f:
    with open(credentials_file, 'w') as f:
        json.dump(data, f, indent=4)
    click.echo(f"Credentials saved for registry: {registry}")

def authenticate(registry, username, password):
    """Simulate authentication with the registry."""
    # In a real implementation, this would send a request to the registry
    if username and password:
        click.echo(f"Successfully authenticated with {registry} as {username}")
        return True
    else:
        click.echo("Authentication failed")
        return False
def docker_login():
    if check_auth_field():
        result = subprocess.run(['docker','login'])
        if result.returncode == 0:
            click.echo('Login successful!')
            return True
    username = click.prompt("Enter your Dockerhub username")
    password = click.prompt("Enter your Dockerhub password")
    result = subprocess.run(['docker', 'login', '-u', username,"--password-stdin"], input=f'{password}\n'.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        click.echo('Login successful!')
        try:
            # Try a simple docker command to check login status
            output = subprocess.check_output(['docker', 'info'], text=True)
            if "Username" in output:
                print("User is already logged in.")
                return True
        except subprocess.CalledProcessError as e:
            print("Not logged in or credentials are invalid.")
            return False
        return True
    else:
        click.echo("Login failed")
        return False
    
def is_docker_installed():
    try:
        # 尝试执行 `docker --version` 命令
        result = subprocess.run(['docker', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            return True
        else:
            return False
    except (FileNotFoundError,CalledProcessError):
        # 如果系统找不到 docker 命令，则 Docker 未安装
        return False
@click.command()
def check_and_login():
    """Simulate Docker login."""
    if not is_docker_installed():
        print('Docker does not seem to be installed. Please install and start docker first.')
        return

    docker_login()


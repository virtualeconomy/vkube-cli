import click
import subprocess
import sys
import platform
from subprocess import CalledProcessError
from config.credentials import 
def is_docker_installed():
    try:
        # 尝试执行 `docker --version` 命令
        result = subprocess.run(['docker', 'info'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            return True
        else:
            return False
    except (FileNotFoundError,CalledProcessError):
        # 如果系统找不到 docker 命令，则 Docker 未安装
        return False

#docker是否已经在后台启动
def start_docker():
    if platform.system() == "Linux":
        # 对于 Linux 使用 systemctl 启动 Docker
        subprocess.run(['sudo', 'systemctl', 'start', 'docker'])
    elif platform.system() == "Darwin":  # Darwin 是 macOS 的系统名称
        # 对于 macOS 使用 open 命令启动 Docker Desktop
        result = subprocess.run(['open', '-a', 'Docker'])
        if result.returncode == 0:
            print("Docker Desktop have started.")
            return True
        else:
            return False
        
    else:
        print("This script only supports macOS and Linux.")
        sys.exit(1)
def docker_ran():
    try:
        result = subprocess.run(['docker', 'info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return True
        else:
            return False
    except (FileNotFoundError,CalledProcessError):
        # 如果系统找不到 docker 命令，则 Docker 未安装
        return False
def docker_login(username,password):
    try:
        result = subprocess.run(['docker', 'login', '-u', username], input=f'{password}\n'.encode(), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returecode == 0:
            click.echo('Login successful!')
            return True
        else:
            click.echo("Login failed")
            return False
    except CalledProcessError as e:
        click.echo('Login failed:', err=True)
        click.echo(e.stderr.decode(), err=True)
        return False

def save_credentials(registry, username, password):
    """Save the credentials to a local file (simulate Docker login)."""
    credentials_file = os.path.expanduser("~/.docker/config.json")

    if os.path.exists(credentials_file):
        with open(credentials_file, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    data[registry] = {"username": username, "password": password}

    with open(credentials_file, 'w') as f:
        json.dump(data, f, indent=4)

    click.echo(f"Credentials saved for registry: {registry}")
def check_login(registry,username,password):
    # username = click.prompt('Input Your Docker Hub Username')
    # password = click.prompt('Input Your Docker Hub Password', hide_input=True)
    if not is_docker_installed():
        print('Docker does not seem to be installed. Please install it first.')
        return
    docker_login(username,password)
        

    

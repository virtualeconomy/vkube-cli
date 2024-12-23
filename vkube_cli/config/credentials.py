import click
import os
import base64
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
        return False
    return True
#Linux
def get_logined_username_in_linux(registry,config_path):
    config_path = os.path.expanduser(config_path)
    
    try:
        # 加载配置文件
        with open(config_path, 'r') as file:
            config = json.load(file)
        
        # 获取 auths 字段
        auths = config.get("auths", {})
        credentials = {}
        
        for registry, data in auths.items():
            auth_base64 = data.get("auth")
            if auth_base64:
                # Base64 解码
                decoded = base64.b64decode(auth_base64).decode('utf-8')
                username, password = decoded.split(":", 1)
                credentials[registry] = {"username": username, "password": password}
        
        return credentials
    
    except FileNotFoundError:
        print(f"Error: Docker config file not found at {config_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {config_path}")
    except Exception as e:
        print(f"Unexpected error: {e}")


#MacOS
def get_logined_username_in_mac(registry):
    try:
        result = subprocess.run(['docker-credential-osxkeychain','list'],capture_output= True,check=True,text=True)
        output = result.stdout[1:-2]
        if len(output) <= 0 :
            return ""
        s = output.replace('"', '')

        # 以逗号分隔字符串
        key_value_pairs = s.split(',')

        # 创建空字典
        result_dict = {}

        # 处理每个键值对
        for pair in key_value_pairs:
            # 找到最后一个分号的位置
            last_colon_index = pair.rfind(':')
            
            if last_colon_index != -1:
                # 切割成键和值并去除空格
                key = pair[:last_colon_index].strip()
                value = pair[last_colon_index + 1:].strip()
                
                # 将键值对添加到字典中
                result_dict[key] = value
        return result_dict[registry]

    except subprocess.CalledProcessError as e:
        print(f"Error running the command:{e}")


def docker_login():
    if check_auth_field():
        result = subprocess.run(['docker','login'])
        if result.returncode == 0:
            click.echo('Login without info successful!')
            return True
        else:
            click.echo("other problem")
            return False
    username = click.prompt("Enter your Dockerhub username")
    password = click.prompt("Enter your Dockerhub password",hide_input=True)
    result = subprocess.run(['docker', 'login', '-u', username,"--password-stdin"], input=f'{password}\n'.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        click.echo('Login successful!')
        return True
    else:
        click.echo("Login failed")
        return False
    
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
@click.command()
def check_and_login():
    """Simulate Docker login."""
    if not is_docker_installed():
        print('Docker is not open. Please install and start docker first.')
        return

    docker_login()


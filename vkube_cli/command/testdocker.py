import docker
client = docker.from_env()
print(client.containers.run('alpine',command='echo hello world'))
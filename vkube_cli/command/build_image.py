import docker
import os

def build_docker_image(dockerfile_path, image_name, tag="latest"):
    # 初始化 Docker 客户端
    client = docker.from_env()

    # 验证 Dockerfile 是否存在
    if not os.path.exists(os.path.join(dockerfile_path, "Dockerfile")):
        raise FileNotFoundError("Dockerfile 不存在，请检查路径！")

    # 构建镜像
    print(f"开始构建镜像：{image_name}:{tag}")
    try:
        image, logs = client.images.build(
            path=dockerfile_path,
            tag=f"{image_name}:{tag}",
            rm=True  # 构建完成后删除中间容器
        )
        for log in logs:
            if 'stream' in log:
                print(log['stream'].strip())
        print(f"镜像构建成功：{image_name}:{tag}")
    except docker.errors.BuildError as e:
        print("构建镜像时发生错误：", e)
    except docker.errors.APIError as e:
        print("Docker API 错误：", e)

# 示例：使用当前目录的 Dockerfile 构建镜像
    
import docker



def run_redis_docker_container():
    client = docker.from_env()
    client.containers.run("redis/redis-stack", detach=True)
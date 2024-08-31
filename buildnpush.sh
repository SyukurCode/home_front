docker rmi syukurdocker/home_front:latest
docker buildx build --platform linux/amd64,linux/arm64 --push -t syukurdocker/home_front:latest .

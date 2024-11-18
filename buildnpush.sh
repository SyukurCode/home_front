docker rmi syukurdocker/home_front:latest
BUILDER=$(docker buildx create --use)
docker buildx build --platform=linux/arm64 --push -t syukurdocker/home_front:latest .
docker buildx rm $BUILDER

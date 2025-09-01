docker build -t abio-stress-twas .
docker login
docker tag abio-stress-twas:latest skgadi/abio-stress-twas:latest
docker push skgadi/abio-stress-twas:latest
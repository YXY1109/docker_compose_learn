# 构建镜像

## 制作镜像

```
#切换目录
cd /root/code/docker_compose_learn/build_image_3

#构建镜像
docker build -t paddle_ocr_ppv3:v1.0 .
docker build -t paddle_ocr_ppv3:v1.0 -f Dockerfile_p .

docker rm paddle_ocr_ppv3:v1.0

#运行镜像
docker run -p 5000:5000 paddle_ocr_ppv3:v1.0
docker run --name paddle_ocr_ppv3 -p 5000:5000 -v /root/code/models:/root/.paddlex -v /root/code/output:/app/output paddle_ocr_ppv3:v1.0

#访问
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/docs
```

## mac镜像

```angular2html
docker build -t paddle_ocr_ppv3:v1.0 -f Dockerfile_slim .
docker run --name paddle_ocr_ppv3 -p 5500:5000 -v /Users/cj/Downloads/temp_ocr/models:/root/.paddlex -v /Users/cj/Downloads/temp_ocr/output:/app/output paddle_ocr_ppv3:v1.0

docker rm paddle_ocr_ppv3
```
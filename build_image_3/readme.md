# 构建镜像

## 制作镜像

```
#切换目录
cd /root/code/docker_compose_learn/build_image_3

#构建镜像
docker build -t paddle_ocr_ppv3:v1.0 .
docker build -t paddle_ocr_ppv3:v1.1 -f Dockerfile_p .

#访问
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/docs
```
# yolo_fast_api
将yolo快速部署为一个服务
# 使用方法
## 构建环境
```docker build -t fastapi-yolo:v0.1 .```
## 开启服务
8200为映射到宿主机的端口
``` docker run -p 8200:8000 -d fastapi-yolo:v0.1 ```


## 测试
```
curl -X POST -F "file=@12.jpg" http://服务器地址:8200/file/

curl -X POST -H "Content-Type: application/json" -d '{"url": "图片地址"}' http://服务器地址:8200/detect/
```

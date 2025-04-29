# yolo_fast_api
将yolo快速部署为一个服务
# 使用方法
## 构建环境
```docker build -t fastapi-yolo:v0.1 .```
## 开启服务
8200为映射到宿主机的端口
``` docker run -p 8200:8000 -d fastapi-yolo:v0.1 ```

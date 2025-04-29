from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import JSONResponse
from ultralytics import YOLO
from typing import List, Dict, Any, Optional
import cv2
import numpy as np
import base64
import requests
from pydantic import BaseModel
import uvicorn
app = FastAPI()

model = YOLO("best.pt")

class ImageData(BaseModel):
    image_url: Optional[str] = None
    image_base64: Optional[str] = None

@app.post("/file/")
async def detect_objects(
    file: UploadFile = File(None),
    image_data: ImageData = Body(None),
):
    try:
        img = None
        
        # 1. 如果上传的是文件（传统方式）
        if file:
            image_data = await file.read()
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # 2. 如果提供的是 Base64 图片
        elif image_data and image_data.image_base64:
            img_bytes = base64.b64decode(image_data.image_base64)
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # 3. 如果提供的是远程 URL
        elif image_data and image_data.image_url:
            response = requests.get(image_data.image_url)
            img_bytes = response.content
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        else:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "No image provided"}
            )
        
        # 进行 YOLO 检测
        results = model.predict(img)
        
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                detections.append({
                    "class": model.names[int(box.cls[0])],
                    "confidence": float(box.conf[0]),
                    "bbox": {
                        "xmin": float(box.xyxy[0][0]),
                        "ymin": float(box.xyxy[0][1]),
                        "xmax": float(box.xyxy[0][2]),
                        "ymax": float(box.xyxy[0][3])
                    }
                })
        
        return JSONResponse(content={"status": "success", "detections": detections})
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )
    

@app.post("/detect/")
async def detect_objects(url: str = Body(..., embed=True)):
    try:
        response = requests.get(url)
        img_bytes = response.content
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        results = model.predict(img)
        
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                detections.append({
                    "class": model.names[int(box.cls[0])],
                    "confidence": float(box.conf[0]),
                    "bbox": {
                        "xmin": float(box.xyxy[0][0]),
                        "ymin": float(box.xyxy[0][1]),
                        "xmax": float(box.xyxy[0][2]),
                        "ymax": float(box.xyxy[0][3])
                    }
                })
        
        return JSONResponse(content={"status": "success", "detections": detections})
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

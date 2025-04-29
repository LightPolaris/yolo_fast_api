from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from ultralytics import YOLO
from typing import List, Dict, Any
import cv2
import numpy as np

app = FastAPI()

model = YOLO("best.pt")

@app.post("/detect/")
async def detect_objects(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        nparr = np.frombuffer(image_data, np.uint8)
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

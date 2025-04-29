FROM ultralytics/ultralytics:latest-cpu

WORKDIR /ultralytics
COPY ./best.pt /ultralytics/best.pt
COPY ./main.py /ultralytics/main.py

RUN pip install fastapi -i https://pypi.tuna.tsinghua.edu.cn/simple/ 
RUN pip install "uvicorn[standard]" -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip install python-multipart -i https://pypi.tuna.tsinghua.edu.cn/simple/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

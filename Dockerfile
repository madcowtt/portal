FROM tensorflow/tensorflow:1.13.2-gpu
#FROM tensorflow/tensorflow:2.7.0-gpu-jupyter

COPY data/requirements.txt ./
RUN apt update
RUN apt install -y python3-pip
RUN apt install -y vim
RUN pip install --no-cache-dir --upgrade pip && \
pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt
COPY client_code_wrapper3.py /
RUN chmod +x /usr/local/bin/ai-benchmark

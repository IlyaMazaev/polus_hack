FROM python:3.8

RUN pip install fastapi uvicorn
RUN apt-get update -y
RUN apt install libgl1-mesa-glx -y
RUN apt-get install 'ffmpeg' 'libsm6' 'libxext6' -y
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /polus_hack_back

WORKDIR /polus_hack_back

COPY ./app /polus_hack_back/app
COPY ./model /polus_hack_back/model

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

FROM python:3.8


RUN apt-get update -y
RUN apt install libgl1-mesa-glx -y
RUN apt-get install 'ffmpeg' 'libsm6' 'libxext6' -y
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /polus_hack_back

WORKDIR /streamlit_app

COPY ./streamlit_app /streamlit_app

EXPOSE 8080
CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]

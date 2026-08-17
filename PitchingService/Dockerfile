FROM python:3.10.7
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=$PYTHONPATH:/code/
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
ADD ./ /code/
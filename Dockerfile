FROM --platform=linux/amd64 python:3.10-slim-bullseye

ENV PORT 8080
EXPOSE $PORT

WORKDIR /app

# this is where images will go
RUN mkdir /app/static
ENV UPLOAD_DIR /app/static

ENV MODEL_DIR /model

ADD requirements.txt /app
RUN pip3 install -r requirements.txt


# do this last since ill be changing this most frequently as i develop
ADD web-app/. /app


# Run the service
CMD [ "python", "web.py" ]


# docker build -t web-app .
# docker run -p 8080:8080 -it web-app
# docker run -it web-app 2>&1 | tee caraline-docker-run.out

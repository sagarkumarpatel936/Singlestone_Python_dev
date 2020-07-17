FROM python:3.7

ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV AWS_BUCKET_NAME=""

WORKDIR /usr/src/
COPY . .
RUN pip install -r requirements.txt
CMD [ "python3", "app.py ${AWS_ACCESS_KEY_ID} ${AWS_SECRET_ACCESS_KEY} ${AWS_BUCKET_NAME}"]

FROM python:3.7-slim

RUN pip3 install --upgrade pip \
    && apt-get update

WORKDIR /twitter_sentimental

COPY . /twitter_sentimental

RUN pip3 install pytorch-pretrained-bert nltk pandas numpy Flask flask-cors tweepy

EXPOSE 5000

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
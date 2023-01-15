# Dockerfile, Image, Container
FROM python:3.11

RUN pip install requests beautifulsoup4 praw openai

ADD python ./

CMD [ "python3", "./main.py"]
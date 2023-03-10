# Dockerfile, Image, Container
FROM python:3.11

WORKDIR /python

ADD python ./

RUN pip install requests beautifulsoup4 praw openai python-dotenv

CMD ["python3", "main.py"]
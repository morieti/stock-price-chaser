FROM python:3.11

RUN apt update
RUN mkdir -p /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Tehran

RUN apt update && apt install gettext vim apt-utils -y && apt autoclean

RUN pip install --upgrade pip --ignore-installed
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
ENTRYPOINT ["sh","./entrypoint.sh"]

# docker build -t mollys:latest .

FROM python:2.7.18-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt-get install -y libcairo2-dev libcairo2 python-cairo python-cairo-dev \
   pkg-config gettext libpq-dev libyaml-dev \
   libldap2-dev libsasl2-dev libjpeg-dev zlib1g-dev libgtk2.0-dev \
   libgirepository1.0-dev \
   procps python-apt python3-cairo python3-cairo-dev

RUN pip install --upgrade pip
WORKDIR /srv/mollys

COPY src/requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .

RUN mv entrypoint.sh /
RUN chmod +x /entrypoint.sh

RUN apt-get clean && apt-get autoremove

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "mollys.wsgi:application", "--bind",  ":8000"]

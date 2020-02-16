FROM python:3.7

MAINTAINER @pomo_mondreganto

ENV PYTHONUNBUFFERED=1

ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

ADD . /app
WORKDIR /app
RUN python setup.py install
WORKDIR /

ADD ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
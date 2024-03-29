FROM python:3.9.7-slim-buster

ARG version

LABEL maintainer="Marcelo Arteaga <marcelo.arteaga@klead.tech>"
LABEL version="${version}"

WORKDIR /home/nobody

RUN apt-get update && apt-get install -y \
        pipenv \
    && rm -rf /var/lib/apt/lists/* \
    && chown -R nobody:nogroup /home/nobody

COPY --chown=nobody:nogroup . .

RUN pipenv install --ignore-pipfile --deploy --system

RUN mkdir -p static
RUN python manage.py collectstatic --noinput

EXPOSE $PORT

CMD ["sh", "-c", "waitress-serve --listen=0.0.0.0:$PORT base.wsgi:application"]

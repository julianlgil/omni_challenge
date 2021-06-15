FROM python:3.8

LABEL maintainer="Julian Gil <julianlgil@hotmail.com.com>" version="1.0.0"

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/base.txt \
    && rm -rf /requirements

COPY ./compose/local/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY . /app

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
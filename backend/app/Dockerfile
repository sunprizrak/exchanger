FROM python:3.12.3-alpine3.18

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add --no-cache \
    postgresql-dev \
    postgresql-client \
    gcc \
    python3-dev \
    musl-dev \
    curl \
    libx11 \
    libxcomposite \
    libxrandr \
    libxtst \
    chromium \
    ca-certificates

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app

# copy project
COPY . .


# Set permissions for chromedriver directory
RUN mkdir -p /usr/src/app/.wdm/drivers
RUN chmod -R 755 /usr/src/app/.wdm/drivers

ENV WDM_LOCAL=True
ENV WDM_DIR=/app/.wdm/drivers


ENTRYPOINT ["sh", "/usr/src/app/entrypoint.sh"]
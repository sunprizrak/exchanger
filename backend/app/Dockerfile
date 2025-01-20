###########
# BUILDER #
###########

FROM python:3.12.3-alpine3.18 as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependecies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.12.3-alpine3.18

# create directory for the app
RUN mkdir -p /home/appuser/backend

# create the app user
RUN addgroup -g 1000 appgroup && adduser -u 1000 -G appgroup -S appuser

# create the appropriate directories
ENV HOME=/home/appuser
ENV APP_HOME=/home/appuser/backend/app

# Create directories for static files and media files and work directory
RUN mkdir -p $APP_HOME/static
WORKDIR $APP_HOME

# Install required libraries (libpq for PostgreSQL)
RUN apk update && apk add libpq

# Copy wheels and install dependencies
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# copy entrypoint.sh
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh
RUN chmod +x $APP_HOME/entrypoint.sh

# chown all the files to the app user
RUN chown -R appuser:appgroup $HOME

# change to the app user
USER appuser

ENTRYPOINT ["sh", "/home/appuser/backend/app/entrypoint.sh"]
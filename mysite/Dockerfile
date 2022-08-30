FROM python:3.6

# create root directory for our project in the container
RUN mkdir /yt_fetch_api

# Set the working directory to /yt_fetch_api
WORKDIR /yt_fetch_api

# Copy the current directory contents into the container at /yt_fetch_api
ADD . /yt_fetch_api/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

CMD [ "python", "./manage.py runserver 0.0.0.0:8000" ]
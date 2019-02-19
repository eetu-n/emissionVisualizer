# Use the latest version of python for the base image
FROM python:latest

# Create the uwsgi user
RUN useradd -ms /bin/bash uwsgi

# Choose an arbitrary working directory
WORKDIR /home/uwsgi

# Install the virtual environment
COPY requirements.txt requirements.txt
RUN python -m venv .env
RUN .env/bin/pip install --upgrade pip
RUN .env/bin/pip install -r requirements.txt

# Copy all the relevant resources for the app to run
COPY wsgi.py wsgi.py
COPY emissionVisualizer.ini emissionVisualizer.ini
COPY app.py app.py
COPY apiCaller.py apiCaller.py
COPY templates templates
COPY static static

# The command that is run when the container is started, here launching uWSGI
CMD [".env/bin/uwsgi", "--ini", "emissionVisualizer.ini"
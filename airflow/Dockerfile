FROM apache/airflow:2.8.0-python3.11

ARG CURRENT_USER=$USER

USER root
# Install Python dependencies to be able to process the wheels from the private PyPI server.
RUN apt-get -y update && ACCEPT_EULA=Y apt-get -y upgrade
RUN apt-get install -y python3.11-distutils python3.11-dev build-essential
USER ${CURRENT_USER}

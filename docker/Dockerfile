FROM python:3.10-bookworm

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Install module and dependencies
RUN apt-get update && apt-get install -y --force-yes gcc
RUN pip install git+https://github.com/valentina-lacivita/pointcloud.git

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Install application into container
COPY cpoints.py .

# Run the application
ENTRYPOINT ["python", "cpoints.py"]

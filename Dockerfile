FROM apache/airflow:2.6.3-python3.10

USER root


RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    vim \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# # We need wget to set up the PPA and xvfb to have a virtual screen and unzip to install the Chromedriver
# RUN apt-get update && \ 
#     apt-get install -y wget xvfb unzip --no-install-recommends

# # Set up the Chrome PPA
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# # Update the package list and install chrome
# RUN apt-get update -y
# RUN apt-get install -y google-chrome-stable

# # Set up Chromedriver Environment variables
# ENV CHROMEDRIVER_VERSION 114.0.5735.90
# ENV CHROMEDRIVER_DIR /chromedriver
# RUN mkdir $CHROMEDRIVER_DIR

# # Download and install Chromedriver
# RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
# RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# # Put Chromedriver into the PATH
# ENV PATH $CHROMEDRIVER_DIR:$PATH

USER airflow

COPY requirements.txt /
COPY etl /opt/airflow/etl


RUN pip install --no-cache-dir --user apache-airflow==${AIRFLOW_VERSION} -r /requirements.txt


FROM apache/airflow:latest-python3.9

USER root

COPY entrypoint.sh /entrypoint.sh

# Make sure the script is executable
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]


RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    vim \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow



COPY requirements.txt .
RUN pip install -r requirements.txt


# Instead of copying the entire application code, copy only the Airflow DAGs
COPY dags/ /usr/local/airflow/dags/

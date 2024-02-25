This is a project for downloading your transaction data from Bank of America using the bofa_scraper project and loading it into the Firefly III financial management software. The multiple steps in this process are managed by Apache Airflow.

bofa_scraper uses Selenium to traverse the BoA site and scrape transaction data from it. It will launch a terminal in which you will handle two-factor authentication to sign in.

Airflow will monitor the downloading of transaction data and when it determines that it is finished will copy the data to the Firefly directory and then call Firefly's import API to load the data.

# Configuration:

Add directories for your downloaded statements and place they will be copied before Firefly imports them to figureman/config.yaml

bofa_scraper looks to a login.txt file in your home directory that contains the following four lines:

    BOA_USERNAME
    BOA_PASSWORD
    DOWNLOAD_DIR (same as in config.yaml)
    ACCOUNTS (Comma-separated list of BoA accounts and cards)

# Setup:

Inside the top-level `figureman` directory

    export AIRFLOW_HOME=./airflow
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    aiflow standalone &
    cp airflow_dags/* /airflow/dags/

# Running:

The pipleline DAG will appear in the airflow web UI under ImportToFirefly. Unless and until the 2FA can be automated, this running on a schedule is not particularly useful. So it simply runs ad-hoc when you prompt it in the UI.

## TODO:

1. Currently this works with a separate Firefly instance running in a Docker container. Add to the instructions and setup how to do this inside of figureman

MIT License

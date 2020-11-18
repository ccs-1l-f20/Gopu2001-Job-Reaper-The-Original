# Jobbing-GUI Extension

Jobbing-GUI Extension, also known as Jobbing-GUI Version E, is a Python application meant to keep a track on jobs from a specific set of companies. The list of companies that were used for this project can be found on the [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1057brcM4eALpCzIQWLOM3C6mvXfoAGp8n8XnYJFzbTc/).

<!-- ## Installation

A public version of this project has not yet been released, but if you wish, you may clone this repository, and start keeping track of jobs by running main.py like so:

```bash
python3.8 main.py
```

This will take approximately 1 minute to gather all of the data.

The web and desktop interfaces will be available soon. -->

## Usage Requirements

Please pip install the following packages. Note that the version of Python used is 3.8.

```bash
pip install sqlite3 PyPDF2 google-api-python-client google-auth-httplib2 google-auth-oauthlib selenium bs4 flask flask_restful flask_sqlalchemy
```

You may need to install sqlite3 if you have not already.

## Running the code

In navigating this project, keep in mind the following:
* run main.py to populate cities.db
* run web.py to run flask server
* run scrape_struct.py to populate ml_jobs.db (which is used by web.py)
* you will require a token.pickle &/ credentials.json file to run scrape_struct.py -- will receive on request
* All html files are templates which are used with web.py
* run job_classifier.py to train the BERT model
* run 'naiveBayes jobs.py' to train the Naive Bayes model
* run giant.py to populate giant.db for use with training the models listed above
* You may notice some errors with can't find file or related errors as some organization took place after so as to declutter the main folder. Contact me if you have any questions with finding any file.

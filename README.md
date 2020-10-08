# Jobbing-GUI Extension

Jobbing-GUI Extension, also known as Jobbing-GUI Version E, is a Python application meant to keep a track on jobs from a specific set of companies. The list of companies that were used for this project can be found on the [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1057brcM4eALpCzIQWLOM3C6mvXfoAGp8n8XnYJFzbTc/).

## Installation

A public version of this project has not yet been released, but if you wish, you may clone this repository, and start keeping track of jobs by running main.py like so:

```bash
python3.8 main.py
```

This will take approximately 1 minute to gather all of the data.

The web and desktop interfaces will be available soon.

## Usage Requirements

Please pip install the following packages. Note that the version of Python used is 3.8.

```bash
pip install sqlite3 PyPDF2 google-api-python-client google-auth-httplib2 google-auth-oauthlib selenium bs4 flask flask_restful flask_sqlalchemy
```
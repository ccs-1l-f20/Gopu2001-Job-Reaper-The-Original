# scrapeStruct.py
# Anmol Kapoor

# Modules for GS CSV file
import pickle, os.path, pandas as pd
# Modules for Scraping
from importlib import import_module
# Modules for Running Predictions
import sys, time, os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from transformers import AutoModel, BertTokenizerFast
import torch
import torch.nn as nn
import numpy as np
import time
import sqlite3 as sql

# These are constant variables
device = torch.device("cpu")
bert = AutoModel.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')

class BERT_Arch(nn.Module):
    def __init__(self, bert):
        super(BERT_Arch, self).__init__()
        self.bert = bert
        # dropout layer
        self.dropout = nn.Dropout(0.2)
        # relu activation function
        self.relu =  nn.ReLU()
        # dense layer 1
        self.fc1 = nn.Linear(768,512)
        # dense layer 2 (Output layer)
        self.fc2 = nn.Linear(512,2)
        #softmax activation function
        self.softmax = nn.LogSoftmax(dim=1)
    #define the forward pass
    def forward(self, sent_id, mask):
        #pass the inputs to the model
        _, cls_hs = self.bert(sent_id, attention_mask=mask)
        x = self.fc1(cls_hs)
        x = self.relu(x)
        x = self.dropout(x)
        # output layer
        x = self.fc2(x)
        # apply softmax activation
        x = self.softmax(x)
        return x

def load_model():
    bert_model = BERT_Arch(bert)
    try:
        bert_model.load_state_dict(torch.load("NLP_Practice/saved_weights.pt"))
    except:
        print("I was unable to successfully load the pre-trained model.")
        print("If you do not have 'NLP_Practice/saved_weights.pt' in your repo,", end=" ")
        print("you may want to train the model again by running job_classifier.py,", end=" ")
        print("or download a trained model (link below) and place it in the", end=" ")
        print("NLP_Practice folder.\n\thttps://bit.ly/saved_weights")
        sys.exit(1)
    # with open("NLP_Practice/naive_bayes.pickle", "rb") as file:
    #     nb = pickle.load(file)
    # with open("NLP_Practice/nb_counter.pickle", "rb") as file:
    #     cv = pickle.load(file)
    # return (bert_model, (nb, cv))
    return bert_model

def get_predictions(model, strings): # strings is an array of strings to test against
    # bert_model, nb = model
    strings_lo = [string.lower() for string in strings]
    tokens_test = tokenizer.batch_encode_plus(
        strings_lo,
        max_length = 25,
        padding='max_length',
        truncation=True
    )
    test_seq = torch.tensor(tokens_test['input_ids'])
    test_mask = torch.tensor(tokens_test['attention_mask'])
    with torch.no_grad():
        preds = model(test_seq.to(device), test_mask.to(device))
        preds = preds.detach().numpy()
    preds = np.argmax(preds, axis=1)
    # nb_preds = nb[0].predict(nb[1].transform(strings))
    # preds = bert_preds + nb_preds - 1
    job_strings = []
    for prediction in range(len(preds)):
        if preds[prediction] == 1:
            job_strings.append(strings[prediction])
    return job_strings

'''
This part in the project accesses the spreadsheet at
docs.google.com/spreadsheets/d/1057brcM4eALpCzIQWLOM3C6mvXfoAGp8n8XnYJFzbTc/ to
populate the job_links list, which will hold the names of all companies in
consideration for a job and their job page. To ensure the safety and security of
this google spreadsheet, I have limited this spreadsheet to readonly for
outsiders.

job_links:
    (company's name, company's careers page url)
'''

def __INIT_GS_API():
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRGRGTwZ6BY3yxYJZBNlMqQVPNrqiySkYpGlyHAZymxSIjP-6aMOqPpuA-HwOuZRgQRyQj8SrRvjFt3/pub?gid=0&single=true&output=csv")
    job_links = list(zip(df["Company Name"].tolist(), df["Job Page Link"].tolist()))
    # print(job_links[0:3]) # Test works!
    return job_links[2:3]

def get_cnxn(src):
    conn, curs = None, None
    try:
        conn = sql.connect(src)
        curs = conn.cursor()
    except sql.Error as e:
        print(e)
        if os.path.exists(src):
            curs.close()
            conn.close()
        sys.exit(1)
    return conn, curs

def submit_report(jobs):
    print("Report:")
    print("\tNumber of Jobs found:", len(jobs))
    print("\tNumber of Companies: ", end="")
    companies = []
    for company, _, _ in jobs:
        if company not in companies:
            companies.append(company)
    print(len(companies))
    # time to save
    src = "ml_jobs.db"
    if os.path.exists(src):
        os.remove(src)
    conn, curs = get_cnxn(src)
    curs.execute('create table jobs ( company nvarchar(20), title nvarchar(120), link nvarchar(175) )')
    conn.commit()
    insertion_cmd = "insert into jobs (company, title, link) values "
    last = False
    for match in jobs:
        if match == jobs[-1]:
            last = True
        # print(type(match[0]), type(match[1]), type(match[2]))
        company = match[0].replace("'", "")
        title = match[1].replace("'", "")
        link = match[2]
        insertion_cmd += f"('{company}', '{title}', '{link}')"
        if not last:
            insertion_cmd += ", "
    curs.execute(insertion_cmd)
    conn.commit()
    # close the sqlite3 connection
    curs.close()
    conn.close()

'''
This part will scan the website for probable job titles and return them.
'''

def __INIT_JOB_SCAN(job_links):
    structurizer = import_module("structurizer")
    jobs = []
    for board in job_links:
        print("Loading data from", board[0] + "...")
        web = structurizer.Website(company=board[0], url=board[1])
        count = 0
        start_time = time.time()
        paths = []
        for job_title in get_predictions(load_model(), web.get_text()):
            path = web.get_path(job_title)
            if path not in paths and path != None:
                for match in web.get_by_path(path):
                    if 'job' in match[1] or 'career' in match[1]:
                        count += 1
                        jobs.append((web.company, match[0].strip(), match[1].strip()))
                    # else:
                        # print("Not matched:", match[0].strip(), "|", match[1])
                paths.append(path)
        print("\tCompleted in", str(time.time()-start_time) + "s.")
        print("\tFound", count, "jobs @", web.company)
        # print("\tSo far I have collected", len(jobs), "jobs.")
    submit_report(jobs)

if __name__ == '__main__':
    __INIT_JOB_SCAN(__INIT_GS_API())

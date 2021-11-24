from tokenize import Ignore
from django.http.response import HttpResponse
from django.shortcuts import render
import pandas as pd
from bert_serving.client import BertClient
import numpy as np
import os
import urllib.parse

home_info=''
questions_encoded = False
current_page=0
# Create your views here.

def home(request):
    try:
        page = request.GET['value']
        global current_page
        if page == 'next':
            current_page = current_page + 11
        if page == 'previous':
            current_page = current_page - 11
    except:
        pass    
    data = get_housing_info()
    return render(request, 'home.html', {'data':data.loc[current_page:current_page+11]})

def selected_house(request):
    addr = request.GET['value']
    data = get_housing_info()
    global home_info
    home_info = data[data['address'] == addr]
    return render(request, 'housing.html', {'data': home_info})
       

def answer(request):
    question = request.GET['question']
    data = get_all_questions()
    if questions_encoded == False:
        encode_questions(data)
    answer, score, predicted_question = get_question_answer(data, question)
    redfin_data = get_housing_info()
    requested_data = redfin_data.loc[2][answer]
    return render(request, 'result.html', {'question': question, 
    'predicted_question' : predicted_question, 
    'answer' : requested_data, 
    'score' : score,
    'data' : home_info})

def get_all_questions():
    cwd = os.getcwd()
    questions_data = pd.read_csv(cwd+'/Bert/Data/AllQuestions.csv')
    return questions_data

def encode_questions(data):
    bertclient = BertClient()
    questions = data["Question"].values.tolist()
    questions_encoder = bertclient.encode(questions)
    np.save("questions", questions_encoder)
    questions_encoder_len = np.sqrt(
        np.sum(questions_encoder * questions_encoder, axis=1)
    )
    np.save("questions_len", questions_encoder_len)
    global questions_encoded
    questions_encoded = True

def get_question_answer(data, question):
    bert_client = BertClient()
    questions_data = data["Question"].values.tolist()
    answers_data = data["Answer"].values.tolist()
    questions_encoder = np.load("questions.npy")
    questions_encoder_len = np.load("questions_len.npy")

    query_vector = bert_client.encode([question])[0]
    score = np.sum((query_vector * questions_encoder), axis=1) / (
            questions_encoder_len * (np.sum(query_vector * query_vector) ** 0.5)
    )
    top_id = np.argsort(score)[::-1][0]
    if float(score[top_id]) > 0.5:
        return answers_data[top_id], score[top_id], questions_data[top_id]
    return "Sorry, I didn't get you.", score[top_id], questions_data[top_id]

def get_housing_info():
    cwd = os.getcwd()
    redfin_data = pd.read_csv(cwd+'/Bert/Data/AllCounties_Data.csv')
    redfin_data.columns= redfin_data.columns.str.lower()
    redfin_data = fix_data_types(redfin_data)
    return redfin_data

def fix_data_types(redfin_data):
    redfin_data['zip or postal code'] = redfin_data['zip or postal code'].astype(str)
    redfin_data['zip or postal code'] = redfin_data['zip or postal code'].str.replace(".0", "", regex=False)
    redfin_data['beds'] = redfin_data['beds'].fillna(0)
    redfin_data['beds'] = redfin_data['beds'].astype(int)
    redfin_data['baths'] = redfin_data['baths'].astype(str)
    redfin_data['baths'] = redfin_data['baths'].str.replace(".0", "", regex=False)
    redfin_data['price'] = redfin_data['price'].fillna(0)
    redfin_data['price'] = redfin_data['price'].astype(int)
    redfin_data['square feet'] = redfin_data['square feet'].fillna(0)
    redfin_data['square feet'] = redfin_data['square feet'].astype(int)
    redfin_data['lot size'] = redfin_data['lot size'].fillna(0)
    redfin_data['lot size'] = redfin_data['lot size'].astype(int)
    redfin_data['year built'] = redfin_data['year built'].fillna(0)
    redfin_data['year built'] = redfin_data['year built'].astype(int)
    redfin_data['days on market'] = redfin_data['days on market'].fillna(0)
    redfin_data['days on market'] = redfin_data['days on market'].astype(int)
    redfin_data['$/square feet'] = redfin_data['$/square feet'].map(lambda x: '{0:.2f}'.format(x)) 
    redfin_data['hoa/month'] = redfin_data['hoa/month'].map(lambda x: '{0:.2f}'.format(x))
    return redfin_data

def get_answer(request):
    question = request.GET['question']
    data = get_all_questions()
    if questions_encoded == False:
        encode_questions(data)
    answer, score, predicted_question = get_question_answer(data, question)
    # redfin_data = get_housing_info()
    requested_data = home_info[answer]
    return HttpResponse(requested_data)

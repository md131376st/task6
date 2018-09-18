from django.shortcuts import render, redirect
# from django.http import Http404
from django.http import HttpResponse
from django.contrib import messages
from .form import Myform
from .models import CsvDoc
import numpy as np
import csv
import codecs
# from rest_framework import generics
# from .serializers import RequestSerializer
from django.shortcuts import render

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.externals import joblib


def create_and_save_model():
    data = pd.read_csv('./character-predictions_pose.csv')
    data4 = pd.read_csv('./uci-news-aggregator.csv')
    for column in data.columns:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column].astype(str))
        if data[column].dtype == type(object):
            data[column] = le.fit_transform(data[column])
            # Fit label encoder and return encoded labels

    for column in data4.columns:
        le = LabelEncoder()
        data4[column] = le.fit_transform(data4[column].astype(str))
        if data4[column].dtype == type(object):
            data4[column] = le.fit_transform(data4[column])
            # Fit label encoder and return encoded labels
    x = data.drop('isAlive', axis=1)
    y = data['isAlive']
    x2 = data4.drop('CATEGORY', axis=1)
    y2 = data4['CATEGORY']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    x2_train, x2_test, y2_train, y2_test = train_test_split(x2, y2, test_size=0.2)

    gnb1 = GaussianNB()
    gnb2 = MultinomialNB()
    gnb3 = BernoulliNB()

    gnb1.fit(x_train, y_train)
    y_pred = gnb1.predict(x_test)
    # data = pd.read_csv('test/test5.csv')
    # for column in data.columns:
    #     le = LabelEncoder()
    #     data[column] = le.fit_transform(data[column].astype(str))
    #     if data[column].dtype == type(object):
    #         data[column] = le.fit_transform(data[column])
    # print("cheaking if the prdictions are the same")
    # print(gnb1.predict(data))
    # print(gnb1)
    # print(x_train)
    print(gnb1.score(x_test, y_test))



    gnb2.fit(x2_train, y2_train)
    y2_pred = gnb2.predict(x2_test)
    print(gnb2.score(x2_test, y2_test))

    gnb3.fit(x_train, y_train)
    y_pred = gnb3.predict(x_test)
    print(gnb3.score(x_test, y_test))

    gnb3.fit(x2_train, y2_train)
    y3_pred = gnb3.predict(x2_test)
    print(y3_pred)
    print(gnb3.score(x2_test, y2_test))



    joblib.dump(gnb1, 'Gaussian.pkl')
    joblib.dump(gnb2, 'Multinomial.pkl')
    joblib.dump(gnb3, 'Bernoulli.pkl')

    g = CsvDoc(name='Gaussian', csv_file='Gaussian.pkl')
    m = CsvDoc(name='Multinomial',  csv_file='Multinomial.pkl')
    b = CsvDoc(name='Bernoulli',  csv_file='Bernoulli.pkl')

    g.save()
    m.save()
    b.save()

# create_and_save_model()
def model_form_upload(request):
    # create_and_save_model()
    if request.method == 'POST':
        form = Myform(request.POST, request.FILES)
        myfile = request.FILES['csv_file']
        if not myfile.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return redirect('simple_upload')
        if form.is_valid():
            mymodel = CsvDoc.objects.filter(name=request.POST['name'])
            # print(mymodel)
            if not mymodel:
                messages.error(request, 'your model is not valid please try again')
                return redirect('simple_upload')
            mymodel = joblib.load(str(mymodel[0]))
            data = pd.read_csv(myfile)
            for column in data.columns:
                le = LabelEncoder()
                data[column] = le.fit_transform(data[column].astype(str))
                if data[column].dtype == type(object):
                    data[column] = le.fit_transform(data[column])
            try:
                data = mymodel.predict(data)
                data=pd.DataFrame(data,columns=['result'])
                data.style.set_table_styles([{
                    'border - color':  '#1ec0a8'
                     }
                ])
                return HttpResponse(data.to_html(classes='datafram'))
            except ValueError:
                messages.error(request, "invalid data")

            return redirect('simple_upload')
    else:
        form = Myform()
    return render(request, 'simple_upload.html', {
        'form': form
    })



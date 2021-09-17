from __future__ import unicode_literals
import json
from django.shortcuts import render, HttpResponse
from django.conf import settings
from API import reddit_flair_prediction as rdf
import sys
import pandas as pd
# Create your views here.

def index(request):
    
    if request.method == 'POST':
        
        model = settings.MODEL_FILE
        val = request.POST.get('url')
        return render(request,"flair_detector/index.html",{"output":rdf.detect_flair(val,model)[0]})

    return render(request,"flair_detector/index.html")

def statistics(request):

    topics_data = pd.read_csv(settings.DATA_PATH)

    #Comments vs Upvotes
    df = topics_data.groupby(['flair']).sum()
    percent = (df)*100/(df.sum()).to_dict()
    
    topics_data['timestamp'] = pd.to_datetime(topics_data['timestamp'])

   
    return render(request,"flair_detector/statistics.html", {"comup": json.dumps(percent.to_dict())})

sys.stdout.flush()
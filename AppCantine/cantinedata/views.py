from .apps import CantinedataConfig

from django.shortcuts import render
from django.db.models import Sum
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import coreapi

import datetime

from cantinedata.models import Fréquentation
from cantinedata.models import Prediction

# Create your views here.

from .models import Fréquentation

@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_freqs = Fréquentation.objects.all().count()
    num_reel = Fréquentation.objects.aggregate(Sum('reel'))['reel__sum']
    num_dates = Fréquentation.objects.values('date').distinct().count()
    num_noms = Fréquentation.objects.values('nom_site').distinct().count()

    context = {
        'num_freqs': num_freqs,
        'num_reel': num_reel,
        'num_dates': num_dates,
        'num_noms': num_noms,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

@login_required
def pick_day(request):
    """View function for home pick day page of site."""
    context = {}
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'pickday.html', context=context)

@login_required
def show_pred(request):
    """View function for show prediction page of site."""
    date1 = str(request.POST.get('datetimepicker'))
    
    getUSdate = lambda string1 : str(datetime.datetime.strptime(string1,"%d.%m.%Y").date())
        
    client=coreapi.Client()
    url1 = 'http://127.0.0.1:8000/cantinedata/prediction/?date=' + getUSdate(date1)     # works with '2011-01-03'
    response = client.get(url1)

    freq1 = int(response) 

    context = {
        'date1':date1 ,
        'freq1':freq1,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'showprediction.html', context=context)

@login_required
def store_pred(request):
    """View function for store prediction of site."""
  
    strEU2date = lambda string1 : datetime.datetime.strptime(string1,"%d.%m.%Y").date()
    
    date1 = strEU2date(request.POST.get('date'))
    freq1 = int(request.POST.get('pred'))
    
    if Prediction.objects.filter(date=date1).count() >0 :
        context = {
            'msg1':'Un enregistrement existe déjà à la date du ' + str(date1)
        }
    else :
        context = {
            'msg1': 'La prédiction de ' + str(freq1) + ' repas a bien été enregistrée au ' + str(date1)
        }
        Prediction.objects.create(date=date1, total_modele=freq1)
    
    
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'storepred.html', context=context)


def store_manuel(request):
    """View function for store prediction of site."""
  
    strEU2date = lambda string1 : datetime.datetime.strptime(string1,"%d.%m.%Y").date()
    
    id1 = int(request.POST.get('id_pred'))
    value1 = int(request.POST.get('value_pred'))
    
    if Prediction.objects.filter(id=id1).count()==1:
        pred1 = Prediction.objects.get(id=id1)
        pred1.total_manuel =  value1
        pred1.save()
        context = {
            'msg1':'Enregistrement effectué',
            'pred1': pred1
        }
        
    else :
        context = {
            'msg1': 'Erreur : Identifiant non unique'
        }
    
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'store_manuel.html', context=context)

@login_required
def prediction(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_freqs = Fréquentation.objects.all().count()


    context = {
        'num_freqs': num_freqs,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'prediction.html', context=context)

@login_required
def pred_list(request):
    """View function prediction list of site."""

    # Generate counts of some of the main objects
    total_preds = Prediction.objects.all().count()
    pred_list = Prediction.objects.order_by("date")[:10]

    context = {
        'total_preds': total_preds,
        'pred_list':pred_list
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'pred_list.html', context=context)

@login_required
def list_manuel(request):
    """View function manual list of site."""

    # Generate counts of some of the main objects
    man_list = Prediction.objects.filter(total_manuel=None)
    total_man = man_list.count()
    

    context = {
        'man_list' : man_list,
        'total_man': total_man
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'list_manuel.html', context=context)


@login_required
def list_monit(request):
    """View function manual list of site."""

    # Generate counts of some of the main objects
    dev_list = Prediction.objects.filter(total_manuel=None)
    total_dev = dev_list.count()
    

    context = {
        'dev_list' : dev_list,
        'total_dev': total_dev
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'list_monit.html', context=context)


@login_required
def calcul_totaux(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    predfilt1 = Prediction.objects.filter(total_calcul=None)
    NoneCount1 = predfilt1.count()
    CalcCount1 = 0
    
    for pred in predfilt1:
        freqquer1 = Fréquentation.objects.filter(date=pred.date)
        if freqquer1.count()>0:
            pred.total_calcul = freqquer1.aggregate(Sum('reel'))['reel__sum']
            pred.save()
            CalcCount1 += 1
        else:
            pred.total_calcul = -1 
            pred.save()
    
    context = {
        'NoneCount1':NoneCount1,
        'CalcCount1':CalcCount1,
        'predfilt1':predfilt1
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'calcul_totaux.html', context=context)



class FreqListView(LoginRequiredMixin, generic.ListView):
    model = Fréquentation
    context_object_name = 'freq_list'   # your own name for the list as a template variable
    queryset = Fréquentation.objects.all()[0:5] # Get 5 books containing the title war
    template_name = './freq_list.html'  # Specify your own template name/location


class call_model(APIView):

    def get(self,request):
        if request.method == 'GET':
            # get sound from request
            date1 = str(request.GET.get('date'))
            # build response
            response = CantinedataConfig.predict_model.predict([CantinedataConfig.getDateParam(date1)])

            # return response
            return Response(round(response[0]), status=status.HTTP_200_OK)

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.messages import constants

from .models import Apostila, ViewApostila

def adicionar_apostilas(request):

    if request.method == "GET":
        apostilas = Apostila.objects.filter(user=request.user)
        # TODO: criar as tags
        views_totais = ViewApostila.objects.filter(apostila__user=request.user).count()

        context = {
            'apostilas': apostilas,
            'views_totais': views_totais
        }

        return render(request, 'adicionar_apostilas.html', context)
    elif request.method == "POST":
        titulo = request.POST.get('titulo')
        arquivo = request.FILES['arquivo']

        apostila = Apostila(
            user = request.user,
            titulo = titulo,
            arquivo = arquivo
        )

        apostila.save()

        messages.add_message(request, constants.SUCCESS, "Apostila salva")
        return redirect('/apostilas/adicionar_apostilas')
    
def apostila(request, id):

    apostila = Apostila.objects.get(id=id)
    views_totais = ViewApostila.objects.filter(apostila=apostila).count()
    views_unicas = ViewApostila.objects.filter(apostila=apostila).values('ip').distinct().count()


    view = ViewApostila(
        ip = request.META['REMOTE_ADDR'],
        apostila = apostila
    )
    view.save()

    context = {
        'apostila': apostila,
        'views_totais': views_totais,
        'views_unicas': views_unicas
    }

    return render(request, 'apostila.html', context)
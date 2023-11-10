from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request,"index.html")

def show_siping(request):
    return render(request,"siping.html")

def show_jiading(request):
    return render(request,"jiading.html")
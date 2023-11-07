from django.shortcuts import render

# Create your views here.
def navi(request):
    return render(request,"index.html")

def jiading_view(request):
    return render(request,"jiading.html")

def siping_view(request):
    return render(request,"siping.html")
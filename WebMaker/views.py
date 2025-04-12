from django.shortcuts import render

# Create your views here.
def WebMakerIndex(request):
    return render(request, 'WebMakerT/index.html')
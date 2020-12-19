import re
import os
import PyPDF2
from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from pathlib import Path
from . models import Files

BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.


def basepage(request):
    c = request.COOKIES.get('csrftoken')
    F = Files.objects.filter(Key=c).order_by("-id")
    result = []
    keywords = None
    if request.method == "POST":
        try:
            for file in request.FILES.getlist("files"):
                allFiles = Files(File_Name=file, File=file, Key=c)
                allFiles.save()
        except Exception as e:
            print(e)
            return HttpResponse("<script>alert('Something went wrong, Try Again');window.location.href='/';")
    elif request.method == "GET":
        if request.GET.get('delete') == "True":
            F.delete()
            return redirect('/')
        if F and request.GET.get('keyword'):
            keywords = request.GET.get('keyword').lower()
            arr = keywords.split(",")
            for item in F:
                full_path = os.path.abspath(settings.URL + str(item.File))
                file = PyPDF2.PdfFileReader(full_path)
                Pages = file.getNumPages()
                item = ap(arr, item, file, Pages)
                if item:
                    result.append(item)
    context = {
        'Files': F,
        'Found_item': result,
        'keywords': keywords
    }
    return render(request, "home.html", context)


def ap(arr, item, file, Pages):
    for i in range(0, Pages):
        pageObj = file.getPage(i)
        text = pageObj.extractText().lower()
        for k in arr:
            for match in re.finditer(k, text):
                return [item.File_Name, item.File, Pages]

from django.http import HttpResponse
import datetime
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context,RequestContext
import os,sys,string


def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})

def hours_ahead(request, offset):
    offset = int(offset)
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def show_chart(request):
    xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
    chartdata = {'x': xdata, 'y': ydata}
    charttype = "pieChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata
    }
    return render_to_response('piechart.html', data)

def error_page(request,err_msg='Page not Found',pic='background'):
    t = get_template('error_page_fit.html')
    html = t.render(RequestContext(request,{'err_msg': err_msg,'pic':pic}))
    return HttpResponse(html)


def show_score(request,score_file):
    if not os.path.exists(score_file):
       error_page(request,"File doesn't exist: %s"%score_file) 


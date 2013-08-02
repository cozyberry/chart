from django.http import HttpResponse
import datetime
import time
import random
import settings
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context,RequestContext
import os,sys,string
import numpy as np
import csv
import pprint
from utilities import add_suffix

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})

def hours_ahead(request, offset):
    offset = int(offset)
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def show_2linechart_demo(request):
    """
    lineChart page
    """
    start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
    nb_element = 100
    xdata = range(nb_element)
    xdata = map(lambda x: start_time + x * 1000000000, xdata)
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata)

    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"},
                   "date_format": tooltip_date}
    chartdata = {'x': xdata,
                 'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie,
                 'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie}
    charttype = "lineChart"
    data = {
        'charttype0': charttype,
        'chartdata0': chartdata,
        'charttype1': charttype,
        'chartdata1': chartdata
    }
    t = get_template('row-grid.html')
    html = t.render(RequestContext(request,data))
    return HttpResponse(html)
    #return render_to_response('row-grid.html',data)

def show_chart(request):
    xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
    chartdata = {'x': xdata, 'y': ydata}
    charttype = "pieChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata
    }
    #t = get_template('piechart.html')
    #html = t.render(Context(data))
    #tmp=open('srcpiechart.html','w')
    #print >>tmp,html
    #tmp.close()
    #return HttpResponse(html)
    return render_to_response('piechart.html', data)

def gen_multicharts_template(nchart,template):
    print >> template,"""<!DOCTYPE html>
<html>
{% load nvd3_tags %}"""
    print >> template,"<head>"
    print >> template,"{% include_nvd3jscss %}"
    for i in range(nchart):
        print >>template,'{%% load_chart charttype%d chartdata%d "chart_container%d" %%}'%(i,i,i)
    print >> template,"""<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>"""
    print >> template,"""
<link rel="stylesheet" type="text/css" href="{{ STATIC_URL }}/css/bootstrap-responsive.min.css">
<link rel="stylesheet" type="text/css" href="{{ STATIC_URL }}/css/bootstrap.min.css">
<script src="js/jquery.js"></script>
<script src="js/bootstrap.min.js"></script>
<style type="text/css">
body{margin:20px 20px 20px 20px}
h1, h2, h3, .masthead p, .subhead p, .marketing h2, .lead {font-family: "Helvetica Neue";font-weight: normal;}
.show-grid [class*="span"] {
    background-color: #EEEEEE;
    border-radius: 3px 3px 3px 3px;
    line-height: 40px;
    min-height: 40px;
    text-align: center;
}
.show-grid {
    margin-bottom: 20px;
    margin-top: 10px;
}
.show-grid [class*="span"]:hover {
    background-color: #DDDDDD;
}
.show-grid [class*="span"] [class*="span"] {
    background-color: #CCCCCC;
}
.show-grid .show-grid [class*="span"] {
    margin-top: 5px;
}
.show-grid [class*="span"] [class*="span"] [class*="span"] {
    background-color: #999999;
}
.bs-docs-example:after {
    background-color: #F5F5F5;
    border: 1px solid #DDDDDD;
    border-radius: 4px 0 4px 0;
    color: #9DA0A4;
    font-size: 12px;
    font-weight: bold;
    left: -1px;
    padding: 3px 7px;
    position: absolute;
    top: -1px;
}
form.bs-docs-example {
    padding-bottom: 19px;
}
.bs-docs-example {
    background-color: #FFFFFF;
    border: 1px solid #DDDDDD;
    border-radius: 4px 4px 4px 4px;
    margin: 15px 0;
    padding: 39px 19px 14px;
    position: relative;
}
.bs-docs-example-submenus .dropup > .dropdown-menu, .bs-docs-example-submenus .dropdown > .dropdown-menu {
    display: block;
    margin-bottom: 5px;
    position: static;
}
.bs-docs-example-submenus {
    min-height: 180px;
}
</style>"""
    print >> template,"""<body>
    <section>
	<div class="row show-grid">
           <div class="span">{% include_container "chart_container0" 400 600 %}</div>
    </div>
    """

    nrow=int((nchart-1)/2)
    for i in range(nrow):
        print >> template,"""
	<div class="row show-grid">
           <div class="span">{%% include_container "chart_container%d" 400 600 %%}</div>
           <div class="span">{%% include_container "chart_container%d" 400 600 %%}</div>
    </div>"""%(2*i+1,2*i+2)
    if nchart%2 == 0:
        print >> template,"""
	<div class="row show-grid">
           <div class="span">{%% include_container "chart_container%d" 400 600 %%}</div>
    </div>"""%(nchart-1)
    print >>template,"""
    </section>
</body>
</html>"""


def show_stackedareachart(request,rdata):
    """
    stackedareachart page
    """
    
    nb_element = np.size(rdata,axis=0) 
    nb_series  = np.size(rdata,axis=1)-1
    xdata = range(nb_element)
    for i in range(nb_element):
        xdata[i] = rdata[i,0]


    ydata = []
    for j in range(nb_series):
        ydata.append(range(nb_element))

    for j in range(nb_series):
            for i in range(nb_element):
                ydata[j][i] = rdata[i,j+1]-rdata[0,j+1]
                #ydata[j][i] = rdata[i,j+1]-rdata[0,j+1]+rdata[0,-1]
                

    for j in range(1,nb_series):
        for i in range(nb_element):
            ydata[j][i]-=ydata[j-1][i]

        #pprint.pprint(ydata[j])
    extra_serie1 = {"tooltip": {"y_start": "Log MAP: ", "y_end": ""}}
    extra_serie2 = {"tooltip": {"y_start": "BIC Difference: ", "y_end": ""}}
    extra_serie3 = {"tooltip": {"y_start": "Cheeseman_Stutz Score Difference: ", "y_end": ""}}

    #pprint.pprint(ydata)
    chartdata = {
        'x': xdata,
        'name1': 'LOG MAP', 'y1': ydata[0], 'extra1': extra_serie1,
        'name2': 'BIC', 'y2': ydata[1], 'extra2': extra_serie2,
        'name3': 'Cheesman_Stutz Score', 'y3': ydata[2], 'extra3': extra_serie3,
    }
    charttype = "stackedAreaChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata
    }
    return render_to_response('stackedareachart.html', data)

def generate_linechart(rdata):
    """
    lineChart page
    """
    start_year = 2001
    start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
    nb_element = np.size(rdata,axis=0) 
    xdata = range(1,nb_element+1) 

    nb_series  = np.size(rdata,axis=1)-1
    ydata = []
    for j in range(nb_series):
        ydata.append(range(nb_element))

    for j in range(nb_series):
            for i in range(nb_element):
                ydata[j][i] = float(rdata[i,j+1])-float(rdata[0,j+1])
 

    tooltip_date = "%y clusters"
    extra_serie1 = {"tooltip": {"y_start": "", "y_end": ""}
                   ,"date_format": tooltip_date}
    extra_serie2 = {"tooltip": {"y_start": "", "y_end": ""}
                   ,"date_format": tooltip_date}
    extra_serie3 = {"tooltip": {"y_start": "", "y_end": ""}
                   ,"date_format": tooltip_date}

    chartdata = {'x': xdata,
                 'name1': 'LOG MAP ', 'y1': ydata[0], 'extra1': extra_serie1,
                 'name2': 'BIC ', 'y2': ydata[1], 'extra2': extra_serie2,
                 'name3': 'Cheeseman_Stutz Score ', 'y3': ydata[2], 'extra3': extra_serie3}
    #charttype = "lineChart"

    #data = {
        #'charttype': charttype,
        #'chartdata': chartdata
    #}
    #return render_to_response('linechart.html', data)
    return chartdata

def generate_multibarchart(rdata):
    """
    multibarchart page
    """
    #print 'rdata'
    #print rdata
    nb_element = np.size(rdata,axis=1)-1 
    nvalue = np.size(rdata,axis=0)-1 

    xdata = range(nb_element)
    ydata=[]
    ydata.append(rdata[0,:])
    for i in range(nvalue):
        ydata.append(range(nb_element))
    for i in range(1,nvalue+1):
        #print rdata[i,:]
        for j in range(0,nb_element):
            ydata[i][j] = float(rdata[i,j+1])
        

    extra_serie = {"tooltip": {"y_start": "Probability: ", "y_end": ""}}

    chartdata = dict()
    #nvalue = np.size(rdata,1)-1
    chartdata['x']=xdata
    for i in range(1,nvalue+1):
        chartdata['name%d'%i] = rdata[i,0]
        chartdata['y%d'%i] = ydata[i]
        chartdata['extra%d'%i]=extra_serie
    return chartdata

def error_page(request,pic='lizard',err_msg='Page not Found'):
    t = get_template('error_page.html')
    html = t.render(RequestContext(request,{'err_msg': err_msg,'pic':pic}))
    return HttpResponse(html)


def show_score(request,score_file,chart_type):
    score_file=os.path.join(settings.DATA_ROOT,score_file)

    if not os.path.exists(score_file):
        return error_page(request,err_msg="File doesn't exist: %s"%score_file) 
    else:
        csvreader=csv.reader(open(score_file,'r'))
        ct = 0;
        n = 0
        cts=[]
        ncols=[]
        
        for row in csvreader:
            #print ct
            #print row
            if len(row) == 0:
                if ct != 0:
                    cts.append(ct)
                    n+=1
                ct = 0
            else:
                if ct == 0:
                    ncols.append(len(row))
                ct=ct+1
        if ct!=0:
            cts.append(ct)
            n+=1
        if len(np.unique(ncols)) > 1:
            return error_page(request,err_msg='The column number of file %s is inconsistent!'%score_file)

        data = np.array(-1*np.ones((np.sum(cts),ncols[0]),float),object);
        csvreader=csv.reader(open(score_file,'r'))
        k=0;
        curct=0;
        for row in csvreader:
            if len(row) !=0:
                data[k,:] = np.array(row,str)
                k+=1
        chart_type=int(chart_type)
        #pprint.pprint(data)
        
        if chart_type == 1:
            return show_chart(request)
            #return show_chart(request,score_file,
        elif chart_type == 2:
            #return show_linechart(request,data,title)
            #return show_stackedareachart(request,data)
            return show_linechart(request,data[1:cts[0],:])
        elif chart_type == 3:
            nchart = len(cts)
            datas=dict()
            datas['charttype0']='lineChart'
            datas['chartdata0']=generate_linechart(data[1:cts[0],:])
            for i in range(1,nchart):
                start=int(np.sum(cts[0:i]))
                end=int(np.sum(cts[0:i+1]))
                datas['charttype%d'%i]='multiBarChart'
                datas['chartdata%d'%i]=generate_multibarchart(data[start:end,:])

            datas['nchart']=len(cts) 
        
            template=add_suffix('multi_charts.html')
            template_file=os.path.join(settings.TEMPLATE_DIRS,template)
            html=open(template_file,'w') 
            gen_multicharts_template(datas['nchart'],html)
            html.close()

            if not os.path.exists(template_file):
                    return error_page(request,err_msg='file does not exist!%s'%template_file)

            t = get_template(template_file)
            html = t.render(RequestContext(request,datas))
            return HttpResponse(html)
            #return render_to_response('multi_charts.html',datas)

        elif chart_type == 0:
            return render_to_response('sample_charts_2.html')
        elif chart_type == 4:
            return show_2linechart_demo(request)
        elif chart_type == 5:
            return render_to_response('2line_chart_src.html')
        
        else:
            return error_page(request,err_msg="Chart type unknown: %s"%chart_type)

def test_list(request):
    datas=dict()
    datas['msg']=[1,2]
    return render_to_response('test_list.html',datas)

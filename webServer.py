#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-08 18:41:47
# @Author  : LiHongyuan (hy.li@8win.com)

from flask import Flask
from flask import request
from flask import render_template
from util.rrdcontroller import RRDController
import os
import time
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def updateRRD():
    pass


def graphImage():
    pass


@app.route('/upload/', methods=['POST'])
def utilData():
    data = request.get_data()
    data = json.loads(data)
    # return render_template('index.html',data=data)
    ipAddress = str(data["ipaddress"])
    serviceName = str(data["Process_Name"])
    #jvmType = str(data["jvmType"])
    rrdFile = '/data/apps/jvm_monitor/%s/%s/%s.rrd' % (
        ipAddress, serviceName, serviceName)
    #staticFile = '/data/apps/jvm_monitor/%s/%s/%s.png' % (ipAddress, serviceName, jvmType)
    staticFile = ''
    print "variable type"
#    print type(rrdFile), type(staticFile)
    print "------------------------"
    rrd = RRDController(rrdfile=rrdFile, static_path=staticFile)
    if os.path.exists(os.path.dirname(rrdFile)) is not True:
        print os.path.dirname(rrdFile)
        os.makedirs(os.path.dirname(rrdFile))
    # if os.path.exists(os.path.dirname(staticFile)) is not True:
    #     print os.path.dirname(staticFile)
    #     os.makedirs(os.path.dirname(staticFile))

    if os.path.isfile(rrdFile) is not True:
        rrd = rrd.create()
    print "recv data success"
    print rrdFile
    result = rrd.update(rrdfile=rrdFile, YGCT_avg=float(data['YGCT_avg']), Heap_used=float(data['Heap_used']),
                        S0_used=float(data['S0_used']), S0_max=float(data['S0_max']), S0_ratio=float(data['S0_ratio']),
                        S1_used=float(data['S1_used']), S1_max=float(data['S1_max']), S1_ratio=float(data['S1_ratio']),
                        Old_used=float(data['Old_used']), Old_max=float(data['Old_max']),
                        Old_ratio=float(data['Old_ratio']), Eden_used=float(data['Eden_used']),
                        Eden_max=float(data['Eden_max']), Eden_ratio=float(data['Eden_ratio']),
                        Metadata_used=float(data['Metadata_used']), Metadata_max=float(data['Metadata_max']),
                        Metadata_ratio=float(data['Metadata_ratio']), Heap_max=float(data['Heap_max']),
                        Heap_ratio=float(data['Heap_ratio']), YGC=float(data['YGC']), FGC=float(data['FGC']),
                        YGCT=float(data['YGCT']), FGCT=float(data['FGCT']), GCT=float(data['GCT']),
                        FGCT_avg=float(data['FGCT_avg']), GCT_avg=float(data['GCT_avg']))

    if result['return_value'] == 0L:
        print "success update value"
    else:
        print "failed update value"

    return "update data success"


@app.route('/getgraph/', methods=["get"])
# request example :
# http://127.0.0.1:5000/getgraph/?ip=192.168.11.129&jvmType=JavaHeapMemory&name=service_account
def getGraph():
    allType = ['JavaS0S1EdenOldMax', 'JavaS0S1EdenOldUsedPercentage', 'JavaHeapMemory',
               'JavaMetadataMemory', 'JavaGCEvents', 'JavaAverageGCTime', 'JavaGCTime']
    imglist = []
    ipAddress = str(request.args.get('ip'))
    jvmType = str(request.args.get('jvmType'))
    serviceName = str(request.args.get('name'))
    print type(allType)
    if jvmType == '':
        for jvmType in allType:
            print "for ....--------" + jvmType
            rrdFile = '/data/apps/jvm_monitor/%s/%s/%s.rrd' % (
                ipAddress, serviceName, serviceName)
            staticFile = '/data/apps/jvm_monitor/%s/%s/%s.png' % (
                ipAddress, serviceName, jvmType)
            print staticFile
            rrd = RRDController(rrdfile=rrdFile, static_path=staticFile)
            print jvmType
            graphFunc = 'graph%s' % (jvmType)
            print graphFunc
            print hasattr(rrd, graphFunc)
            if hasattr(rrd, graphFunc):
                print graphFunc + "will be runnnig........."
                getattr(rrd, graphFunc)(ipAddress=ipAddress,serviceName=serviceName,period='-6h')
                print graphFunc + "is running"
            displayImgName = "static/img/jvm_data/%s/%s/%s.png" % (
                ipAddress, serviceName, jvmType)
            print "++++++++++++++++++++" + displayImgName
            imglist.append(displayImgName)
            print imglist

    else:
        rrdFile = '/data/apps/jvm_monitor/%s/%s/%s.rrd' % (
            ipAddress, serviceName, serviceName)
        print type(rrdFile)
        staticFile = '/data/apps/jvm_monitor/%s/%s/%s.png' % (
            ipAddress, serviceName, jvmType)
        print type(staticFile)
        print staticFile
        rrd = RRDController(rrdfile=rrdFile, static_path=staticFile)
        graphFunc = 'graph%s' % (jvmType)
        print graphFunc
        if hasattr(rrd, graphFunc):
            getattr(rrd, graphFunc)()
        displayImgName = "static/img/jvm_data/%s/%s/%s.png" % (
            ipAddress, serviceName, jvmType)
        print "*******************************"+displayImgName
        imglist.append(displayImgName)
        print imglist
    return ','.join(imglist)
#    return render_template('index.html', staticImg=imglist, mimetype='image/gif')


@app.route('/dashboard', methods=['get'])
def dashboard():
    data = []
    for root, sub, file in os.walk('/root/jvm_monitor_rrdtool/static/img/jvm_data/'):
        if file != []:
            data.append(root.split('/')[-2:])

    hostlist = {}
    for ip, pname in data:
        hostlist.setdefault(ip, []).append(pname)
    return render_template('dashboard.html',hostlist=hostlist)


@app.route('/gethosttypelist', methods=['get'])
def gethosttypelist():

    data = []
    for root, sub, file in os.walk('/root/jvm_monitor_rrdtool/static/img/jvm_data/'):
        if file != []:
            data.append(root.split('/')[-2:])
    print data
    hostlist = {}
    for ip, pname in data:
        hostlist.setdefault(ip, []).append(pname)
    hostlist = json.dumps(hostlist)
    print hostlist
    return hostlist

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# curl -H "Content-Type:application/json" -d '{"Process_Name":
# "service_account", "GCT_avg": "0.010", "S1_max": "4194304.00",
# "S1_ratio": "0.00", "Old_max": "20971520.00", "Heap_max": "62914560.00",
# "YGCT_avg": "0.010", "FGCT_avg": "0", "FGC": "0", "Metadata_used":
# "15324364.80", "Heap_used": "26282803.20", "Eden_max": "33554432.00",
# "Old_used": "10134630.40", "Eden_used": "15132364.80", "YGC": "6",
# "ipaddress": "192.168.11.129", "YGCT": "0.060", "Eden_ratio": "69.94",
# "S0_used": "0.00", "Metadata_max": "15990784.00", "FGCT": "0.000",
# "Old_ratio": "48.33", "Heap_ratio": "41.78", "S0_ratio": "87.26",
# "S1_used": "1015808.00", "S0_max": "4194304.00", "Metadata_ratio":
# "97.30", "GCT": "0.060"}' http://127.0.0.1:5000/upload

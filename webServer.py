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
    return '<h1>Hello World!</h1>'


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
    jvmType = str(data["jvmType"])
    rrdFile = '/data/apps/jvm_monitor/%s/%s/%s.rrd' % (
        ipAddress, serviceName, serviceName)
    staticFile = '/data/apps/jvm_monitor/%s/%s/%s.png' % (
        ipAddress, serviceName, jvmType)
    print "variable type"
    print type(rrdFile), type(staticFile)
    print "------------------------"
    rrd = RRDController(rrdfile=rrdFile, static_path=staticFile)
    if os.path.exists(os.path.dirname(rrdFile)) is not True:
        print os.path.dirname(rrdFile)
        os.makedirs(os.path.dirname(rrdFile))
    if os.path.exists(os.path.dirname(staticFile)) is not True:
        print os.path.dirname(staticFile)
        os.makedirs(os.path.dirname(staticFile))

    if os.path.isfile(rrdFile) is not True:
        rrd = rrd.create()
    print "recv data success"
    result = rrd.update(rrdfile=rrdFile, YGCT_avg=float(data["YGCT_avg"]), Heap_used=float(data['Heap_used']),
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

    rrd.graphJavaS0S1EdenMetadata()

    return "graph success"


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

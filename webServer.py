#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-08 18:41:47
# @Author  : LiHongyuan (hy.li@8win.com)


from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')

def index():
	return '<h1>Hello World!</h1>'

def updateRRD():
	pass

def graphImage():
	pass

@app.route('/upload/', methods=['POST'])
def utilData(data):
	data = request.data()
	return render_template('index.html',data=data)

if __name__ == '__main__':
	app.run(debug=True)



#curl -H "Content-Type:application/json" -d '{"Process_Name": "service_account", "GCT_avg": "0.010", "S1_max": "4194304.00", "S1_ratio": "0.00", "Old_max": "20971520.00", "Heap_max": "62914560.00", "YGCT_avg": "0.010", "FGCT_avg": "0", "FGC": "0", "Metadata_used": "15324364.80", "Heap_used": "26282803.20", "Eden_max": "33554432.00", "Old_used": "10134630.40", "Eden_used": "15132364.80", "YGC": "6", "ipaddress": "192.168.11.129", "YGCT": "0.060", "Eden_ratio": "69.94", "S0_used": "0.00", "Metadata_max": "15990784.00", "FGCT": "0.000", "Old_ratio": "48.33", "Heap_ratio": "41.78", "S0_ratio": "87.26", "S1_used": "1015808.00", "S0_max": "4194304.00", "Metadata_ratio": "97.30", "GCT": "0.060"}' http://127.0.0.1:5000/upload
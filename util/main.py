#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-04 17:17:15
# @Author  : LiHongyuan (hy.li@8win.com)

from rrdcontroller import RRDController
import rrdtool
import os
import time

if __name__ == '__main__':
	cur_time = str(int(time.time()))
	ipAddress = '192.168.11.129'
	serviceName = 'service_account'
	jvmType = 'JAVA_S0_S1_Eden_Metadata'
	rrdFile = '/data/apps/jvm_monitor/%s/%s/%s.rrd' % (ipAddress,serviceName,serviceName)
	staticFile = '/data/apps/jvm_monitor/%s/%s/%s.png' %(ipAddress,serviceName,jvmType)
	rrd = RRDController(rrdfile=rrdFile,static_path=staticFile)
	if os.path.exists(os.path.dirname(rrdFile)) is not True:
		print os.path.dirname(rrdFile)
		os.makedirs(os.path.dirname(rrdFile))
	if os.path.exists(os.path.dirname(staticFile)) is not True:
		print os.path.dirname(staticFile)
		os.makedirs(os.path.dirname(staticFile))

	if os.path.isfile(rrdFile) is not True:
		rrd = rrd.create()
	zdict = {'Process_Name': 'service_account', 'GCT_avg': '0.010', 'S1_max': '4194304.00', 'S1_ratio': '0.00', 'Old_max': '20971520.00', 'Heap_max': '62914560.00', 'YGCT_avg': '0.010', 'FGCT_avg': '0', 'FGC': '0', 'Metadata_used': '15324364.80', 'Heap_used': '26282803.20', 'Eden_max': '33554432.00', 'Old_used': '10134630.40', 'Eden_used': '15132364.80', 'YGC': '6', 'ipaddress': '192.168.11.129', 'YGCT': '0.060', 'Eden_ratio': '69.94', 'S0_used': '0.00', 'Metadata_max': '15990784.00', 'FGCT': '0.000', 'Old_ratio': '48.33', 'Heap_ratio': '41.78', 'S0_ratio': '87.26', 'S1_used': '1015808.00', 'S0_max': '4194304.00', 'Metadata_ratio': '97.30', 'GCT': '0.060'}
	
	result = rrd.update(rrdfile=rrdFile,YGCT_avg=float(zdict['YGCT_avg']),
    Heap_used=float(zdict['Heap_used']),
    S0_used=float(zdict['S0_used']),
    S0_max=float(zdict['S0_max']),
    S0_ratio=float(zdict['S0_ratio']),
    S1_used=float(zdict['S1_used']),
    S1_max=float(zdict['S1_max']),
    S1_ratio=float(zdict['S1_ratio']),
    Old_used=float(zdict['Old_used']),
    Old_max=float(zdict['Old_max']),
    Old_ratio=float(zdict['Old_ratio']),
    Eden_used=float(zdict['Eden_used']),
    Eden_max=float(zdict['Eden_max']),
    Eden_ratio=float(zdict['Eden_ratio']),
    Metadata_used=float(zdict['Metadata_used']),
    Metadata_max=float(zdict['Metadata_max']),
    Metadata_ratio=float(zdict['Metadata_ratio']),
    Heap_max=float(zdict['Heap_max']),
    Heap_ratio=float(zdict['Heap_ratio']),
    YGC=float(zdict['YGC']),
    FGC=float(zdict['FGC']),
    YGCT=float(zdict['YGCT']) ,
    FGCT=float(zdict['FGCT']) ,
    GCT=float(zdict['GCT']),
    FGCT_avg=float(zdict['FGCT_avg']),
    GCT_avg=float(zdict['GCT_avg'])
    )

	if result['return_value'] == 0L:
		print "success update value"
	else:
		print "failed update value"

	rrd.graphJavaS0S1EdenMetadata()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-04 17:17:15
# @Author  : LiHongyuan (hy.li@8win.com)

from rrdcontroller import RRDController
import os

if __name__ == '__main__':
	ipAddress = '192.168.11.129'
	serviceName = 'service_account'
	jvmType = 'JAVA_S0_S1_Eden_Metadata'
	rrdFile = '/data/apps/jvm_monitor/%s/%s/%s.rrd' % (ipAddress,serviceName,serviceName)
	staticFile = '/data/apps/jvm_monitor/%s/%s/%s.png' %(ipAddress,serviceName,jvmType)
	
	if os.path.exists(os.path.dirname(rrdFile)) is not True:
		print os.path.dirname(rrdFile)
		os.makedirs(os.path.dirname(rrdFile))
	if os.path.exists(os.path.dirname(staticFile)) is not True:
		print os.path.dirname(staticFile)
		os.makedirs(os.path.dirname(staticFile))

	if os.path.isfile(rrdFile) is not True:
		print rrdFile
		rrd = RRDController(rrdFile, staticFile)
		rrd.create()



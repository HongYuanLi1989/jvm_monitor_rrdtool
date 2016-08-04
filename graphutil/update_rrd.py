#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-03 16:54:31
# @Author  : LiHongyuan (hy.li@8win.com)

from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, CDEF, VDEF
from pyrrd.graph import LINE, AREA, GPRINT
from pyrrd.graph import ColorAttributes, Graph
import os
import logging
import time
class RRDController(object):

	def __init__(self, rrdfile, static_path):

		self.rrdfile = rrdfile
		self.static_path = static_path

	def create(self):
		if os.path.exists(self.rrdfile):
			self.rrd = RRD(self.rrdfile)
			return
		dss = []
		ds1 = DS(dsName="GCT_avg", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds2 = DS(dsName="Eden_ratio", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds3 = DS(dsName="S1_max", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds4 = DS(dsName="S1_ratio", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds5 = DS(dsName="Old_max", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds6 = DS(dsName="Heap_max", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds7 = DS(dsName="YGCT_avg", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds8 = DS(dsName="FGCT_avg", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds9 = DS(dsName="FGC", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds10 = DS(dsName="Metadata_used", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds11 = DS(dsName="Heap_used", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds12 = DS(dsName="Eden_max", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds13 = DS(dsName="Old_used", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds14 = DS(dsName="Eden_used", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds15 = DS(dsName="YGC", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds16 = DS(dsName="YGCT", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds17 = DS(dsName="S0_used", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds18 = DS(dsName="Metadata_max", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds19 = DS(dsName="FGCT", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds20 = DS(dsName="Old_ratio", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds21 = DS(dsName="Heap_ratio", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds22 = DS(dsName="S0_ratio", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds23 = DS(dsName="S1_used", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds24 = DS(dsName="Metadata_ratio", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds25 = DS(dsName="GCT", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)
		ds26 = DS(dsName="S0_max", dsType="GAUGE", heartbeat=120, minval=0, maxval=1000000000)


		dss.extend([ds1, ds2, ds3, ds4, ds5, ds6, ds7, ds8, ds9, ds10, ds11, ds12, ds13, ds14, ds15, ds16, ds17, ds18, ds19, ds20, ds21, ds22, ds23, ds24, ds25, ds26])

		rras = []
		rra1 = RRA(cf="AVERAGE", xff=0.5, steps=1, rows=2880)
		rra2 = RRA(cf="AVERAGE", xff=0.5, steps=30, rows=672)
		rra3 = RRA(cf="AVERAGE", xff=0.5, steps=120, rows=732)
		rra4 = RRA(cf="AVERAGE", xff=0.5, steps=720, rows=1460)

		rras.extend([rra1, rra2, rra3, rra4])

		self.rrd = RRD(self.rrdfile, step=60, ds=dss, rra=rras)
		self.rrd.create(debug=False)
		time.sleep(2)

	def update(self, GCT_avg, S1_max, S1_ratio, Old_max, Heap_max, YGCT_avg, FGCT_avg, FGC, Metadata_used, Heap_used, Eden_max, Old_used, Eden_used, YGC, YGCT, Eden_ratio, S0_used, Metadata_max, FGCT, Old_ratio, Heap_ratio, S0_ratio, S1_used, S0_max, Metadata_ratio, GCT):
		self.rrd.bufferValue("%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d" %(time.time(),GCT_avg, S1_max, S1_ratio, Old_max, Heap_max, YGCT_avg, FGCT_avg, FGC, Metadata_used, Heap_used, Eden_max, Old_used, Eden_used, YGC, YGCT, Eden_ratio, S0_used, Metadata_max, FGCT, Old_ratio, Heap_ratio, S0_ratio, S1_used, S0_max, Metadata_ratio, GCT))
		self.rrd.update(template="GCT_avg:S1_max:S1_ratio:Old_max:Heap_max:YGCT_avg:FGCT_avg:FGC:Metadata_used:Heap_used:Eden_max:Old_used:Eden_used:YGC:YGCT:Eden_ratio:S0_used:Metadata_max:FGCT:Old_ratio:Heap_ratio:S0_ratio:S1_used:S0_max:Metadata_ratio:GCT",debug=True)


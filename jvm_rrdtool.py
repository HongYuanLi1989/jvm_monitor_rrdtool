#!/usr/bin/env python
from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, CDEF, VDEF
from pyrrd.graph import LINE, AREA, GPRINT
from pyrrd.graph import ColorAttributes, Graph

import os, logging, time

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
		
	def graph_request(self, period='day'):
		pass

	def grap_heap_Memory(self, period='day'):
		def1=DEF(rrdfile=self.rrdfile, vname="Heap_used", dsName="Heap_used", cdef="AVERAGE")
		def2=DEF(rrdfile=self.rrdfile, vname="Heap_max", dsName="Heap_max" ,cdef="AVERAGE")
		def3=DEF(rrdfile=self.rrdfile, vname="Eden_used", dsName="Eden_used", cdef="AVERAGE")

		vdef1 = VDEF(vname="max", rpn='Heap_used,MAXIMUM')
		vdef2 = VDEF(vname="avg", rpn='Heap_used,AVERAGE')
		vdef3 = VDEF(vname="last", rpn='Heap_used,LAST')
		vdef4 = VDEF(vname="min", rpn='Heap_used,MINIMUM')

		line1 = LINE(1, defObj=def1, color='#22FF22', legend='Heap_Used')

		gprint1 = GPRINT(vdef1, "Max\\: %5.1lf %s")
		gprint2 = GPRINT(vdef2, "Avg\\: %5.1lf %s")
		gprint3 = GPRINT(vdef3, "Current\\: %5.1lf %s")
		gprint4 = GPRINT(vdef4, "Min\\: %5.1lf %s\\n")

		max_vdef1 = VDEF(vname="heap_max", rpn='Heap_max,MAXIMUM')
		max_vdef2 = VDEF(vname="heap_avg", rpn='Heap_max,AVERAGE')
		max_vdef3 = VDEF(vname="heap_last", rpn='Heap_max,LAST')
		max_vdef4 = VDEF(vname="heap_min", rpn='Heap_max,MINIMUM')


		line2 = LINE(1, defObj=def2, color='#0022FF', legend='Heap_max')

		max_gprint1 = GPRINT(max_vdef1, "Max\\: %5.1lf %s")
		max_gprint2 = GPRINT(max_vdef2, "Avg\\: %5.1lf %s")
		max_gprint3 = GPRINT(max_vdef3, "Current\\: %5.1lf %s")
		max_gprint4 = GPRINT(max_vdef4, "Min\\: %5.1lf %s\\n")

		eden_used_vdef1 = VDEF(vname="eden_used_max", rpn='Eden_used,MAXIMUM')
		eden_used_vdef2 = VDEF(vname="eden_used_avg", rpn='Eden_used,AVERAGE')
		eden_used_vdef3 = VDEF(vname="eden_used_last", rpn='Eden_used,LAST')
		eden_used_vdef4 = VDEF(vname="eden_used_min", rpn='Eden_used,MINIMUM')


		line3 = LINE(1, defObj=def3, color='#CC22FF', legend='Eden_used')

		eden_used_gprint1 = GPRINT(eden_used_vdef1, "Max\\: %5.1lf %s")
		eden_used_gprint2 = GPRINT(eden_used_vdef2, "Avg\\: %5.1lf %s")
		eden_used_gprint3 = GPRINT(eden_used_vdef3, "Current\\: %5.1lf %s")
		eden_used_gprint4 = GPRINT(eden_used_vdef4, "Min\\: %5.1lf %s\\n")


		ca = ColorAttributes()
		ca.back = '#333333'
		ca.canvas = '#333333'
		ca.shadea = '#000000'
		ca.shadeb = '#111111'
		ca.mgrid = '#CCCCCC'
		ca.axis = '#FFFFFF'
		ca.frame = '#AAAAAA'
		ca.font = '#FFFFFF'
		ca.arrow = '#FFFFFF'

		img = "heap_used_%s.png" % period
		imgname = self.static_path + "/" + img
		start = '-1'+period

		#g = Graph(imgname, imgformat='PNG', step=start, vertical_label='KB', color=ca, width=700, height=350)
		g = Graph(imgname, imgformat='PNG', step=start, vertical_label='Units_KB', color=ca, width=700, height=400, units_exponent=6, base=1024, title="JVM_HEAP_USED")
		g.data.extend([def1, vdef1, vdef2, vdef3, vdef4, line1, gprint1, gprint2, gprint3, gprint4])
		g.data.extend([def2, max_vdef1, max_vdef2, max_vdef3, max_vdef4, line2, max_gprint1, max_gprint2, max_gprint3, max_gprint4])
		g.data.extend([def3, eden_used_vdef1, eden_used_vdef2, eden_used_vdef3, eden_used_vdef4, line3, eden_used_gprint1, eden_used_gprint2, eden_used_gprint3, eden_used_gprint4])

		g.write()

	def graph(self, period='day'):
		self.grap_heap_Memory(period)






	  
	  
	  
	  
	  
	  
	  
	  
	  
	  
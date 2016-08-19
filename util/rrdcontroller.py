#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-04 15:41:32
# @Author  : LiHongyuan (hy.li@8win.com)

import rrdtool
import os
import time

cur_time = str(int(time.time()))

class RRDController(object):

	def __init__(self, rrdfile, static_path):
		self.rrdfile = rrdfile
		self.static_path = static_path
		#print type(self.rrdfile),type(self.static_path)
		#print self.rrdfile,self.static_path

	def create(self):
		if os.path.isfile(self.rrdfile) is not True:
			print self.rrdfile
			self.rrd = rrdtool.create(self.rrdfile, '--step', '30', '--start',cur_time, 'DS:GCT_avg:GAUGE:120:0:U','DS:Eden_ratio:GAUGE:120:0:U','DS:S1_max:GAUGE:120:0:U','DS:S1_ratio:GAUGE:120:0:U',	'DS:Old_max:GAUGE:120:0:U',	'DS:Heap_max:GAUGE:120:0:U','DS:YGCT_avg:GAUGE:120:0:U','DS:FGCT_avg:GAUGE:120:0:U','DS:FGC:GAUGE:120:0:U',	'DS:Metadata_used:GAUGE:120:0:U','DS:Heap_used:GAUGE:120:0:U','DS:Eden_max:GAUGE:120:0:U','DS:Old_used:GAUGE:120:0:U','DS:Eden_used:GAUGE:120:0:U',	'DS:YGC:GAUGE:120:0:U',	'DS:YGCT:GAUGE:120:0:U','DS:S0_used:GAUGE:120:0:U',	'DS:Metadata_max:GAUGE:120:0:U','DS:FGCT:GAUGE:120:0:U','DS:Old_ratio:GAUGE:120:0:U','DS:Heap_ratio:GAUGE:120:0:U',	'DS:S0_ratio:GAUGE:120:0:U','DS:S1_used:GAUGE:120:0:U',	'DS:Metadata_ratio:GAUGE:120:0:U','DS:GCT:GAUGE:120:0:U','DS:S0_max:GAUGE:120:0:U',	'RRA:AVERAGE:0.5:1:2880','RRA:AVERAGE:0.5:30:672','RRA:AVERAGE:0.5:120:732','RRA:AVERAGE:0.5:720:1460',	'RRA:MIN:0.5:1:2880','RRA:MIN:0.5:30:672','RRA:MIN:0.5:120:732','RRA:MIN:0.5:720:1460',	'RRA:MAX:0.5:1:2880','RRA:MAX:0.5:30:672','RRA:MAX:0.5:120:732','RRA:MAX:0.5:720:1460')

			if self.rrd:
				print rrdtool.error()
		else:
			print "create success!"
		return self.rrd

	def update(self,rrdfile, GCT_avg, S1_max, S1_ratio, Old_max, Heap_max, YGCT_avg, FGCT_avg, FGC, Metadata_used, 
		Heap_used, Eden_max, Old_used, Eden_used, YGC, YGCT, Eden_ratio, S0_used, Metadata_max, FGCT, Old_ratio, 
		Heap_ratio, S0_ratio, S1_used, S0_max, Metadata_ratio, GCT):
        #rrdtool update pf_stats_db.rrd --template BytesIn:BytesOut:PktsInPass:PktsInBlock:PktsOutPass:PktsOutBlock:States:StateSearchs:StateInserts:StateRemovals N:$RETURN_VALUE
		self.update = rrdtool.updatev(self.rrdfile, '--template', 'GCT_avg:S1_max:S1_ratio:Old_max:Heap_max:YGCT_avg:FGCT_avg:FGC:Metadata_used:Heap_used:Eden_max:Old_used:Eden_used:YGC:YGCT:Eden_ratio:S0_used:Metadata_max:FGCT:Old_ratio:Heap_ratio:S0_ratio:S1_used:S0_max:Metadata_ratio:GCT', '%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d' 
			% (time.time(),GCT_avg, S1_max, S1_ratio, Old_max, Heap_max, YGCT_avg, 
			FGCT_avg, FGC, Metadata_used, Heap_used, Eden_max, Old_used, Eden_used, YGC, YGCT, Eden_ratio, S0_used, Metadata_max, FGCT, 
			Old_ratio, Heap_ratio, S0_ratio, S1_used, S0_max, Metadata_ratio, GCT))
		print GCT_avg, S1_max, S1_ratio, Old_max, Heap_max, YGCT_avg, FGCT_avg, FGC, Metadata_used, Heap_used, Eden_max, Old_used, Eden_used, YGC, YGCT, Eden_ratio, S0_used, Metadata_max, FGCT, Old_ratio, Heap_ratio, S0_ratio, S1_used, S0_max, Metadata_ratio, GCT
		return self.update

	def graphJavaS0S1EdenOldMax(self):
		rrdtool.graph(self.static_path,'--start','-1d',"--vertical-label=Bytes",
		"--x-grid","MINUTE:10:HOUR:1:MINUTE:120:0:%R", "--no-gridfit","--slope-mode",
		"--width","785 ","--height","230","--title","Java S0_S1_Eden_Old Max",
		"--color", "ARROW#FFFFFF", "--color", "AXIS#FFFFFF", "--color", "BACK#333333",
		"--color", "CANVAS#333333", "--color", "FONT#FFFFFF", "--color", "FRAME#AAAAAA", 
		"--color", "MGRID#CCCCCC", "--color", "SHADEA#000000", "--color", "SHADEB#111111",
		"DEF:S0_max="+self.rrdfile+":S0_max:AVERAGE",
		"DEF:S1_max="+self.rrdfile+":S1_max:AVERAGE",
		"DEF:Eden_max="+self.rrdfile+":Eden_max:AVERAGE",
		"DEF:Old_max="+self.rrdfile+":Old_max:AVERAGE",
		"LINE1:S0_max#0E0BEE:S0_MAX",
		"GPRINT:S0_max:MAX:Max\: %5.1lf %S",
		"GPRINT:S0_max:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:S0_max:LAST:Current\: %5.1lf %S",
		"GPRINT:S0_max:MIN:Min\: %5.1lf %S\\n",

		"LINE1:S1_max#00FF00:S1_MAX",
		"GPRINT:S1_max:MAX:Max\: %5.1lf %S",
		"GPRINT:S1_max:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:S1_max:LAST:Current\: %5.1lf %S",
		"GPRINT:S1_max:MIN:Min\: %5.1lf %S\\n",

		"LINE1:Eden_max#FF0000:Eden_max",
		"GPRINT:Eden_max:MAX:Max\: %5.1lf %S",
		"GPRINT:Eden_max:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:Eden_max:LAST:Current\: %5.1lf %S",
		"GPRINT:Eden_max:MIN:Min\: %5.1lf %S\\n",

		"LINE1:Old_max#FF8833:Old_max",
		"GPRINT:Old_max:MAX:Max\: %5.1lf %S",
		"GPRINT:Old_max:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:Old_max:LAST:Current\: %5.1lf %S",
		"GPRINT:Old_max:MIN:Min\: %5.1lf %S\\n"
		)

		#YGCT_avg,FGCT_avg,GCT_avg
	def graphJavaAverageGCTime(self):
		rrdtool.graph(self.static_path,'--start','-1d',"--vertical-label=Unit second",
		"--x-grid","MINUTE:10:HOUR:1:MINUTE:120:0:%R", "--no-gridfit","--slope-mode",
		"--width","785 ","--height","230","--title","Java Average GC Time",
		"--color", "ARROW#FFFFFF", "--color", "AXIS#FFFFFF", "--color", "BACK#333333",
		"--color", "CANVAS#333333", "--color", "FONT#FFFFFF", "--color", "FRAME#AAAAAA", 
		"--color", "MGRID#CCCCCC", "--color", "SHADEA#000000", "--color", "SHADEB#111111",
		"DEF:YGCT_avg="+self.rrdfile+":YGCT_avg:AVERAGE",
		"DEF:FGCT_avg="+self.rrdfile+":FGCT_avg:AVERAGE",
		"DEF:GCT_avg="+self.rrdfile+":GCT_avg:AVERAGE",
		"LINE1:YGCT_avg#0E0BEE:YGCT_avg",
		"GPRINT:YGCT_avg:MAX:Max\: %5.1lf %S",
		"GPRINT:YGCT_avg:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:YGCT_avg:LAST:Current\: %5.1lf %S",
		"GPRINT:YGCT_avg:MIN:Min\: %5.1lf %S\\n",

		"LINE1:FGCT_avg#00FF00:FGCT_avg",
		"GPRINT:FGCT_avg:MAX:Max\: %5.1lf %S",
		"GPRINT:FGCT_avg:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:FGCT_avg:LAST:Current\: %5.1lf %S",
		"GPRINT:FGCT_avg:MIN:Min\: %5.1lf %S\\n",

		"LINE1:GCT_avg#FF0000:GCT_avg",
		"GPRINT:GCT_avg:MAX:Max\: %5.1lf %S",
		"GPRINT:GCT_avg:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:GCT_avg:LAST:Current\: %5.1lf %S",
		"GPRINT:GCT_avg:MIN:Min\: %5.1lf %S\\n"
		)

	#Old_ratio, S1_ratio, S0_ratio, Eden_ratio
	def graphJavaS0S1EdenOldUsedPercentage(self):
		rrdtool.graph(self.static_path,'--start','-1d',"--vertical-label=Percentage",
		"--x-grid","MINUTE:10:HOUR:1:MINUTE:120:0:%R", "--no-gridfit","--slope-mode",
		"--width","785 ","--height","230","--title","Java S0_S1_Eden_Old Used Percentage",
		"--color", "ARROW#FFFFFF", "--color", "AXIS#FFFFFF", "--color", "BACK#333333",
		"--color", "CANVAS#333333", "--color", "FONT#FFFFFF", "--color", "FRAME#AAAAAA", 
		"--color", "MGRID#CCCCCC", "--color", "SHADEA#000000", "--color", "SHADEB#111111",
		"DEF:Old_ratio="+self.rrdfile+":Old_ratio:AVERAGE",
		"DEF:S1_ratio="+self.rrdfile+":S1_ratio:AVERAGE",
		"DEF:S0_ratio="+self.rrdfile+":S0_ratio:AVERAGE",
		"DEF:Eden_ratio="+self.rrdfile+":Eden_ratio:AVERAGE",
		"LINE1:Old_ratio#0E0BEE:Old_ratio",
		"GPRINT:Old_ratio:MAX:Max\: %5.1lf %S",
		"GPRINT:Old_ratio:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:Old_ratio:LAST:Current\: %5.1lf %S",
		"GPRINT:Old_ratio:MIN:Min\: %5.1lf %S\\n",

		"LINE1:S1_ratio#00FF00:S1_ratio",
		"GPRINT:S1_ratio:MAX:Max\: %5.1lf %S",
		"GPRINT:S1_ratio:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:S1_ratio:LAST:Current\: %5.1lf %S",
		"GPRINT:S1_ratio:MIN:Min\: %5.1lf %S\\n",

		"LINE1:S0_ratio#FF0000:S0_ratio",
		"GPRINT:S0_ratio:MAX:Max\: %5.1lf %S",
		"GPRINT:S0_ratio:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:S0_ratio:LAST:Current\: %5.1lf %S",
		"GPRINT:S0_ratio:MIN:Min\: %5.1lf %S\\n",

		"LINE1:Eden_ratio#FF8833:Eden_ratio",
		"GPRINT:Eden_ratio:MAX:Max\: %5.1lf %S",
		"GPRINT:Eden_ratio:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:Eden_ratio:LAST:Current\: %5.1lf %S",
		"GPRINT:Eden_ratio:MIN:Min\: %5.1lf %S\\n"
		)
	#YGC, FGC
	def graphJavaGCEvents(self):
		rrdtool.graph(self.static_path,'--start','-1d',"--vertical-label=Times",
		"--x-grid","MINUTE:10:HOUR:1:MINUTE:120:0:%R","--no-gridfit","--slope-mode",
		"--width","785 ","--height","230","--title","Java GC Events",
		"--color", "ARROW#FFFFFF", "--color", "AXIS#FFFFFF", "--color", "BACK#333333",
		"--color", "CANVAS#333333", "--color", "FONT#FFFFFF", "--color", "FRAME#AAAAAA", 
		"--color", "MGRID#CCCCCC", "--color", "SHADEA#000000", "--color", "SHADEB#111111",
		"DEF:YGC="+self.rrdfile+":YGC:AVERAGE",
		"DEF:FGC="+self.rrdfile+":FGC:AVERAGE",
		"LINE1:YGC#0E0BEE:YGC",
		"GPRINT:YGC:MAX:Max\: %5.1lf %S",
		"GPRINT:YGC:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:YGC:LAST:Current\: %5.1lf %S",
		"GPRINT:YGC:MIN:Min\: %5.1lf %S\\n",

		"LINE1:FGC#00FF00:FGC",
		"GPRINT:FGC:MAX:Max\: %5.1lf %S",
		"GPRINT:FGC:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:FGC:LAST:Current\: %5.1lf %S",
		"GPRINT:FGC:MIN:Min\: %5.1lf %S\\n"
		)

		#YGCT,FGCT,CGT
	def graphJavaAverageGCTime(self):
		rrdtool.graph(self.static_path,'--start','-1d',"--vertical-label=Unit second",
		"--x-grid","MINUTE:10:HOUR:1:MINUTE:120:0:%R","--no-gridfit","--slope-mode",
		"--width","785 ","--height","230","--title","Java Average GC Time",
		"--color", "ARROW#FFFFFF", "--color", "AXIS#FFFFFF", "--color", "BACK#333333",
		"--color", "CANVAS#333333", "--color", "FONT#FFFFFF", "--color", "FRAME#AAAAAA", 
		"--color", "MGRID#CCCCCC", "--color", "SHADEA#000000", "--color", "SHADEB#111111",
		"DEF:YGCT="+self.rrdfile+":YGCT:AVERAGE",
		"DEF:FGCT="+self.rrdfile+":FGCT:AVERAGE",
		"DEF:GCT="+self.rrdfile+":GCT:AVERAGE",
		"LINE1:YGCT#0E0BEE:YGCT",
		"GPRINT:YGCT:MAX:Max\: %5.1lf %S",
		"GPRINT:YGCT:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:YGCT:LAST:Current\: %5.1lf %S",
		"GPRINT:YGCT:MIN:Min\: %5.1lf %S\\n",

		"LINE1:FGCT#00FF00:FGCT",
		"GPRINT:FGCT:MAX:Max\: %5.1lf %S",
		"GPRINT:FGCT:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:FGCT:LAST:Current\: %5.1lf %S",
		"GPRINT:FGCT:MIN:Min\: %5.1lf %S\\n",

		"LINE1:GCT#FF0000:GCT",
		"GPRINT:GCT:MAX:Max\: %5.1lf %S",
		"GPRINT:GCT:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:GCT:LAST:Current\: %5.1lf %S",
		"GPRINT:GCT:MIN:Min\: %5.1lf %S\\n"
		)
		#Heap_used,Heap_max,Heap_ratio
	def graphJavaHeapMemory(self):
		rrdtool.graph(self.static_path,'--start','-1d',"--vertical-label=MBytes",
		"--x-grid","MINUTE:10:HOUR:1:MINUTE:120:0:%R", "--no-gridfit","--slope-mode",
		"--width","785 ","--height","230","--title","Java Heap Memory",
        "--right-axis-label", "Heap ratio",
		"--right-axis", "1:0 ", 
		"--color", "ARROW#FFFFFF", "--color", "AXIS#FFFFFF", "--color", "BACK#333333",
		"--color", "CANVAS#333333", "--color", "FONT#FFFFFF", "--color", "FRAME#AAAAAA", 
		"--color", "MGRID#CCCCCC", "--color", "SHADEA#000000", "--color", "SHADEB#111111",
		"--right-axis-format", "%1.0lf",
		"DEF:Heap_used="+self.rrdfile+":Heap_used:AVERAGE",
		"DEF:Heap_max="+self.rrdfile+":Heap_max:AVERAGE",
		"DEF:Heap_ratio="+self.rrdfile+":Heap_ratio:AVERAGE",
		"CDEF:Heap_used_calc=Heap_used,1000000,/",
		"CDEF:Heap_max_calc=Heap_max,1000000,/",
		"CDEF:Heap_ratio_calc=Heap_ratio,1,*",

		"AREA:Heap_used_calc#0E0BEE:Heap_used",
		"GPRINT:Heap_used:MAX:Max\: %5.1lf %S",
		"GPRINT:Heap_used:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:Heap_used:LAST:Current\: %5.1lf %S",
		"GPRINT:Heap_used:MIN:Min\: %5.1lf %S\\n",

		"LINE1:Heap_max_calc#00FF00:Heap_max",
		"GPRINT:Heap_max:MAX:Max\: %5.1lf %S",
		"GPRINT:Heap_max:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:Heap_max:LAST:Current\: %5.1lf %S",
		"GPRINT:Heap_max:MIN:Min\: %5.1lf %S\\n",

		"LINE1:Heap_ratio_calc#FF0000:Heap_ratio",
		"GPRINT:Heap_ratio:MAX:Max\: %1.1lf",
		"GPRINT:Heap_ratio:AVERAGE:Avg\: %1.1lf",
		"GPRINT:Heap_ratio:LAST:Current\: %1.1lf",
		"GPRINT:Heap_ratio:MIN:Min\: %1.1lf\\n"
		)

			#Metadata_used,Metadata_max,Metadata_ratio
	def graphJavaMetadataMemory(self):
		rrdtool.graph(self.static_path,'--start','-1d',"--vertical-label=MBytes",
		"--x-grid","MINUTE:10:HOUR:1:MINUTE:120:0:%R","--no-gridfit","--slope-mode",
		"--width","785 ","--height","230","--title","Java Metadata Memory",
		"--right-axis-label", "Metadata ratio",
		"--right-axis", "1:0 ", 
		"--color", "ARROW#FFFFFF", "--color", "AXIS#FFFFFF", "--color", "BACK#333333",
		"--color", "CANVAS#333333", "--color", "FONT#FFFFFF", "--color", "FRAME#AAAAAA", 
		"--color", "MGRID#CCCCCC", "--color", "SHADEA#000000", "--color", "SHADEB#111111",
		"--right-axis-format", "%1.0lf",
		"DEF:Metadata_used="+self.rrdfile+":Metadata_used:AVERAGE",
		"DEF:Metadata_max="+self.rrdfile+":Metadata_max:AVERAGE",
		"DEF:Metadata_ratio="+self.rrdfile+":Metadata_ratio:AVERAGE",
		"CDEF:Metadata_used_calc=Metadata_used,1000000,/",
		"CDEF:Metadata_max_calc=Metadata_max,1000000,/",
		"CDEF:Metadata_ratio_calc=Metadata_ratio,1,*",

		"AREA:Metadata_used_calc#0E0BEE:Metadata_used",
		"GPRINT:Metadata_used:MAX:Max\: %5.1lf %S",
		"GPRINT:Metadata_used:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:Metadata_used:LAST:Current\: %5.1lf %S",
		"GPRINT:Metadata_used:MIN:Min\: %5.1lf %S\\n",

		"LINE1:Metadata_max_calc#00FF00:Metadata_max",
		"GPRINT:Metadata_max:MAX:Max\: %5.1lf %S",
		"GPRINT:Metadata_max:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:Metadata_max:LAST:Current\: %5.1lf %S",
		"GPRINT:Metadata_max:MIN:Min\: %5.1lf %S\\n",

		"LINE1:Metadata_ratio_calc#FF0000:Metadata_ratio",
		"GPRINT:Metadata_ratio:MAX:Max\: %1.1lf",
		"GPRINT:Metadata_ratio:AVERAGE:Avg\: %1.1lf",
		"GPRINT:Metadata_ratio:LAST:Current\: %1.1lf",
		"GPRINT:Metadata_ratio:MIN:Min\: %1.1lf\\n"
		)
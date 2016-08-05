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

		print self.rrdfile,self.static_path

	def create(self):
		if os.path.isfile(self.rrdfile) is not True:

			self.rrd = rrdtool.create(self.rrdfile, '--step', '30', '--start',cur_time, 
				'DS:GCT_avg:GAUGE:120:0:U',
				'DS:Eden_ratio:GAUGE:120:0:U',
				'DS:S1_max:GAUGE:120:0:U',
				'DS:S1_ratio:GAUGE:120:0:U',
				'DS:Old_max:GAUGE:120:0:U',
				'DS:Heap_max:GAUGE:120:0:U',
				'DS:YGCT_avg:GAUGE:120:0:U',
				'DS:FGCT_avg:GAUGE:120:0:U',
				'DS:FGC:GAUGE:120:0:U',
				'DS:Metadata_used:GAUGE:120:0:U',
				'DS:Heap_used:GAUGE:120:0:U',
				'DS:Eden_max:GAUGE:120:0:U',
				'DS:Old_used:GAUGE:120:0:U',
				'DS:Eden_used:GAUGE:120:0:U',
				'DS:YGC:GAUGE:120:0:U',
				'DS:YGCT:GAUGE:120:0:U',
				'DS:S0_used:GAUGE:120:0:U',
				'DS:Metadata_max:GAUGE:120:0:U',
				'DS:FGCT:GAUGE:120:0:U',
				'DS:Old_ratio:GAUGE:120:0:U',
				'DS:Heap_ratio:GAUGE:120:0:U',
				'DS:S0_ratio:GAUGE:120:0:U',
				'DS:S1_used:GAUGE:120:0:U',
				'DS:Metadata_ratio:GAUGE:120:0:U',
				'DS:GCT:GAUGE:120:0:U', 
				'DS:S0_max:GAUGE:120:0:U',
				'RRA:AVERAGE:0.5:1:2880',
				'RRA:AVERAGE:0.5:30:672',
				'RRA:AVERAGE:0.5:120:732',
				'RRA:AVERAGE:0.5:720:1460',
				'RRA:MIN:0.5:1:2880',
				'RRA:MIN:0.5:30:672',
				'RRA:MIN:0.5:120:732',
				'RRA:MIN:0.5:720:1460',
				'RRA:MAX:0.5:1:2880',
				'RRA:MAX:0.5:30:672',
				'RRA:MAX:0.5:120:732',
				'RRA:MAX:0.5:720:1460')
			if self.rrd:
				print rrdtool.error()
		else:
			print "create success!"
		return self.rrd

	def update(self,rrdfile, GCT_avg, S1_max, S1_ratio, Old_max, Heap_max, YGCT_avg, FGCT_avg, FGC, Metadata_used, 
		Heap_used, Eden_max, Old_used, Eden_used, YGC, YGCT, Eden_ratio, S0_used, Metadata_max, FGCT, Old_ratio, 
		Heap_ratio, S0_ratio, S1_used, S0_max, Metadata_ratio, GCT):

		self.update = rrdtool.updatev(self.rrdfile, '%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d:%d' 
			% (time.time(),GCT_avg, S1_max, S1_ratio, Old_max, Heap_max, YGCT_avg, 
			FGCT_avg, FGC, Metadata_used, Heap_used, Eden_max, Old_used, Eden_used, YGC, YGCT, Eden_ratio, S0_used, Metadata_max, FGCT, 
			Old_ratio, Heap_ratio, S0_ratio, S1_used, S0_max, Metadata_ratio, GCT))
		return self.update

	def graphJavaS0S1EdenMetadata(self):
		rrdtool.graph(self.static_path,'--start','-1d',"--vertical-label=Bytes",
		"--x-grid","MINUTE:12:HOUR:1:HOUR:1:0:%H",
		"--width","650","--height","230","--title","test---test",
		"DEF:S0_max="+self.rrdfile+":S0_max:AVERAGE",
		"DEF:S1_max="+self.rrdfile+":S1_max:AVERAGE",
		"DEF:Eden_max="+self.rrdfile+":Eden_max:AVERAGE",
		"DEF:Metadata_max="+self.rrdfile+":Metadata_max:AVERAGE",
		"LINE1:S0_max#0E0BEE:SO_MAX",
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

		"LINE1:Metadata_max#FF8833:Metadata",
		"GPRINT:Metadata_max:MAX:Max\: %5.1lf %S",
		"GPRINT:Metadata_max:AVERAGE:Avg\: %5.1lf %S",
		"GPRINT:Metadata_max:LAST:Current\: %5.1lf %S",
		"GPRINT:Metadata_max:MIN:Min\: %5.1lf %S\\n"
		)
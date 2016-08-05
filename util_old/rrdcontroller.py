#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-04 15:41:32
# @Author  : LiHongyuan (hy.li@8win.com)

import rrdtool
import os
import time

data_source = "DS:GCT_avg:GAUGE:120:0:1000000000","DS:Eden_ratio:GAUGE:120:0:1000000000","DS:S1_max:GAUGE:120:0:1000000000","DS:S1_ratio:GAUGE:120:0:1000000000","DS:Old_max:GAUGE:120:0:1000000000","DS:Heap_max:GAUGE:120:0:1000000000","DS:YGCT_avg:GAUGE:120:0:1000000000","DS:FGCT_avg:GAUGE:120:0:1000000000","DS:FGC:GAUGE:120:0:1000000000","DS:Metadata_used:GAUGE:120:0:1000000000","DS:Heap_used:GAUGE:120:0:1000000000","DS:Eden_max:GAUGE:120:0:1000000000","DS:Old_used:GAUGE:120:0:1000000000","DS:Eden_used:GAUGE:120:0:1000000000","DS:YGC:GAUGE:120:0:1000000000","DS:YGCT:GAUGE:120:0:1000000000","DS:S0_used:GAUGE:120:0:1000000000","DS:Metadata_max:GAUGE:120:0:1000000000","DS:FGCT:GAUGE:120:0:1000000000","DS:Old_ratio:GAUGE:120:0:1000000000","DS:Heap_ratio:GAUGE:120:0:1000000000","DS:S0_ratio:GAUGE:120:0:1000000000","DS:S1_used:GAUGE:120:0:1000000000","DS:Metadata_ratio:GAUGE:120:0:1000000000","DS:GCT:GAUGE:120:0:1000000000", "DS:S0_max:GAUGE:120:0:1000000000"
rra_source = "RRA:AVERAGE:0.5:1:2880","RRA:AVERAGE:0.5:30:672","RRA:AVERAGE:0.5:120:732","RRA:AVERAGE:0.5:720:1460" 
cur_time = str(int(time.time()))

class RRDController(object):

	def __init__(self, rrdfile, static_path):
		self.rrdfile = rrdfile
		self.static_path = static_path

	def create(self):
		if os.path.exists(self.rrdfile) is True: 
			rrd = rrdtool.create('/data/apps/jvm_monitor/192.168.11.129/service_account/service_account.rrd', '--step', '30', '--start',cur_time, 'DS:GCT_avg:GAUGE:120:0:U',
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

#"RRA:AVERAGE:0.5:1:2880", "RRA:AVERAGE:0.5:30:672", "RRA:AVERAGE:0.5:120:732","RRA:AVERAGE:0.5:720:1460" 
#"DS:GCT_avg:GAUGE:120:0:1000000000","DS:Eden_ratio:GAUGE:120:0:1000000000", "DS:S1_max:GAUGE:120:0:1000000000","DS:S1_ratio:GAUGE:120:0:1000000000", "DS:Old_max:GAUGE:120:0:1000000000","DS:Heap_max:GAUGE:120:0:1000000000", "DS:YGCT_avg:GAUGE:120:0:1000000000","DS:FGCT_avg:GAUGE:120:0:1000000000", "DS:FGC:GAUGE:120:0:1000000000","DS:Metadata_used:GAUGE:120:0:1000000000", "DS:Heap_used:GAUGE:120:0:1000000000","DS:Eden_max:GAUGE:120:0:1000000000", "DS:Old_used:GAUGE:120:0:1000000000","DS:Eden_used:GAUGE:120:0:1000000000", "DS:YGC:GAUGE:120:0:1000000000","DS:YGCT:GAUGE:120:0:1000000000", "DS:S0_used:GAUGE:120:0:1000000000","DS:Metadata_max:GAUGE:120:0:1000000000", "DS:FGCT:GAUGE:120:0:1000000000","DS:Old_ratio:GAUGE:120:0:1000000000", "DS:Heap_ratio:GAUGE:120:0:1000000000","DS:S0_ratio:GAUGE:120:0:1000000000", "DS:S1_used:GAUGE:120:0:1000000000","DS:Metadata_ratio:GAUGE:120:0:1000000000", "DS:GCT:GAUGE:120:0:1000000000","DS:S0_max:GAUGE:120:0:1000000000


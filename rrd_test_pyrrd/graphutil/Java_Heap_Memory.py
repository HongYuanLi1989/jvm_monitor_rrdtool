#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-03 17:13:10
# @Author  : LiHongyuan (hy.li@8win.com)

from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, CDEF, VDEF
from pyrrd.graph import LINE, AREA, GPRINT
from pyrrd.graph import ColorAttributes, Graph
from update_rrd import RRDController
import os

def create_java_heap_memory(filename):

	rrdfile = '/data/apps/jvm_monitor/rrd/java_heap_memory/%s.rrd' %filename
	imgdir = '/data/apps/jvm_monitor/img/java_heap_img/%s.png' %filename

	rrd = RRDController(rrdfile=rrdfile, static_path=imgdir)

	rrd.create()

	if os.path.isfile(rrdfile) is True:
		print "Create rrd file Successed!"
	else:
		exit

def graph(period='day'):
	def1=DEF(rrdfile=self.rrdfile, vname="Heap_used", dsName="Heap_used", cdef="AVERAGE")
	def2=DEF(rrdfile=self.rrdfile, vname="Heap_max", dsName="Heap_max" ,cdef="AVERAGE")
	def3=DEF(rrdfile=self.rrdfile, vname="Heap_ratio", dsName="Heap_ratio", cdef="AVERAGE")

	vdef1 = VDEF(vname="max", rpn='Heap_used,MAXIMUM')
	vdef2 = VDEF(vname="avg", rpn='Heap_used,AVERAGE')
	vdef3 = VDEF(vname="last", rpn='Heap_used,LAST')
	vdef4 = VDEF(vname="min", rpn='Heap_used,MINIMUM')

	area1 = AREA(defObj=def1, color='#22FF22', legend='Heap_Used')

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

	imgname = imgdir
	start = '-1'+period

	#g = Graph(imgname, imgformat='PNG', step=start, vertical_label='KB', color=ca, width=700, height=350)
	g = Graph(imgname, imgformat='PNG', step=start, vertical_label='Units_KB', color=ca, width=700, height=400, units_exponent=6, base=1024, title=filename)
	g.data.extend([def1, vdef1, vdef2, vdef3, vdef4, area1, gprint1, gprint2, gprint3, gprint4])
	g.data.extend([def2, max_vdef1, max_vdef2, max_vdef3, max_vdef4, line2, max_gprint1, max_gprint2, max_gprint3, max_gprint4])
	g.write()


if __name__ == '__main__':
	create_java_heap_memory(filename='service_account')
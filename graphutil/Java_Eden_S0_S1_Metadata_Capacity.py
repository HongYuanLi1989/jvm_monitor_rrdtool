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

#rrdfile = '/data/apps/jvm_monitor/rrd/java_heap_memory/%s.rrd' % os.path.basename(__file__).split('.')[0]
rrdfile = '/data/heap_memory.rrd'
imgdir = '/data/apps/jvm_monitor/img/java_heap_img/%s.png' % os.path.basename(__file__).split('.')[0]
title = '/data/apps/jvm_monitor/img/java_heap_img/%s.png' % os.path.basename(__file__).split('.')[0]
def create_java_heap_memory():

	rrd = RRDController(rrdfile=rrdfile, static_path=imgdir)

	rrd.create()

	if os.path.isfile(rrdfile) is True:
		print "Create rrd file Successed!"
	else:
		exit

def graph(period='day'):

	def1=DEF(rrdfile=rrdfile, vname="S0_max", dsName="S0_max", cdef="AVERAGE")
	def2=DEF(rrdfile=rrdfile, vname="S1_max", dsName="S1_max" ,cdef="AVERAGE")
	def3=DEF(rrdfile=rrdfile, vname="Eden_max", dsName="Eden_max", cdef="AVERAGE")
	def4=DEF(rrdfile=rrdfile, vname="Metadata_max", dsName="Metadata_max", cdef="AVERAGE")
	

	vdef1 = VDEF(vname="s0_max", rpn='S0_max,MAXIMUM')
	vdef2 = VDEF(vname="s0_avg", rpn='S0_max,AVERAGE')
	vdef3 = VDEF(vname="s0_last", rpn='S0_max,LAST')
	vdef4 = VDEF(vname="s0_min", rpn='S0_max,MINIMUM')

	gprint1 = GPRINT(vdef1, "Max\\: %5.1lf %s")
	gprint2 = GPRINT(vdef2, "Avg\\: %5.1lf %s")
	gprint3 = GPRINT(vdef3, "Current\\: %5.1lf %s")
	gprint4 = GPRINT(vdef4, "Min\\: %5.1lf %s\\n")

	line1 = LINE(1,defObj=def1, color='#22FF22', legend='S0_max')

	s1_vdef1 = VDEF(vname="s1_max", rpn='S1_max,MAXIMUM')
	s1_vdef2 = VDEF(vname="s1_avg", rpn='S1_max,AVERAGE')
	s1_vdef3 = VDEF(vname="s1_last", rpn='S1_max,LAST')
	s1_vdef4 = VDEF(vname="s1_min", rpn='S1_max,MINIMUM')

	s1_gprint1 = GPRINT(s1_vdef1, "Max\\: %5.1lf %s")
	s1_gprint2 = GPRINT(s1_vdef2, "Avg\\: %5.1lf %s")
	s1_gprint3 = GPRINT(s1_vdef3, "Current\\: %5.1lf %s")
	s1_gprint4 = GPRINT(s1_vdef4, "Min\\: %5.1lf %s\\n")

	line2 = LINE(1, defObj=def2, color='#B3442C', legend='S1_max')

	eden_vdef1 = VDEF(vname="eden_max", rpn='Eden_max,MAXIMUM')
	eden_vdef2 = VDEF(vname="eden_avg", rpn='Eden_max,AVERAGE')
	eden_vdef3 = VDEF(vname="eden_last", rpn='Eden_max,LAST')
	eden_vdef4 = VDEF(vname="eden_min", rpn='Eden_max,MINIMUM')

	eden_gprint1 = GPRINT(eden_vdef1, "Max\\: %5.1lf %s")
	eden_gprint2 = GPRINT(eden_vdef2, "Avg\\: %5.1lf %s")
	eden_gprint3 = GPRINT(eden_vdef3, "Current\\: %5.1lf %s")
	eden_gprint4 = GPRINT(eden_vdef4, "Min\\: %5.1lf %s\\n")

	line3 = LINE(1,defObj=def3, color='#189918', legend='Eden_max')


	metadata_vdef1 = VDEF(vname="metadata_max", rpn='Metadata_max,MAXIMUM')
	metadata_vdef2 = VDEF(vname="metadata_avg", rpn='Metadata_max,AVERAGE')
	metadata_vdef3 = VDEF(vname="metadata_last", rpn='Metadata_max,LAST')
	metadata_vdef4 = VDEF(vname="metadata_min", rpn='Metadata_max,MINIMUM')

	metadata_gprint1 = GPRINT(metadata_vdef1, "Max\\: %5.1lf %s")
	metadata_gprint2 = GPRINT(metadata_vdef2, "Avg\\: %5.1lf %s")
	metadata_gprint3 = GPRINT(metadata_vdef3, "Current\\: %5.1lf %s")
	metadata_gprint4 = GPRINT(metadata_vdef4, "Min\\: %5.1lf %s\\n")

	line4 = LINE(1,defObj=def4, color='#8E14A7', legend='Metadata_max')

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
	#g = Graph(imgname, imgformat='PNG', step=start, vertical_label='Units_B', color=ca, width=700, height=400, units_exponent=6, base=1024, title=title)
	g = Graph(imgname, imgformat='PNG', step=start, vertical_label='Units_B', x_grid="MINUTE:10:HOUR:1:HOUR:4:0:%X", alt_y_grid=True, rigid=True, color=ca, width=700, height=400, units_exponent=6, base=1024, title=title)
	g.data.extend([def1, vdef1, vdef2, vdef3, vdef4, line1, gprint1, gprint2, gprint3, gprint4])
	g.data.extend([def2, s1_vdef1, s1_vdef2, s1_vdef3, s1_vdef4, line2, s1_gprint1, s1_gprint2, s1_gprint3, s1_gprint4])
	g.data.extend([def3, eden_vdef1, eden_vdef2, eden_vdef3, eden_vdef4, line3, eden_gprint1, eden_gprint2, eden_gprint3, eden_gprint4])
	g.data.extend([def4, metadata_vdef1, metadata_vdef2, metadata_vdef3, metadata_vdef4, line4, metadata_gprint1, metadata_gprint2, metadata_gprint3, metadata_gprint4])
	g.write()


if __name__ == '__main__':
	#create_java_heap_memory()
	graph(period='day')
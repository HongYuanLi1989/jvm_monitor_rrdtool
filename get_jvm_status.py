#!/usr/bin/env python

import subprocess
from jvm_rrdtool import RRDController
import os
import time
import sys
import socket

class Jprocess:
    def __init__(self, arg):
        self.pdict = {
        "jpname": arg,
        }
        self.zdict = {
        "Heap_used" : 0,
        "Heap_ratio" : 0,
        "Heap_max" : 0,
        "Metadata_used" : 0,
        "Metadata_ratio" : 0,
        "Metadata_max"  : 0,
        "S0_used"   : 0,
        "S0_ratio"  : 0,
        "S0_max"    : 0,
        "S1_used"   : 0,
        "S1_ratio"  : 0,
        "S1_max"    : 0,
        "Eden_used" : 0,
        "Eden_ratio" : 0,
        "Eden_max"  : 0,
        "Old_used"  : 0,
        "Old_ratio" : 0,
        "Old_max"   : 0,
        "YGC"       : 0,
        "YGCT"      : 0,
        "YGCT_avg"  : 0,
        "FGC"       : 0,
        "FGCT"      : 0,
        "FGCT_avg"  : 0,
        "GCT"       : 0,
        "GCT_avg"   : 0,
        }
    def check_proc(self):
        command = "ps aux | grep /data/deploy/apache-tomcat-7.0.69/conf/logging.properties | grep -v grep | awk '{print $2}'"
        pidout = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        pid = pidout.stdout.readline().split("\n")
        self.pdict['pid'] = pid[0]
        return self.pdict['pid']

    def get_jstats(self):
        if self.pdict['pid'] == '':
            return False
        #print self.pdict['pid']
        self.pdict.update(self.fill_jstat("-gc"))
        self.pdict.update(self.fill_jstat("-gccapacity"))
        self.pdict.update(self.fill_jstat("-gcutil"))
    def fill_jstat(self, opts):
        command = "/data/apps/jdk1.8.0_91/bin/jstat %s %s" %(opts, self.pdict['pid'])
        jstatout = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = jstatout.communicate()
        legend, data = stdout.split('\n',1)
        mydict = dict(zip(legend.split(), data.split()))
        #print mydict
        return mydict
    def compute_jstats(self):
        if self.pdict['pid'] == "":
            return False
        self.zdict['S0_used'] = format(float(self.pdict['S0U']) * 1024,'0.2f')
        self.zdict['S0_max'] =  format(float(self.pdict['S0C']) * 1024,'0.2f')
        self.zdict['S0_ratio'] = format(float(self.pdict['S0']) ,'0.2f')
        self.zdict['S1_used'] = format(float(self.pdict['S1U']) * 1024,'0.2f')
        self.zdict['S1_max'] = format(float(self.pdict['S1C']) * 1024,'0.2f')
        self.zdict['S1_ratio'] = format(float(self.pdict['S1']) ,'0.2f')
        self.zdict['Old_used'] = format(float(self.pdict['OU']) * 1024,'0.2f')
        self.zdict['Old_max'] =  format(float(self.pdict['OC']) * 1024,'0.2f')
        self.zdict['Old_ratio'] = format(float(self.pdict['O']) ,'0.2f')
        self.zdict['Eden_used'] = format(float(self.pdict['EU']) * 1024,'0.2f')
        self.zdict['Eden_max'] = format(float(self.pdict['EC']) * 1024,'0.2f')
        self.zdict['Eden_ratio'] = format(float(self.pdict['E']),'0.2f')
        self.zdict['Metadata_used'] = format(float(self.pdict['MU']) * 1024,'0.2f')
        self.zdict['Metadata_max'] = format(float(self.pdict['MC']) * 1024,'0.2f')
        self.zdict['Metadata_ratio'] = format(float(self.pdict['M']),'0.2f')
        self.zdict['Heap_used'] = format((float(self.pdict['EU']) + float(self.pdict['S0U']) + float(self.pdict['S1U'])  + float(self.pdict['OU'])) * 1024,'0.2f')
        self.zdict['Heap_max'] = format((float(self.pdict['EC']) + float(self.pdict['S0C']) + float(self.pdict['S1C'])  + float(self.pdict['OC'])) * 1024,'0.2f')
        self.zdict['Heap_ratio'] = format(float(self.zdict['Heap_used']) / float(self.zdict['Heap_max'])*100,'0.2f')
        self.zdict['YGC'] = self.pdict['YGC']
        self.zdict['FGC'] = self.pdict['FGC']
        self.zdict['YGCT'] = format(float(self.pdict['YGCT']),'0.3f')
        self.zdict['FGCT'] = format(float(self.pdict['FGCT']),'0.3f')
        self.zdict['GCT'] = format(float(self.pdict['GCT']),'0.3f')
        self.zdict['Process_Name'] = self.pdict['jpname']
        self.zdict['ipaddress'] = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        if self.pdict['YGC'] == '0':
            self.zdict['YGCT_avg'] = '0'
        else:
            self.zdict['YGCT_avg'] = format(float(self.pdict['YGCT'])/float(self.pdict['YGC']),'0.3f')
        if self.pdict['FGC'] == '0':
            self.zdict['FGCT_avg'] = '0'
        else:
            self.zdict['FGCT_avg'] = format(float(self.pdict['FGCT'])/float(self.pdict['FGC']),'0.3f')
        if self.pdict['YGC'] == '0' and self.pdict['FGC'] == '0':
            self.zdict['GCT_avg'] = '0'
        else:
            self.zdict['GCT_avg'] = format(float(self.pdict['GCT'])/(float(self.pdict['YGC']) + float(self.pdict['FGC'])),'0.3f')

if __name__ == '__main__':

    RRD_PATH = "%s/../../data" % os.path.abspath(os.path.dirname(__file__))
    STATIC_PATH = "%s/../../media/image" % os.path.abspath(os.path.dirname(__file__))

    rrdfile = RRD_PATH + "/heap_memory.rrd"
    imgdir = STATIC_PATH + "/heap_memory"

    if not (os.path.isdir(imgdir)):
        os.makedirs(imgdir)
    
    rrd = RRDController(rrdfile=rrdfile, static_path=imgdir)
    rrd.create()

    jproc = Jprocess("service_account")
    pid = jproc.check_proc()

    jproc.get_jstats()
    jproc.compute_jstats()
    zdict = jproc.zdict
    print jproc.zdict
    rrd.update(
    YGCT_avg=float(zdict['YGCT_avg']),
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
    rrd.graph(period='day')
    print jproc.zdict
    #print jproc.pdict
    
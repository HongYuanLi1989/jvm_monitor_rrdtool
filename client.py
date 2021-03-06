#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-09 10:13:56
# @Author  : LiHongyuan (hy.li@8win.com)

import requests
import json
import subprocess
import os
import time
import sys
import socket

class Jprocess:
    def __init__(self, jpname, service_name):
        self.pdict = {
        "jpname": jpname,
        "service_name": service_name,
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
        #print self.pdict['jpname']
        command = "ps aux | grep '"+ self.pdict['jpname'] +"' | grep -v grep | awk '{print $2}'"
        #print command
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
        command = "/data/apps/java/jdk1.8.0_45/bin/jstat %s %s" %(opts, self.pdict['pid'])
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
        self.zdict['Process_Name'] = self.pdict['service_name']
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
#    serviceName = {"com.zhangyu.trad.booter.ServiceSecurityMain":"zy-trad-service-security","com.zhangyu.trad.booter.TradPusherMain":"zy-trad-pusher","com.zhangyu.trad.booter.ServiceAccountMain":"zy-trad-service-account","com.zhangyu.trad.booter.ServiceMonitorMain":"zy-trad-service-monitor",	"com.zhangyu.trad.booter.ServicePrizeMain":"zy-trad-service-prize","com.zhangyu.trad.booter.TradTaskMain":"zy-trad-task","com.zhangyu.trad.booter.ServiceMatchMain":"zy-trad-service-match","/data/deploy/dev-zy-trad-partner/apache-tomcat/bin/bootstrap.jar":"zy-trad-partner","/data/deploy/dev-zy-trad-admin/apache-tomcat/bin/bootstrap.jar":"zy-trad-admin"}
#    command = "ps aux | grep java| grep -v 'wrapper.script.version'| grep -v 'jstat' | grep -v grep | grep -v apache-tomcat| awk '{print $NF}'"
#    pidout = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
#    pid = pidout.stdout.readlines()
    def getJvmList():
        service_dict = {}
        for root,subFolders,files in os.walk("/data/deploy/"):
            for filename in files:
              if filename.find('.pid') !=-1 :
                target_dir = root.split("/")[1:4]
                for root,subFolders,files in os.walk("/"+"/".join(target_dir)):
                  #print root,subFolders,files
                  if "wrapper.conf" in files:
                    #print files
                    with open(os.path.join(root,"wrapper.conf")) as f:
                      data = f.readlines()
                      for item in data:
                        if "wrapper.app.parameter.1" in item:
                          jpname = item.split("=")[1].split("\n")[0]
                          service_name = root.split("/")[3].replace("dev-","")
                          service_dict.update({jpname:service_name})
                  elif "catalina.sh" in files:
                    #print files
                    jpname = root+"/"+files[0]
                    service_name =  root.split("/")[3].replace("dev-","")
                    service_dict.update({jpname:service_name})
        return service_dict
    serviceName = getJvmList()
    #print serviceName
    #print type(serviceName)
    for item in serviceName:
        jproc = Jprocess(jpname=item,service_name=serviceName[item])
        pid = jproc.check_proc()
        if pid == '':
            print "pid is not valid value"
            sys.exit(1)
        if not jproc.get_jstats():
            if not jproc.compute_jstats():
                zdict = jproc.zdict
                #print zdict
                print "start report to server.........."
                zdict = json.dumps(zdict)
                try:
                    res = requests.post("http://192.168.0.107:5000/upload/",data=zdict)
                except requests.exceptions.RequestException as e:    # This is the correct syntax
                    print e
                    sys.exit(1)
                print res.text
            else:
                print "get_jstatas failed!"
                sys.exit(1)
        #time.sleep(1)
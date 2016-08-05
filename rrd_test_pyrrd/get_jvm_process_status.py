#!/usr/bin/env python

import subprocess

command = "/data/apps/jdk1.8.0_91/bin/jstat -gcutil 7566"

def get_jvm_gcutil_status():
    jstatout = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    stdout, stderr = jstatout.communicate()
    legend, data = stdout.split('\n',1)
    mydict = dict(zip(legend.split(), data.split())
    return mydict

command_gc = "/data/apps/jdk1.8.0_91/bin/jstat -gc 7566"
def get_jvm_gc_status():
    jstatout = subprocess.Popen(command_gc, shell=True, stdout=subprocess.PIPE)
    stdout, stderr = jstatout.communicate()
    legend, data = stdout.split('\n',1)

    mydict = dict(zip(legend.split(), data.split()))
    return mydict

command_gc = "/data/apps/jdk1.8.0_91/bin/jstat -gccapacity 7566"    
def get_jvm_gccapacity_status():
    jstatout = subprocess.Popen(command_gc, shell=True, stdout=subprocess.PIPE)
    stdout, stderr = jstatout.communicate()
    legend, data = stdout.split('\n',1)

    mydict = dict(zip(legend.split(), data.split()))
    return mydict

if __name__ == '__main__':
	print get_jvm_gcutil_status()
	print get_jvm_gc_status()
	print get_jvm_gccapacity_status()
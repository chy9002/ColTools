#!python
# -*- coding: utf-8 -*-

from multiprocessing import Pool
import os
import subprocess
import sys
import time
import re

def formatOutput(Output, Filename, uniKey):
    NoResult = list(re.findall(r'([0-9]*)(\.[^.\\/:*?"<>|\r\n]+)$', Filename))
    extResult = list(re.findall(r'[0-9]*\.[^.\\/:*?"<>|\r\n]+$', Filename))
    fileNo=''
    fileNoWithext=''
    if len(extResult)>0:
        fileNo = NoResult[0][0]
        fileNoWithext = extResult[0]
    if uniKey != '':
        uniKey = time.strftime('%Y%m%d', time.localtime())+uniKey
    Filename = str.replace(Filename,fileNoWithext,'')
    result = Output+'/'+Filename+uniKey+'_'+fileNo+'.gz'
    return result

def processTask(cmd):
    sp = subprocess.call(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    return sp

def WalkDir(zipDir,Output, rootDir, uniKey, IsIncremental):
    list_dirs = os.walk(rootDir)
    results = []
    p = Pool(4)
    for root, dirs, files in list_dirs:
        for f in files:
            sourcepath = os.path.join(root, f)
            filename = os.path.basename(f)
            cmd = []
            if IsIncremental == '1':
                cmd = [zipDir, 'a', '-tgzip','-mx=1', formatOutput(Output, filename,uniKey), sourcepath]
            else:
                cmd = [zipDir, 'a', '-tgzip','-mx=1', formatOutput(Output, filename,''), sourcepath]
            results.append(p.apply_async(processTask,args=(cmd,)))
    p.close()
    p.join()
    for res in results:
        if int(res.get()) != 0:
            raise NameError('7z error, compress failed!')
    print 'All subprocesses done.'




if __name__ == '__main__':
    ###
    # This script need five argv
    # 1: "C:\Program Files (x86)\7-Zip\7zg" it's 7z path
    # 2: output path
    # 3: Input path
    # 4: add a batch id
    # 5: Add Datetime
    ###
    WalkDir(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

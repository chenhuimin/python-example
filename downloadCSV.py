#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created By chenhuimin
import os
import urllib2
import urllib
from datetime import datetime, timedelta


def main():
    defaultUrl = "http://192.168.7.194:8080/rest/v1/policyBXB/apply/download"
    url = raw_input("Please enter download url (default: %s):" % defaultUrl) or defaultUrl
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    begin = raw_input("Please enter begin search date (default: %s):" % yesterday) or yesterday
    end = raw_input("Please enter end search date (default: %s):" % yesterday) or yesterday
    # defaultSavedDirctory = "download"
    # savedDirctory = raw_input(
    #     "Please enter the directory to save download file(default: %s):" % defaultSavedDirctory) or defaultSavedDirctory
    url = url + "?begin=%s&end=%s" % (begin, end)
    print "The target download url is %s" % url
    remotefile = urllib2.urlopen(url)
    headers = remotefile.info()
    if (headers.has_key('Content-Disposition')):
        encodedFilename = headers['Content-Disposition'].split('filename=')[-1].strip()
        filename = urllib.unquote_plus(encodedFilename)
        data = remotefile.read()
        # parentPath = os.path.dirname(os.path.abspath(__file__))
        # targetPath = os.path.join(parentPath, savedDirctory)
        # if not os.path.exists(targetPath):
        #     os.makedirs(targetPath)
        # savedFile = os.path.join(targetPath, filename.decode('utf-8').encode('gb2312'))
        targetPath = filename.decode('utf-8').encode('gb2312')
        with open(targetPath, "wb") as out:
            out.write(data)
    else:
        print ("No data to download ")


if __name__ == "__main__":
    main()
    raw_input('Press <enter> to exit...')

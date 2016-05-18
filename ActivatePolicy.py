#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created By chenhuimin
import sys, os
import urllib2
import urllib
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import json
from datetime import datetime, timedelta


def download():
    # defaultDownloadUrl = "http://192.168.7.194:8080/rest/v1/policyBXB/apply/download"
    defaultDownloadUrl = "http://store.91baofeng.com/rest/v1/policyBXB/apply/download"
    downloadUrl = raw_input("Please enter download url (default: %s):" % defaultDownloadUrl) or defaultDownloadUrl
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    begin = raw_input("Please enter begin search date (default: %s):" % yesterday) or yesterday
    end = raw_input("Please enter end search date (default: %s):" % yesterday) or yesterday
    downloadUrl = downloadUrl.strip() + "?begin=%s&end=%s" % (begin.strip(), end.strip())
    print "The target download url is %s" % downloadUrl
    try:
        remotefile = urllib2.urlopen(downloadUrl)
    except urllib2.URLError:
        print "May be the server is down,connect to the server failed"
        return
    headers = remotefile.info()
    if headers.has_key('Content-Disposition'):
        encodedFilename = headers['Content-Disposition'].split('filename=')[-1].strip()
        filename = urllib.unquote_plus(encodedFilename)
        data = remotefile.read()
        # filename = filename.decode('utf-8').encode('gb2312')
        with open(filename, "wb") as out:
            out.write(data)
    else:
        print ("No data to download ")


def uploadAndParse():
    # defaultUploadUrl = "http://192.168.7.194:8080/rest/v1/policyBXB/parseCSV"
    defaultUploadUrl = "http://store.91baofeng.com/rest/v1/policyBXB/parseCSV"
    uploadUrl = raw_input("Please enter upload url (default: %s):" % defaultUploadUrl) or defaultUploadUrl
    fileName = raw_input("Please enter csv file name:")
    if not fileName:
        print "File name is required"
        return
    if fileName.find(".csv") == -1:
        fileName = fileName.strip() + ".csv"
    currentPath = cur_file_dir()
    # targetFile = os.path.join(currentPath, fileName.decode('utf-8'))
    targetFile = os.path.join(currentPath, fileName.strip())
    if not os.path.exists(targetFile):
        print "The target csv file: %s is not existed" % targetFile
        return
    print "The selected upload file path is: %s" % targetFile
    register_openers()
    with open(targetFile, 'r') as f:
        datagen, headers = multipart_encode({"csv": f})
        request = urllib2.Request(uploadUrl.strip(), datagen, headers)
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError:
            print "May be the server is down,connect to the server failed"
            return
        code = response.code
        if code != 200:
            print "Upload failed, http status code is %d" % code
            return
        data = json.load(response)
        if data:
            resultCode = data['code']
            if resultCode != 0:
                errorMsg = data['errorMsg']
                print "csv parse faild, return error msg is: %s" % errorMsg
                return
            else:
                print "The upload csv file is parsed successfully, return data:"
                dataStr = json.dumps(data['data'], sort_keys=True, indent=4)
                print dataStr


def cur_file_dir():
    # 获取脚本路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def main():
    defaultOperation = "1"
    operation = raw_input(
        "Please choose the operation: 1.download CSV; 2.upload and parse CSV (default: %s):" % defaultOperation) or defaultOperation
    if operation.strip() == "1":
        download()
    elif operation.strip() == "2":
        uploadAndParse()
    else:
        print "No valid operation selected, please choose 1 or 2 to operate."


if __name__ == "__main__":
    input = ''
    while input.strip() != 'exit':
        main()
        input = raw_input('Enter <exit> to exit...  ')

#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'FuJunYi'
__version__ = "v1.0.%s.%s"

import os
import time
import xml.etree.ElementTree as eT


class SoapOrder(object):
    def __init__(self, xmlFile, soapPath):
        self.xmlFile = xmlFile
        self.soapPath = soapPath

    def createSoapOrder(self, MSISDN=None):
        namespaceMmt = "http://www.chinaunicom.com/IMS/VoLTEAS/"
        namespaceSoapEnv = "http://schemas.xmlsoap.org/soap/envelope/"
        FileExist = os.path.isfile(self.xmlFile)
        if FileExist:  # 判断文件是否存在
            eT.register_namespace('mmt', namespaceMmt)     # xml命名空间注册
            eT.register_namespace('soapenv', namespaceSoapEnv)    # xml命名空间注册
            tree = eT.parse(self.xmlFile)
            root = tree.getroot()
            body = root.find("{%s}Body" % namespaceSoapEnv)
            set_owsBr = body.find("{%s}SET_OWSBR" % namespaceMmt)
            imPu = set_owsBr.find("{%s}IMPU" % namespaceMmt)
            imPu.text = "sip:+86%s@an.ims.mnc001.mcc460.3gppnetwork.org" % MSISDN    # 修改xml标签内容
            tree.write(os.path.join(self.soapPath, "Soap", "%s.xml") % MSISDN)     # 保存成xml文件
            return True
        else:
            return False  # 异常返回


class TelnetOrder(object):
    def __init__(self, telnetPath):
        self.telnetPath = telnetPath

    def createTelnetOrder(self, MSISDN=None, ImSI=None):
        with open(os.path.join(self.telnetPath, "Telnet", "%s.txt" % MSISDN), "w", encoding="utf-8") as file:
            file.write("HGSDC:MSISDN=86%s,SUD=OBA-0;\n" % MSISDN)
            file.write("HGSDC:MSISDN=86%s,SUD=OBSSM-0;\n" % MSISDN)
            file.write("HGSNC:MSISDN=86%s,NAM=0;\n" % MSISDN)
            file.write("HSSEC:IMSI=%s,EPSODB=NONE;\n" % ImSI)
        pass


if __name__ == "__main__":
    tempFile = r"D:\Python\CoreNetwork\Template\Soap\SoapOrder.xml"   # xml模板文件
    csvF = r"D:\Python\CoreNetwork\Template\20200901.csv"
    orderPath = r"D:\Python\CoreNetwork\Order"
    start = time.time()
    f = open(csvF, "r", encoding="utf-8")
    lines = f.readlines()  # 获取文件内容列表，按行
    telnetOrder = TelnetOrder(orderPath)
    soapOrder = SoapOrder(tempFile, orderPath)
    for i in range(1, len(lines)):
        line = lines[i].strip().split(",")
        telnetOrder.createTelnetOrder(line[0], line[1])
        soapOrder.createSoapOrder(line[0])
    else:
        print("总用时：%s" % (time.time() - start))
    pass

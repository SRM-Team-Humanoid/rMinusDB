#!/usr/bin/env python
import time
import csv
import numpy as np
from pprint import pprint
import xml.etree.cElementTree as ET
from collections import Counter
from copy import deepcopy




class XmlTree(object):

    def __init__(self,str):
        try:
            with open(str) as f:
                pass
            self.tree = ET.ElementTree(file=str)
        except:
            raise RuntimeError("File not found.")


    def pageconvert(self,filename):
        find = "PageRoot/Page"
        pages = [x for x in self.tree.findall(find)]
	row = ["Page","Frame"] + ["Motor "+str(id) for id in range(1,19)]
	rows = [row]
	for page in pages:
		text = page.attrib['name']
		find = "PageRoot/Page[@name='" + text + "']/steps/step"
		steps = [x for x in self.tree.findall(find)]
		for step in steps:
			row = [text] + [step.attrib['frame']] + step.attrib['pose'].split()
			rows.append(row)
	with open(filename, 'wb') as f:
    		writer = csv.writer(f)
    		writer.writerows(rows)

    def flowconvert(self,filename):
        find = "FlowRoot/Flow"
        flows = [x for x in self.tree.findall(find)]
	row = ["Flow","PageID","PageName","Speed"]
	rows = [row]
	for flow in flows:
		text = flow.attrib['name']
		find = "FlowRoot/Flow[@name='"+text+"']/units/unit"
		steps = [x for x in self.tree.findall(find)]
		count = 1
		for step in steps:
			row = [text] + [count] + [step.attrib['main']] + [step.attrib['mainSpeed']]
			rows.append(row)
			count +=1

	with open(filename, 'wb') as f:
    		writer = csv.writer(f)
    		writer.writerows(rows)





tree = XmlTree('data.xml')
tree.pageconvert('pagedata.csv')
tree.flowconvert('flowdata.csv')



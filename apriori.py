# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 19:16:38 2020

@author: Hiral
"""
import csv
import re
file = open("data.txt", 'r')
#reader = csv.reader(file)
#allRows = [int(row) for row in reader]

T = [list(map(int,rec)) for rec in csv.reader(file, delimiter=',')]

file2 =  open("mis.txt", 'r')                                                  #doesnt work if mis.txt has \n in the end.
a=file2.read()
d= {}
for x in a.split("\n"):
    (k,v) = x.split("=")
    
    d[k.strip()] = float(v.strip())

sdc = d['SDC']
d.pop('SDC', None)

sorted_mis = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}    #M sorted items according to MIS values.

support_count = {}
unique_items = []
for transaction in T:
    for item in transaction:
        support_count[item] = 0

I = []
for key in support_count:
    I.append(key)

temp_I = I
for key in sorted_mis:                                                         #if MIS.txt has an item that is not used
                                                                               #in the transactions file exception will 
                                                                               #be thrown
    if key == 'MIS(rest)':
        continue
    item = int(re.findall(r'\d+', key)[0])
    temp_I.remove(item)
for item in temp_I:
    sorted_mis['MIS('+str(item)+')'] = sorted_mis['MIS(rest)']
sorted_mis.pop('MIS(rest)', None)

M_ = {k: v for k, v in sorted(sorted_mis.items(), key=lambda item: item[1])}   #consists of sorted values

M = {}
for key in M_:
    M[int(re.findall(r'\d+', key)[0])] = M_[key]                               #conversion of string keys to int

for key in support_count:
    for transaction in T:
        if key in transaction:
            support_count[key] += 1
            continue
M_keys = []    
for key in M:
    M_keys.append(key)
""" creating L from sorted lsit of items in the order of ascending mis values.""" 
L = []
L.append(M_keys[0])
for item in M_keys[1:]:
    if support_count[item]/len(T) >= M[M_keys[0]]:
        L.append(item)
        
""" creating F1 frequent itemset """
F1 = []
for l in L:
    if support_count[l]/len(T) >= M[l]:
        F1.append(l)
        
""" Variables we have """
print("M is a dictionary that consists of items as keys and MIS as values:",M)
print("M_keys consists of all items in M sorted in the order of ascending MIS values:",M_keys)
print("L consists of items satisfying the algorithm",L)
print("F1 is the frequent itemset",F1)

""" Candidate Generation Function """
#working
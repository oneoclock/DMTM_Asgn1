# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 19:16:38 2020

@author: Hiral
"""
import csv
import re
import itertools
import sys

if len(sys.argv)!=3:
	print('Please provide input mis file names\n')
	print('python apriori.py data.txt MIS.txt')
	exit()

file = open(sys.argv[1], 'r')
#file = open("data.txt", 'r')
#reader = csv.reader(file)
#allRows = [int(row) for row in reader]

T = [list(map(int,rec)) for rec in csv.reader(file, delimiter=',')]
N=len(T)

file2 =  open(sys.argv[2], 'r')                                                  #doesnt work if mis.txt has \n in the end.
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
        
#""" Variables we have """
#print("M is a dictionary that consists of items as keys and MIS as values:",M)
#print("M_keys consists of all items in M, sorted in the order of ascending MIS values:",M_keys)
#print("L consists of items satisfying the algorithm",L)
#print("F1 is the frequent itemset",F1)
#print("Support count of all the items in all Transactions",support_count)

numT = len(T)

def get_M():
    return M
def get_M_keys():
    return M_keys
def get_L():
    return L
def get_F1():
    return F1
def get_support_count():
    return support_count
def get_sdc():
    return sdc
def get_numT():
    return len(T)
def get_T():
    return T

""" Candidate Generation Function """
def level2_can_gen(L,numT,sdc):
    L_temp = []
    L_temp.extend(L)
    C2=[]
    for idx in range(len(L)):
        L_temp.pop(0)
        if (support_count[L[idx]] / numT) >= M[L[idx]]:
            for item in L_temp:
                if (support_count[item] / numT) >= M[L[idx]] and (abs(support_count[item] - support_count[L[idx]]) <= sdc):
                    C2.append([L[idx],item])
    return C2

class candidate:
    def __init__(self, count, items):
        self.count=count
        self.items=items
F={}
F[1] = get_F1()
def apriori():
    k=2
    
    while True:
        fk = []
        candidates = []                                                        #k-itemset candidates
        
        if k==2:
            ck = level2_can_gen(L,numT,sdc)                                    #ck is current k-item candidate set
        else:
            F_k_1=F[k-1]
            C=[]
            for i in range(len(F_k_1)):
                for j in range(len(F_k_1)): 
                    f1 = F_k_1[i][:k-2]
                    f2 = F_k_1[j][:k-2]
                    if F_k_1[i]==F_k_1[j]:
                    	continue
                    if f1==f2:
                        
                        
                        ik_1=F_k_1[i][-1] 
                        ik_2=F_k_1[j][-1]
                     

                        if (M_keys.index(ik_1)<M_keys.index(ik_2)) and (abs((support_count[ik_1]/numT)-(support_count[ik_2]/numT))<=sdc): #add candidate 
                           
                            c=F_k_1[i].copy()
                            
                            c.append(ik_2)
                 
                            flag=False
                            
                            for s in itertools.combinations(c, k-1): #prune the candidate list
                                #s=c[window:k-1]
                        
                                s=list(s)
                            
                                if (c[0] in s) or (M[c[1]]==M[c[0]]):
                                	if s not in F_k_1:
                      
                                		flag=True
                                		break
                            
                            if not (flag):
                            
                            	C.append(c)
           
            #break added for debugging
            if len(C)>0:
                F[k]=C
                ck = F[k]
            else:
            	ck=None
        #print(ck)
        #break
        #candidate_counts = [] * len(ck)
        if not ck:
        	break

        for t in T:
            for c in ck:                                                       #k-set candidates should not repeat that is 
                candidates.append(candidate(0,c))                              #[[1,2],[2,1]]  <- should not occur.
                if all(elem in t  for elem in c):
                    candidates[-1].count += 1
        for c in candidates:
            if (c.count/numT >= M[c.items[0]]):
                fk.append(c.items)
        F[k] = fk    
        k+=1
        ###
        #break
    return F

a= apriori()
print(a)
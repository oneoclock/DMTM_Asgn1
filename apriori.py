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
    print(L)
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
    fk = [0]
    while not not fk:
        fk = []
        candidates = []                                                        #k-itemset candidates
        
        if k==2:
            ck = level2_can_gen(L,numT,sdc)                                    #ck is current k-item candidate set
        else:
            print("not implemented")
            #F_k_1=[(40,4),(50,3),(20,5),(40,3)]#F[k-1]
            F_k_1=F[k-1]
            F_k_1=[(50, 30), (50, 40), (30, 40), (10, 4), (10, 9), (4, 9), (6, 8), (6, 1), (6, 2), (8, 1), (8, 2), (1, 2), (3, 5), (7, 20)]
            #print(F_k_1)
            
            C=[]
            for i in range(len(F_k_1)):
                for j in range(i+1, len(F_k_1)): 
                    f1 = list(F_k_1[i])[:k-2]
                    f2 = list(F_k_1[j])[:k-2]
                    if f1==f2:
                        #print(f1)
                        
                        ik_1=F_k_1[i][-1] 
                        ik_2=F_k_1[j][-1]
                        #print(ik_1,ik_2)
                        #print('M[ik_1]',M[ik_1])
                        #print('M[ik_2]',M[ik_2])
                        if M_keys.index(ik_1)<M_keys.index(ik_2) and (abs(M[ik_1]-M[ik_2])<=sdc): #add candidate 
                            print("good")
                            c=list(F_k_1[i])
                            c.append(ik_2)
                            flag=False
                            
                            for window in range(k-1): #prune the candidate list 
                                s=c[window:k-1]
                                if (c[0] in s) or (M[c[1]]==M[c[0]]):
                                    if s in F_k_1:
                                        flag=True
                                        break
                            
                            if not (flag):
                                C.append(set(c))
            print(C)
            #break
            if len(C)>0:
                F[k]=C
                ck = F[k]
        #print(ck)
        #break
        #candidate_counts = [] * len(ck)
        for t in T:
            for c in ck:                                                       #k-set candidates should not repeat that is 
                candidates.append(candidate(0,c))                              #[[1,2],[2,1]]  <- should not occur.
                if all(elem in t  for elem in c):
                    candidates[-1].count += 1
        for c in candidates:
            if (c.count/numT >= M[c.items[0]]):
                fk.append(c.items)
        F[k] = fk       
        print(fk)
        k+=1
        ###
        #break
    return fk

a= apriori()
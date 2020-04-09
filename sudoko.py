import numpy as np
import random as rnd
class Sudoko:
    def __init__(self):
        self.que=np.zeros((9,9)).astype(str)
        self.que[:,:]=' ';
        self.values=np.copy(self.que)
        self.create()
        self.ans=np.copy(self.que)
        self.space()
        
    def row(self,r,v):
        return set(v[r,:])-{' '}
    def col(self,c,v):
        return set(v[:,c])-{' '}
    def box(self,i,j,v):
        i-=i%3
        j-=j%3
        return set(list(v[i,j:j+3])+list(v[i+1,j:j+3])+list(v[i+2,j:j+3]))-{' '}
    def space(self):
        l=[]
        for i in range(0,9):
            for j in range(0,9):
                l.append((i,j))
        rnd.shuffle(l)
        rnd.shuffle(l)
        i=0
        k=0
        while k<=40:
            if len(list(self.box(*l[i],self.que)))>4:
                k+=1
                self.que[l[i]]=' '
            i+=1

    def create(self):
        j=0
        while j<9:
            i=0
            k=0
            while i<9:
                k+=1
                l=set(['1','2','3','4','5','6','7','8','9'])-(self.box(j,i,self.que)|self.row(j,self.que)|self.col(i,self.que))
                if len(l)==0:
                    i=-1
                    self.que[j:]=' '
                else:
                    self.que[j,i]=rnd.choice(list(l))
                i+=1
                if k>100:
                    j=-1
                    self.que[:,:]=' '
                    break
            j+=1
    def check(self,i,j,k):
        if k==' ':
            return
        list=[]
        for c in range(9):
            if (self.que[i,c]==k or self.values[i,c]==k):
                list.append((i,c))
        for r in range(9):
            if (self.que[r,j]==k or self.values[r,j]==k) and r!=i:
                list.append((r,j))
        for r in range(i-i%3,i-i%3+3):
            for c in range(j-j%3,j-j%3+3):
                if r!=i and c!=j:
                    if self.que[r,c]==k or self.values[r,c]==k:
                        list.append((r,c))
        return list
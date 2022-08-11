'''
Created on 7 Aug 2022

@author: stefanosilva
'''
    
    
def countList(lst):
    count = 0
    for el in lst:
        if type(el)== type([]):
            count+= 1         
    return count
    
        

for i in range(0,40,5):
    print(i)
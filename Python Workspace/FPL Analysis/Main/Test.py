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
    
        
a = [1,2,3,4,5]
print(a[1:])
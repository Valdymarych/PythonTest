import numpy as np

a=np.array([[True],[False]])
b=np.array([
    [1,0,1],
    [2,6,1]
])
c=np.array([
    [0,1,1],
    [6,2,1]
])
print(np.where(a,b,[5,53,1]))
print(a.shape,b.shape,np.array([5,53,1]).shape)
import time

def run(**args):
	time0=time.time()
	while (True):
		if time.time()-time0>50:
			with open(r'd:\\Program Files\\MATLAB\\R2016b\\bin\\win64\\data.txt','r') as fp:
				ss=fp.readlines()            
			return str(ss)

        

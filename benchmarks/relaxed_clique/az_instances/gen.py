import random

numNode = [10,20,50,100,200,300,400,500]
p = [0.5,0.8,0.9,1]

for x in numNode:
	for y in p:
		g = []
		outfile_wc = open('p'+str(int(float(str(y*100))))+'n'+str(x), 'w')
		for i in range(0, x):
		    outfile_wc.write('node('+str(i)+').\n')
		    g.append([])
		    for j in range(0, x):
		        r = random.random()
		        if r < y:
		            g[i].append(1)
		            outfile_wc.write('edge(' + str(i) + ', ' + str(j) + ').\n')
		        else:
		            g[i].append(0)

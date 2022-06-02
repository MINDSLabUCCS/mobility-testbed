import matplotlib.pyplot as plt 


def polyDraw(rectangle):
	plt.figure(figsize=(16, 16))
	plt.axis('equal')
	for i in rectangle:
		x = (i[::2])
		y = (i[1::2])	
		print(len(x))
		print(len(y))
		plt.fill(x, y)
	plt.savefig('map_2.png')

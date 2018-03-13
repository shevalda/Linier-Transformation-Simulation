import math, copy

"""
	Fungsi yang mengubah matriks dengan titik-titik poligon hasil
	transformasi menjadi matriks dengan titik-titik yang sesuai untuk
	ditampilkan.
"""
def showShape(M):
	mShow = copy.deepcopy(M)
	for point in mShow:
		point[0] = 250 + point[0]
		point[1] = 250 + point[1]
	return mShow

"""
	Mengubah list dengan satu indeks (baris) menjadi sebuah list dengan dua indeks (baris dan kolom) untuk perkalian matriks
"""
def convert1(X):
	for i in range(len(X)):
		X.reverse()
		Elmt = X.pop()
		X.reverse()
		X.append([Elmt])

"""
	Mengembalikan list menjadi bentuk sebelum diaplikasikan prosedur convert1
"""
def convert2(X):
	for i in range(len(X)):
		X.reverse()
		Elmt = X.pop()
		X.reverse()
		X.append(Elmt[0])

""" Mengembalikan nilai cos(rad) """
def toCos(rad):
	return math.cos(rad)

""" Mengembalikan nilai sin(rad) """
def toSin(rad):
	return math.sin(rad)

""" Prosedur perkalian matriks 2*2 """
def xMatriks(M1, M2):
	return [[sum(a*b for a,b in zip(M1_row,M2_col)) for M2_col in zip(*M2)] for M1_row in M1]

# PROSEDUR-PROSEDUR TRANSFORMASI
"""
	op : translate <dx> <dy>
	Mentranslasi matriks poligon sebesar <dx> dan <dy>
"""
def translate(M, op):
	dx = float(op[1]) / 2.0
	dy = float(op[2]) / 2.0
	for point in M:
		point[0] = point[0] + dx
		point[1] = point[1] + dy

"""
	op : dilate <k>
	Mendilatasi/mengkontraksi matriks poligon terhadap skala <k>
"""
def dilate(M, op):
	k = float(op[1])

	Mdilate = [[k, 0], [0, k]]
	
	for i in range(len(M)):
		convert1(M[i])
		M[i] = xMatriks(Mdilate, M[i])
		convert2(M[i])

"""
	op : rotate <deg> <a> <b>
	Merotasi matriks poligon sebesar <deg> derajat terhadap titik (a,b)
"""
def rotate(M, op):
	deg = float(op[1])
	a = float(op[2]) / 2.0
	b = float(op[3]) / 2.0
	
	cent = [a, b]
	rad = deg * math.pi / 180.0
	
	Mrotate = [[toCos(rad), -toSin(rad)], [toSin(rad), toCos(rad)]]
	
	for i in range(len(M)):
		for j in range(len(cent)):
			M[i][j] -= cent[j]
		convert1(M[i])
		M[i] = xMatriks(Mrotate, M[i])
		convert2(M[i])
		for j in range(len(cent)):
			M[i][j] += cent[j]

"""
	op : reflect <param>
	Mencerminkan matriks poligon terhadap <param>
	<param> dapat berupa (a,b), x, y, y=x, y=-x
"""
def reflect(M, op):
	param = op[1]
	
	p = 0; q = 0; r = 0; s = 0
	if param == "x" or param == "y" or param == "y=x" or param == "y=-x":
		if param == "x": 		# terhadap sumbu x
			p = 1; s = -1
		elif param == "y": 		# terhadap sumbu y
			p = -1; s = 1
		elif param == "y=x": 	# terhadap y = x
			q = 1; r = 1
		elif param == "y=-x":	# terhadap y = -x
			q = -1; r = -1
		
		Mrefleksi = [[p, q], [r, s]]
		
		for i in range(len(M)):
			convert1(M[i])
			M[i] = xMatriks(Mrefleksi, M[i])
			convert2(M[i])
		
	else:						# terhadap (a,b)
		param = param[1:]
		param = param [:len(param)-1]
		param = param.split(",")
		a = float(param[0]) / 2.0
		b = float(param[1]) / 2.0
		
		Mrefleksi = [[-1.0,0], [0,-1.0]]
		
		for i in range(len(M)):
			convert1(M[i])
			M[i] = xMatriks(Mrefleksi, M[i])
			convert2(M[i])
			
		for i in range(len(M)):
			M[i][0] += 2*a
			M[i][1] += 2*b

"""
	op : shear <param> <k>
	Membusurkan poligon terhadap <param> dengan skala <k> 
"""
def shear(M, op):
	param = op[1]
	k = float(op[2])
	
	p = 1.0; q = 0; r = 0; s = 1.0
	if param == "x": 	# sumbu x
		q = k
	elif param == "y": 	# sumbu y
		r = k
	Mshear = [[p, q], [r, s]]
	
	for i in range(len(M)):
		convert1(M[i])
		M[i] = xMatriks(Mshear, M[i])
		convert2(M[i])

"""
	op : stretch <param> <k>
	Mengekspansi/mengkompresi pada arah <param> dengan faktor <k>
"""
def stretch(M, op):
	k = float(op[2])
	param = op[1]
	
	p = 0; q = 0; r = 0; s = 0
	if param == "x": # sumbu x
		p = k; s = 1 
	elif param == "y": # sumbu y
		p = 1; s = k
	Mstretch = [[p, q], [r, s]]
	
	for i in range(len(M)):
		convert1(M[i])
		M[i] = xMatriks(Mstretch, M[i])
		convert2(M[i])

"""
	op : custom <a> <b> <c> <d>
	Mentransformasi matriks poligon dengan matriks
		<a> <b>
		<c> <d>
"""
def custom(M, op):
	a = float(op[1])
	b = float(op[2])
	c = float(op[3]) 
	d = float(op[4])
	
	Mcustom = [[a, b], [c, d]]
	
	for i in range(len(M)):
		convert1(M[i])
		M[i] = xMatriks(Mcustom, M[i])
		convert2(M[i])

"""
	input sebelum masuk prosedur multiple:
		multiple <n>
	Mentransformasi matriks poligon sebanyak <n>
	transList adalah list berisi instruksi transformasi
"""
def multiple(vertices, transList):
	for instruction in transList:
		op = instruction.split(" ")
		if op[0] == "translate":
			translate(vertices, op)
		elif op[0] == "dilate":
			dilate(vertices, op)
		elif op[0] == "rotate":
			rotate(vertices, op)
		elif op[0] == "reflect":
			reflect(vertices, op)
		elif op[0] == "shear":
			shear(vertices, op)
		elif op[0] == "stretch":
			stretch(op)
		elif op[0] == "custom":
			custom(vertices, op)
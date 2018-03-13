from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import threading, copy, math
import transformasi as trans

# ukuran window
width, height = 500, 500

""" meng-set tampilan dalam bentuk 2D """
def refresh2d(width, height):
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
	glMatrixMode (GL_MODELVIEW)
	glLoadIdentity()

""" memberikan titik-titik yang akan ditampilkan di OpenGL """
def drawShape():
	glBegin(GL_POLYGON)
	for i in range(len(mShow)):
		glVertex2f(mShow[i][0], mShow[i][1])
	glEnd()

""" menggambar garis sumbu x dan y """
def drawXYLines():
	glBegin(GL_LINES)		# garis x
	glVertex2f(0, 250)
	glVertex2f(500, 250)
	glEnd()
	
	glBegin(GL_LINES)		# garis y
	glVertex2f(250, 0)
	glVertex2f(250, 500)
	glEnd()

""" untuk meng-update layar jika ada perubahan titik-titik """
def draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	refresh2d(width, height)
	
	glColor3f(250.0, 250.0, 250.0)
	drawXYLines()
	drawShape()

	glutSwapBuffers()

"""
	Inisialisasi OpenGL dan pengaturan lainnya
	sebelum program grafik ditampilkan
"""
def mainOpenGL():
	glutInit()
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
	glutInitWindowSize(width, height)
	glutCreateWindow(b'Transformasi Poligon')
	glutDisplayFunc(draw)
	glutIdleFunc(draw)
	glutMainLoop()


""" PROGRAM UTAMA """
# N adalah berapa banyak titik pada poligon yang akan ditampilkan
N = int(input())

""" Meng-input titik-titik poligon """
# oriPL adalah matriks yang berisi titik-titik poligon
# yang pertama kali di-input user
oriPL = []
for i in range(N):
	points = input()
	points = points.split(",")
	temp = []
	for p in points:
		temp.append(float(p)/2.0)
	oriPL.append(temp)

# vetrices adalah matriks yang berisi titik-titik hasil transformasi
vertices = []
vertices = copy.deepcopy(oriPL)

# mShow adalah matriks yang berisi titik-titik hasil transformasi yang 
# disesuaikan supaya sesuai di tampilan
mShow = trans.showShape(vertices)

""" Memulai threading untuk program OpenGL """
t = threading.Thread(target=mainOpenGL)
t.daemon = True
t.start()

"""
	Pembacaan perintah
		- transformasi
		- reset matriks
		- keluar dari program
"""
userInput = input()
while userInput != "exit":
	if userInput == "reset":		# mengembalikan poligon transformasi menjadi poligon awal yang diinput user
		vertices = copy.deepcopy(oriPL)
	else:
		op = userInput.split(" ")
		if op[0] == "translate":	# mentranslasi gambar
			trans.translate(vertices, op)
		elif op[0] == "dilate":		# mendilatasi/menkontraksi poligon
			trans.dilate(vertices, op)
		elif op[0] == "rotate":		# merotasi poligon
			trans.rotate(vertices, op)
		elif op[0] == "reflect":	# mencerminkan poligon
			trans.reflect(vertices, op)
		elif op[0] == "shear":		# membusurkan poligon
			trans.shear(vertices, op)
		elif op[0] == "stretch":	# mengekspansi/menkontraksi poligon
			trans.stretch(vertices, op)
		elif op[0] == "custom":		# mentransformasi poligon berdasarkan matriks 2*2 dari user
			trans.custom(vertices, op)
		elif op[0] == "multiple":	# mentransformasi poligon beberapa kali
			n = int(op[1])
			transList = []
			for times in range(n):
				inputMulti = input()
				transList.append(inputMulti)
			trans.multiple(vertices, transList)
	# meng-update titik-titik poligon yang akan ditampilkan di layar
	mShow = trans.showShape(vertices)
	# input perintah/transformasi selanjutnya
	userInput = input()
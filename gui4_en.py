# correrlo con el python del systema por los codecs

import os, sys, time, json
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl,QRect

M,N = 17, 10 

class Gui(QWidget):

	def __init__(self):
		
		super().__init__()
		
		self.arx= '.test'
		
		self.setGeometry(0,0,1200, 600)
		
		# main window
		self.MainWindow = QMainWindow()
		self.centralwidget = QWidget(self.MainWindow)
		self.MainWindow.setCentralWidget(self.centralwidget)

		# reproductor
		self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
		videowidget = QVideoWidget()
		#videowidget.setFixedWidth(750)
		
		self.mediaPlayer.setVideoOutput(videowidget)
		
		openBtn = QPushButton('Load Video')
		openBtn.clicked.connect(self.open_file)
		
		
		# para busqueda en tiempo
		self.Tsearch = QLineEdit()
		self.Tsearch.setFixedWidth(100)
		TsearchBtn = QPushButton('go t')
		TsearchBtn.setFixedWidth(100)
		TsearchBtn.clicked.connect(self.go_t)
		
		h0= QHBoxLayout()
		h0.addWidget(openBtn)
		h0.addWidget(self.Tsearch)
		h0.addWidget(TsearchBtn)
		
		
		# Layout 1 --------------------------------
		vboxLayout1 = QVBoxLayout()
		vboxLayout1.addWidget(videowidget)
		
		
		#vboxLayout1.addWidget(openBtn)
		vboxLayout1.addLayout(h0)
		
		
				
	
		# Layout 2 ------------------------------
		vboxLayout2 = QVBoxLayout()
		
	
		# equipos
		self.equipo1 = QLineEdit()
		self.equipo1.setFixedWidth(200)
		self.equipo1.setText('<- Team 1')
		
		self.equipo2 = QLineEdit()
		self.equipo2.setFixedWidth(200)
		self.equipo2.setText('Team 2->')
		
		h1= QHBoxLayout()
		h1.addWidget(self.equipo1)
		h1.addWidget(self.equipo2)
		
		vboxLayout2.addLayout(h1)
		
		
		# boton comenzar rally
		inicioRallyBtn = QPushButton('Start Rally')
		inicioRallyBtn.clicked.connect(self.inicioRally)
		vboxLayout2.addWidget(inicioRallyBtn)
		
		# info text
		info1 = QLabel()
		info1.setText('REC at the place where the event occurs: [PlayerId]<space>[eventType]\nService : 0-jump, 1-jump float, 2-float, 3-Other\nHits: 11-pass, 12-set, 13-attack, 14-touch, 15-block, 16-other') 
				
		info1.setFixedHeight(50)		
		vboxLayout2.addWidget(info1)
		
		# grid
		self.grid = QGridLayout()
		self.grid.setSpacing(0.01)
		vboxLayout2.addLayout(self.grid)
		
		self.C = [
			[1,0, 1,1,1,1,1,1,0,1,1,1,1,1,1, 0,1],
			[0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0],
			[1,0, 1,1,1,1,1,1,0,1,1,1,1,1,1, 0,1],
			[1,0, 1,1,1,1,1,1,0,1,1,1,1,1,1, 0,1],
			[1,0, 1,1,1,1,1,1,0,1,1,1,1,1,1, 0,1],
			[1,0, 1,1,1,1,1,1,0,1,1,1,1,1,1, 0,1],
			[1,0, 1,1,1,1,1,1,0,1,1,1,1,1,1, 0,1],
			[1,0, 1,1,1,1,1,1,0,1,1,1,1,1,1, 0,1],
			[0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0],
			[1,0, 1,1,1,1,1,1,0,1,1,1,1,1,1, 0,1],		
		]
		
		
		
		for i in range(N):
			for j in range(M):
				
				if self.C[i][j]==1:
					entry = QLineEdit()
					entry.setEnabled(False)
					entry.setMaximumWidth(30)
					entry.setMaximumHeight(30)
					self.grid.addWidget(entry, i,j)
					
				else:
					self.grid.addWidget(entry, i,j)
		
		# boton cargar evento
		self.cargarEventoBtn = QPushButton('Load event')
		self.cargarEventoBtn.clicked.connect(self.cargarEvento)
		self.cargarEventoBtn.setEnabled(False)
		vboxLayout2.addWidget(self.cargarEventoBtn)
		
		# remover ultimo evento cargado 
		self.removerEventoBtn = QPushButton('Remove last event')
		self.removerEventoBtn.clicked.connect(self.removerEvento)
		self.removerEventoBtn.setEnabled(False)
		vboxLayout2.addWidget(self.removerEventoBtn)
		
		# info 2
		info2 = QLabel()
		info2.setText('REC Finish: [TeamId]<space>[FinalEventType]\nUse : 21- ball in, 22-ball out, 23-hands and out, 24-cannot control, 25-infraction,\n26-other') 
		info2.setFixedHeight(50)		
		vboxLayout2.addWidget(info2)
		
		# fin
		
		self.fin = QLineEdit()
		self.fin.setEnabled(False)
		vboxLayout2.addWidget(self.fin)
		
		# boton fin rally
		self.finRallyBtn = QPushButton('End Rally')
		self.finRallyBtn.clicked.connect(self.finRally)
		self.finRallyBtn.setEnabled(False)
		vboxLayout2.addWidget(self.finRallyBtn)
		
		# main layout
		mainLayout = QHBoxLayout()
		mainLayout.addLayout(vboxLayout1)
		mainLayout.addLayout(vboxLayout2)
		self.setLayout(mainLayout)
		
		
	
	
	
	def inicioRally(self):
		
		for i in range(N):
			for j in range(M):
				
				if self.C[i][j]==1:
					entry = self.grid.itemAtPosition(i,j).widget()
					entry.setEnabled(True)
					entry.setText('')
		
		
		self.cargarEventoBtn.setEnabled(True)
		
		t0 = self.mediaPlayer.position()
		
		self.newRally = {'t0':t0, 'events':[], 'eq1':self.equipo1.text(), 'eq2':self.equipo2.text()}
	
	
	
	def cargarEvento(self):
		
		for i in range(N):
			for j in range(M):
				
				if self.C[i][j]==1:
					entry = self.grid.itemAtPosition(i,j).widget()
					
					txt = entry.text()
					if txt!='':
						t = self.mediaPlayer.position()
						
						self.newRally['events'].append([t, i, j,txt] )
					
						print (self.newRally['events'][-1])
						
						entry.setText('')
		
		
		
		self.fin.setEnabled(True)
		self.finRallyBtn.setEnabled(True)
		self.removerEventoBtn.setEnabled(True)
	
	
	
	def removerEvento(self):
		self.newRally['events'].pop()
		
		
		
	
	
	def finRally(self):
				
		t = self.mediaPlayer.position()
		
		txt = self.fin.text()
		
		self.fin.setText('')
		
		self.newRally['events'].append([t, txt])
		
		# save data
		js = json.dumps(self.newRally)
		f = open(self.arx,"a")
		f.write(js)
		f.write('\n')
		f.close()
		
		
		
		print ('\n')
		#print (self.newRally)
		
		
		self.fin.setEnabled(False)
		self.finRallyBtn.setEnabled(False)
		
		for i in range(N):
			for j in range(M):
				
				if self.C[i][j]==1:
					entry = self.grid.itemAtPosition(i,j).widget()
					entry.setEnabled(False)

		
		
		
		
		
		
		
	
	
	
	

	def open_file(self):
		
		filename, _ = QFileDialog.getOpenFileName(self, "Load Video")
		
		if filename!= '':
			self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
			
			self.arx = "data/%s_%d.dat" % (filename.split('/')[-1], time.time())
			
			print ('[Arx salida] : %s' %self.arx)
			
			

	
	def keyPressEvent(self, event):
		key = event.text()
		
		
		if key=='s':
			
			#print (self.mediaPlayer.state())
			
			if self.mediaPlayer.state() ==1:
				self.mediaPlayer.pause()
			else:
				self.mediaPlayer.play()
				

		# adelantando 
		elif key=='d':
			pos = self.mediaPlayer.position()
			self.mediaPlayer.setPosition(pos+2000)
		
		elif key=='a':
			pos = self.mediaPlayer.position()
			if pos>2000:
				self.mediaPlayer.setPosition(pos-2000)
		
		
		elif key=='c':
			pos = self.mediaPlayer.position()
			self.mediaPlayer.setPosition(pos+60000)
		
		elif key=='z':
			pos = self.mediaPlayer.position()
			if pos>60000:
				self.mediaPlayer.setPosition(pos-60000)

		
		
		elif key=='e':
			pos = self.mediaPlayer.position()
			self.mediaPlayer.setPosition(pos+30)
		
		elif key=='q':
			pos = self.mediaPlayer.position()
			if pos>60000:
				self.mediaPlayer.setPosition(pos-30)



	def go_t(self):
		t = int(self.Tsearch.text())
		T = self.mediaPlayer.duration()
		
		if t<T:
			self.mediaPlayer.setPosition(t)
		else:
			print ("El video no es tan largo...")
			print ("Duracion :", T)
			self.mediaPlayer.setPosition(T-5000)



		

	def mousePressEvent(self, event):
		try:
			QApplication.focusWidget().clearFocus()
		except:
			None





if __name__ == '__main__':
	
	
	os.system("clear")
	
	print ('Commands:\n(s)-Play/Pause, (a)- --2 seg, (d)- ++2 seg\n(z)- --1 min, (c)- ++1 min')
	print ('(q) --0.01 seg, (e) ++0.01 seg')
		
	app = QApplication(sys.argv)

	demo = Gui()
	
	demo.show()

	sys.exit(app.exec_())

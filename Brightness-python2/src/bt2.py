#!/usr/bin/python2
import sys
import os
import subprocess
#import math
from PySide import QtCore, QtGui
#from PyQt4 import QtCore, QtGui
class Window(QtGui.QMainWindow):    
	def __init__(self):
		super(Window,self).__init__()
		#setting up the position of the GUI with 1st and 2nd parameters
		#(3rd and 4th parameters are not useful as we have fixed it's max and min size below)
		self.setGeometry(530,290,280,120)
		self.setWindowTitle("Brightness")
		
		self.setMinimumSize(QtCore.QSize(280, 120))
		self.setMaximumSize(QtCore.QSize(280, 120))
		
		#The slider which we slide
		self.slide = QtGui.QSlider(self)
		self.slide.setGeometry(QtCore.QRect(70, 58, 160, 22))
		self.slide.setOrientation(QtCore.Qt.Horizontal)
		self.slide.valueChanged.connect(self.slided_def)
		self.slide.setMaximum(100)
		self.slide.setMinimum(0)
		
		#Just a label to denote what user need to do
		self.adj = QtGui.QLabel(self)
		self.adj.setGeometry(50, 5, 471, 20)
		self.adj.setText("Slide the bar to adjust brightness")

		#creating and adding increment button		
		self.inc = QtGui.QPushButton("+",self)
		self.inc.setGeometry(QtCore.QRect(237, 60, 17, 17))
		self.inc.clicked.connect(self.inc_def)

		#creating and adding increment button
		self.dec = QtGui.QPushButton("-",self)
		self.dec.setGeometry(QtCore.QRect(45, 60, 17, 17))
		self.dec.clicked.connect(self.dec_def)

		#This label shows the black sun with rays! 
		self.bright = QtGui.QLabel(self)
		self.bright.setGeometry(20, 60,20, 20)
		self.bright.setText(u"\u2600")
    
		#This shows the percentage of brightness
		self.percentval = QtGui.QLabel(self)
		self.percentval.setGeometry(35, 35, 471, 20)
		self.percentval.setText("Slide the bar to adjust brightness")
		
		#The set button
		self.set = QtGui.QPushButton("Set",self)
		self.set.setGeometry(QtCore.QRect(20, 90, 120, 23))
		self.set.clicked.connect(self.set_val_def)
		
		#the exit button
		self.exit = QtGui.QPushButton("Exit",self)
		self.exit.setGeometry(QtCore.QRect(144, 90, 120, 23))
		self.exit.clicked.connect(self.close_application)
		
		#we will use this one later for timer(our countdown is 10 but we use 9 because we waste a second on 10)
		self.count = 9
		
		#if such path exists then we change value in that path else exception propogates
		try:
			path = os.path.join("/sys/class/backlight/nv_backlight", "brightness")
			with open(path, "r") as inputFile:
				self.init = inputFile.read()
				self.init1 = int(self.init)
		except IOError:
			try:
				path = os.path.join("/sys/class/backlight/radeon_bl0", "brightness")
				with open(path, "r") as inputFile:
					self.init1 = int(inputFile.read())/26
			except IOError:
				try:
					path = os.path.join("/sys/class/backlight/intel_backlight", "brightness")
					with open(path, "r") as inputFile:
						self.init1 = int(inputFile.read())/75
				except IOError:
#					try:
#						path = os.path.join("/sys/class/backlight/acpi_video0", "brightness")
#						with open(path, "r") as inputFile:
#							self.init1 = int(inputFile.read())
#							self.slide.setMaximum(15)
#							self.slide.setMinimum(0)
#					except IOError:
					try:
						#if searched documents are not present we use xrandr for changing brightness
						a = float(readx())*100
						self.init1 = int(a)
					except Exception:
						choice = QtGui.QMessageBox.warning(self,'Caution!',"We are not supporting your display drivers as of now.\nSorry:(",QtGui.QMessageBox.Cancel)
						if choice == QtGui.QMessageBox.Cancel:
							sys.exit()
						else:
							pass

		self.slide.setValue(int(self.init1))
		
		#uncomment the below 6 lines if you want :)
		#self.setGeometry(530,290,160,22)
		#self.setMinimumSize(QtCore.QSize(280, 150))
		#self.setMaximumSize(QtCore.QSize(280, 150))
		#self.india = QtGui.QLabel(self)
		#self.india.setGeometry(65   , 120, 471, 20)
		#self.india.setText(" Made with  "+ u"\u2764"+"  in INDIA")
		
		#check if the user is running as root
		if not os.geteuid() == 0:
			choice = QtGui.QMessageBox.warning(self,'Sorry',"Only root can run this script!\n",QtGui.QMessageBox.Close)
			if choice == QtGui.QMessageBox.Close:
				sys.exit(1)
			else:
				pass
		
		
		
		#show all the above content in the dialog box	
		self.show()

	#used with '+' to increment 1 unit
	def inc_def(self):
		tmp1 = self.slide.value()    
		self.slide.setValue(int(tmp1)+1)
		
		
	#used with '-' to decrement 1 unit	
	def dec_def(self):
		tmp1 = self.slide.value()    
		self.slide.setValue(int(tmp1)-1) 


	#just close the application
	def close_application(self):        
		sys.exit(1)

		
	#changimg value on slider on startup and on setting
	def slided_def(self):
		#for acpi_video0,we are checking for percent which has only 0-15 values
		val = self.slide.value()
		#if os.path.isdir("/sys/class/backlight/acpi_video0"):
		#	val = int(val*6.66)+1
		self.percentval.setText(str(val)+" %")


	#set the brightness
	def set_val_def(self):
		#get the current values before setting the brightness
		try:
			path = os.path.join("/sys/class/backlight/nv_backlight", "brightness")
			with open(path, "r") as inputFile:
				self.prev = inputFile.read()
		except IOError:
			try:
				path = os.path.join("/sys/class/backlight/radeon_bl0", "brightness")
				with open(path, "r") as inputFile:
					self.prev = int(inputFile.read())/26
			except IOError:
				try:
					path = os.path.join("/sys/class/backlight/intel_backlight", "brightness")
					with open(path, "r") as inputFile:
						self.prev = int(inputFile.read())/75
				except IOError:
#					try:
#						path = os.path.join("/sys/class/backlight/acpi_video0", "brightness")
#						with open(path, "r") as inputFile:
#							self.prev = math.ceil(int(inputFile.read())*6.666)
#					except IOError:
					try:
						a = float(readx())*100
						self.prev = int(a)
					except IOError:
						choice = QtGui.QMessageBox.warning(self,'Caution!',"We are not supporting your display drivers as of now.\nSorry :(",QtGui.QMessageBox.Cancel)
						if choice == QtGui.QMessageBox.Cancel:
							sys.exit()
						else:
							pass
    
		val = self.slide.value()
		#if os.path.isdir("/sys/class/backlight/acpi_video0"):
		#	val=int(val*6.666)
		
		#if the setting value is less than 10% then we ask user if they are sure!
		#if they are sure,as a safety check we will wait for 10 seconds and revert back to previous brightness 
		if val<10:
			choice = QtGui.QMessageBox.warning(self,'Caution!',"Are you sure you want to do this?\nIt might not be visible to you!",QtGui.QMessageBox.Yes|          QtGui.QMessageBox.No)
			if choice == QtGui.QMessageBox.Yes:
				self.confirm()
				self.revert()
			else:
				pass
		else:
			try:
				text = str(val)
				path = os.path.join("/sys/class/backlight/nv_backlight", "brightness")
				with open(path, "w") as inputFile:
					inputFile.write(text)
					save("/sys/class/backlight/nv_backlight",text)
			except IOError:
				try:
					text = str(val*26)
					path = os.path.join("/sys/class/backlight/radeon_bl0", "brightness")
					with open(path, "w") as inputFile:
						inputFile.write(text)
						save("/sys/class/backlight/radeon_bl0",text)
				except IOError:
					try:
						text = str(val*75)
						path = os.path.join("/sys/class/backlight/intel_backlight", "brightness")
						with open(path, "w") as inputFile:
							inputFile.write(text)
							save("/sys/class/backlight/intel_backlight",text)
					except IOError:
#						try:
#							text = str(int(math.ceil(val/6.666)))
#							path = os.path.join("/sys/class/backlight/acpi_video0", "brightness")
#							with open(path, "w") as inputFile:
#								inputFile.write(text)
#								save("/sys/class/backlight/acpi_video0",text)
#						except IOError:
						try:
							text = int(val)
							writex(text)
						except IOError:
							sys.exit(1)
                    	
	#we are creating a message box asking them to click 'Cancel' if they want to revert
	def revert(self):
		self.startCount()
		self.msg = QtGui.QMessageBox(self)
		self.msg.setText("Reverting in (10)")
		self.msg.setInformativeText("Click cancel to stop reverting.")
		self.msg.setWindowTitle("Reverting..")
		self.msg.setIcon(QtGui.QMessageBox.Warning)
		self.msg.setStandardButtons(QtGui.QMessageBox.Cancel)
		self.msg.buttonClicked.connect(self.win_cancel) 	
		self.msg.open() # displaying the message box
	
	#if the user clicks on cancel,this will be executed
	def win_cancel(self):
		self.timer.stop() #stopping the timer
		self.msg.done(1) #closing the message box
		self.count = 9 #again setting up count for future use

	#starts the countdown
	def startCount(self):
		self.timer = QtCore.QTimer()  # set up your QTimer
		self.timer.timeout.connect(self.updateButtonCount)  # connect it to your update function each second
		self.timer.start(1000) #1000 milliseconds = 1 second(interval between the counts) 

	def updateButtonCount(self):
		#That messsage box will be displayed until count is 0(10 seconds)
		if self.count > 0:
			self.msg.setText("Reverting in (%s)"%self.count)
			self.count-=1
		
		#if the count is 0(completion of 10 seconds) then fix the brightness value 
		else:
			self.timer.stop()
			self.msg.done(1)
			self.slide.setValue(int(self.prev))
			try:
				text = str(self.prev)
				path = os.path.join("/sys/class/backlight/nv_backlight", "brightness")
				with open(path, "w") as inputFile:
					inputFile.write(text)
					save("/sys/class/backlight/nv_backlight",text)
			except IOError:
				try:
					text = str(self.prev*26)
					path = os.path.join("/sys/class/backlight/radeon_bl0", "brightness")
					with open(path, "w") as inputFile:
						inputFile.write(text)
						save("/sys/class/backlight/radeon_bl0_backlight",text)
				except IOError:
					try:
						text = str(self.prev*75)
						path = os.path.join("/sys/class/backlight/intel_backlight", "brightness")
						with open(path, "w") as inputFile:
							inputFile.write(text)
							save("/sys/class/backlight/intel_backlight",text)
					except IOError:
#						try:
#							text = str(int(int(self.prev)/6.6))
#							path = os.path.join("/sys/class/backlight/acpi_video0", "brightness")
#							with open(path, "w") as inputFile:
#								inputFile.write(text)
#								save("/sys/class/backlight/acpi_video0",text)		
#						except IOError:
						try:
							text = int(self.prev)
							writex(text)
						except IOError:
							sys.exit(1)
			self.count =9 #again setting up count for future use
		
		
	#this will actually set the brightness
	def confirm(self):
		val = self.slide.value()
		text = str(val)
		try:
			path = os.path.join("/sys/class/backlight/nv_backlight", "brightness")
			with open(path, "w") as inputFile:
				inputFile.write(text)
				save("/sys/class/backlight/nv_backlight",text)
		except IOError:
			try:
				path = os.path.join("/sys/class/backlight/radeon_bl0", "brightness")
				with open(path, "w") as inputFile:
					inputFile.write(text)
					save("/sys/class/backlight/radeon_bl0",text)
			except IOError:
				try:
					path = os.path.join("/sys/class/backlight/intel_backlight", "brightness")
					with open(path, "w") as inputFile:
						inputFile.write(text)
						save("/sys/class/backlight/intel_backlight",text)
				except IOError:
#					try:
#						path = os.path.join("/sys/class/backlight/acpi_video0", "brightness")
#						with open(path, "w") as inputFile:
#							inputFile.write(text)
#							save("/sys/class/backlight/acpi_video0",text)
#					except IOError:
					try:
						writex(int(text))
					except IOError:
						sys.exit(1)


#By using xrandr(if searched documents are not present we use xrandr),we set the brightness here    
def writex(text):
	op = subprocess.check_output(['xrandr','-q'])

	encoding = sys.getdefaultencoding()
	decode = op.decode(encoding)
	decode = decode.split('\n')
	decode = " ".join(decode)

	dl = decode.split(' ')

	con_list = []

	length = len(dl)
	conn_list = []
	for i in range(length):
		if dl[i] == 'connected':
			conn_list.append(i-1)
	
	#ending \n
	conn_dev = []
	
	for each in conn_list:
		conn_dev.append(dl[each])

	cmd_list = []



	for dev in conn_dev:
		cmd_list.append('xrandr --output '+dev+' --brightness ')

	bt = (text/100.0)
	bt_str = str(bt)
	new_cmd = []
	for each in cmd_list:
		new_cmd.append(each+bt_str)
	for each in new_cmd:
		os.system(each)
	savex(new_cmd[0])


#getting the current brightness using xrandr	
def readx():
	op = subprocess.check_output("xrandr --verbose | grep -i brightness | cut -f2 -d ' '",shell = True)
	encoding = sys.getdefaultencoding()
	decode = op.decode(encoding)
	decode = decode.split('\n')
	decode = " ".join(decode)
	bl = decode.split(' ')
	return(str(bl[0]))
	
	
#remembering the brightness to adjust brightness when rebooted(may not work in some systems due to system or other startup applications)
#needs to be updated!	
def savex(cmd):	
	users = os.listdir("/home")
	for user in users:
		filepath =  "/home/"+user+"/.config/autostart"
		fileloc = filepath+"/xbrightness.desktop"
		if not os.path.exists(filepath):
			os.makedirs(filepath)
		with open(fileloc,'w') as save:
			save.write("""[Desktop Entry]
Name=Brightness for xrandr
Exec="""+cmd+"""
Type=Application
		""")


#(while not using xrandr)adding the job to crontab of executing a python script on every reboot 
def save(floc,percent):
	try:
		op = subprocess.check_output("sudo crontab -l",shell = True)
		encoding = sys.getdefaultencoding()
		decode = op.decode(encoding)
		if "@reboot python /bin/init_bt.py &" not in decode:
			os.system("(sudo crontab -l 2>/dev/null; echo \"@reboot python /bin/init_bt.py &\")| crontab -")
	except subprocess.CalledProcessError as e:
		os.system("(sudo crontab -l 2>/dev/null; echo \"@reboot python /bin/init_bt.py &\")| crontab -")
	cmd = "echo "+str(percent)+" > "+floc+"/brightness"
	with open("/bin/init_bt.py",'w') as save:
		save.write("""#!/usr/bin/python
import os;
class save_bt:
	def __init__(self):
		os.system(cmd)
		
cmd = \""""+cmd+"""\"
save_bt()""")
	os.system("chmod +x /bin/init_bt.py")
	

#Finally this invokes the applications
def run():
    app=QtGui.QApplication(sys.argv)
    QtGui.QApplication.setStyle('cleanlooks') #you can change it to any style you wish(according to my personal opinion is,this looks better)
    GUI= Window()
    sys.exit(app.exec_())


run()

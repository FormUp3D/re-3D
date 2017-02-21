from tkinter import *
from tkinter import filedialog
import serial
import os

class Application (Frame):

	def __init__(self, master):
		Frame.__init__(self, master)
		self.grid()
		self.place(x=0, y=0)
		self.create_widgets()
		self.BAUD = 250000
		self.COM = 0
		
	def get_COM_List(self):
		self.COM_List = [];

		for x in range(0, 30):
			self.COM = x
			try:
				self.ser = serial.Serial(port=self.COM)
				if self.ser.isOpen:
					self.COM_List.append("COM" + str(x+1))
				self.ser.close()
			except serial.serialutil.SerialException:
				pass

		return tuple(self.COM_List)

	def create_widgets(self):
	
		#Embed and image into the GUI
		self.can = Canvas(bg="#F0F0ED", width=250, height=200)
		self.pic = PhotoImage(file='main-logo-dark-re3d.png')
		self.item = self.can.create_image(80, 80, image=self.pic)
		self.can.pack(side = TOP)
		self.can.grid()
		self.can.place(x=-25, y=100)
		
		#Create the upload button
		self.upload_button = Button(self)
		self.upload_button["text"] = "Upload"
		self.upload_button ["command"] = self.upload
		self.upload_button.grid(row=6, column=4, columnspan=1, sticky=S)
		self.upload_button.config(state="disabled")
		
		#Create label for baudrates
		Label(self, text="Baudrate").grid(row = 2, column = 3)
		
		#Create BAUDRATE option box
		BAUD_list = ("9600", "19200", "38400", "57600", "115200", "250000")
		self.v = StringVar()
		self.v.set(BAUD_list[5])
		self.BAUD_options = OptionMenu(self, self.v,*BAUD_list, command = self.setBAUD)
		self.BAUD_options.grid(row=2, column=4, columnspan=1, sticky=W)
		
		#create label for COM port selections
		Label(self, text="Com Port").grid(row = 3, column = 3)
		
		#Create COMPORT option box
		COM_list = self.get_COM_List()  #("COM1", "COM2")
		self.g = StringVar()
		self.g.set(COM_list[0])
		self.COMPORT_options = OptionMenu(self, self.g,*COM_list, command = self.setCOM)
		self.COMPORT_options.grid(row=3, column=4, columnspan=1, sticky=W)
		
		#create browse button
		self.button = Button(self)
		self.button["text"] = "Browse"
		self.button["command"] = self.browseFiles
		self.button.grid(row=0, column=3, columnspan=1)
		self.button.place()
						
		#create text block
		self.TEXT = ""
		self.T = Text(self, height=1, width=50)
		self.T.grid(row=0, column=4, columnspan=1, rowspan=1)
		self.T.insert(END, self.TEXT)
		self.T.config(state=DISABLED)
		
	def setCOM(self, value):
		num = int(value.replace('COM', ''))
		self.COM = num-1

	def setBAUD(self, value):
		self.BAUD = int(value)

	def browseFiles(self):
		Frame.fileName = filedialog.askopenfilename(filetypes = (("Binary files", "*.bin"), ("All files", "*.*")))
		self.file = open(Frame.fileName, 'r')	
		self.T.config(state=NORMAL)
		self.T.delete("0.0", END)
		self.T.insert("0.0", Frame.fileName)
		self.upload_button.config(state="normal")
		self.T.config(state=DISABLED)
		
	def setText(self):
		self.TEXT = self.file.read()
		
	def upload(self):
		#self.ser = serial.Serial(port=self.COM, baudrate=self.BAUD, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
		
		#with open(Frame.fileName, 'rb') as myfile:
		#	bytes = myfile.read(1024)
		#	while bytes:
		#		self.ser.write(bytes)
		#		bytes = myfile.read(1024)
			
		#self.ser.close()
		os_text = "avrdude.exe -Cavrdude.conf -q -q -patmega2560 -cwiring -PCOM" + str(self.COM+1) + " -b115200 -D \"-Uflash:w:" + Frame.fileName + ":i\""
		print(os_text)
		os.system(os_text)

root = Tk()	

#modify root window
root.title("3D Firmware Flash")
root.geometry("500x300")

#disabled resizing of window
root.resizable(0,0)

app = Application(root)

root.mainloop()
from tkinter import *
from tkinter import filedialog
from tkinter import font
import json
from os import listdir
from os.path import isfile, join
from functools import partial
from lab8 import send_email
from lab8 import check_verification_code

root = Tk()
root.title('CS Lab')
root.geometry('1200x660')

is_email_confirmed = 0

passcode = StringVar()

# Create New File Function
def new_file():
	# Delete previous text
	my_text.delete('1.0', END)
	
	# Update status bars 
	root.title('New File')
	status_bar.config(text = 'New File       ')


def connect():
	global passcode
	global is_email_confirmed

	def validatePasscode_1(pass_code):
		global passcode
		global is_email_confirmed

		check = check_verification_code(passcode, pass_code.get())

		if check:
			is_email_confirmed = 2
		else:
			is_email_confirmed = 0

		print(is_email_confirmed)
		pass_window.destroy()


	def validateEmail(email):

		def validatePasscode(pass_code):
			global passcode
			global is_email_confirmed

			check = check_verification_code(passcode, pass_code.get())

			if check:
				is_email_confirmed = 2
			else:
				is_email_confirmed = 0

			print(is_email_confirmed)
			pass_window.destroy()

		global passcode
		global is_email_confirmed


		is_email_confirmed = 1
		passcode = send_email(email.get())

		connect_window.destroy()

		pass_window = Tk()
		pass_window.title('Email Confirmation')

		pass_label = Label(pass_window, text = 'Code:').grid(row = 0, column = 0)
		pass_code = StringVar(pass_window)
		pass_entry = Entry(pass_window, textvariable = pass_code, width = 50).grid(row = 0, column = 1)

		validatePasscode = partial(validatePasscode, pass_code)

		submit = Button(pass_window, text = 'Submit' ,command = validatePasscode).grid(row = 2, column = 0)
	
		pass_window.mainloop()


	if is_email_confirmed == 0:
	
		connect_window = Tk()
		connect_window.title('Email Confirmation')

		email_label = Label(connect_window, text = 'Email:').grid(row = 0, column = 0)
		email = StringVar(connect_window)
		email_entry = Entry(connect_window, textvariable = email, width = 50).grid(row = 0, column = 1)

		validateEmail = partial(validateEmail, email)

		submit = Button(connect_window, text = 'Submit' ,command = validateEmail).grid(row = 2, column = 0)
	
		connect_window.mainloop()

	elif is_email_confirmed == 1:

		pass_window = Tk()
		pass_window.title('Email Confirmation')

		pass_label = Label(pass_window, text = 'Code:').grid(row = 0, column = 0)
		pass_code = StringVar(pass_window)
		pass_entry = Entry(pass_window, textvariable = pass_code, width = 50).grid(row = 0, column = 1)

		validatePasscode_1 = partial(validatePasscode_1, pass_code)

		submit = Button(pass_window, text = 'Submit' ,command = validatePasscode_1).grid(row = 2, column = 0)
	
		pass_window.mainloop()

		
def check_status():

	global is_email_confirmed

	if is_email_confirmed == 0:
		my_text.delete('1.0', END)
		my_text.insert(END, 'The email is not confirmed!')

	elif is_email_confirmed == 1:
		my_text.delete('1.0', END)
		my_text.insert(END, 'The email is pending!')
	
	elif is_email_confirmed == 2:
		my_text.delete('1.0', END)
		my_text.insert(END, 'The email is confirmed!')


# Create Main Frame
my_frame = Frame(root)
my_frame.pack(pady = 5)

# Create out Scollbar For the Text Box
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side = RIGHT, fill = Y)

# Create Text Box
my_text = Text(my_frame, width = 97, height = 25,
			 font = ('Helvetica', 16), selectbackground = 'yellow',
			 selectforeground = 'black', undo = True,
			 yscrollcommand = text_scroll.set)
my_text.pack()

# Configure out Scrollbar
text_scroll.config(command = my_text.yview)

# Create Menu
my_menu = Menu(root)
root.config(menu = my_menu)

# Add File Menu
file_menu = Menu(my_menu, tearoff = False)
my_menu.add_cascade(label = 'File', menu = file_menu)
file_menu.add_command(label = 'New', command = new_file)
file_menu.add_command(label = 'Confirm email', command = connect)
file_menu.add_command(label = 'Check email status', command = check_status)
file_menu.add_separator()
file_menu.add_command(label = 'Exit', command = root.quit)

# Add Status Bar to Bottom
status_bar = Label(root, text = 'Ready     ', anchor = E)
status_bar.pack(fill = X, side = BOTTOM, ipady = 5)
root.mainloop()
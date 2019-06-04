import json,os,sys
import requests,socket,logging,threading
from tkinter import *
import time
from datetime import datetime
import re

# Define variables and configure log settings
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
LOGNAME = "{}.log".format(__file__.split('.')[0])
logging.basicConfig(filename=LOGNAME, level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
DIR=os.getcwd()
DIR_PIS = os.path.join(os.getcwd(),'PIS_INFO')
headers={'Content-Type': 'application/json'}
HOST='0.0.0.0'
PORT=8887

# activation send for PIS
def act_send(DEV_ID,HSM_ID,ACT_MSG):
	ttc_host_input = ttc_host.get()
	ttc_port_input = ttc_port.get()
	FILE=os.path.join(DIR,'activation_default.json')
	URL='/management/activation/serializationIds/chipID-{}'.format(DEV_ID)
	with open (FILE,'r') as f:
		F=f.read()
	# json --> dict
	D=json.loads(s=F)	
	D['deviceData']['activationMsg'] = ACT_MSG
	F = json.dumps(D)
	try:
		#print ("http://{}:{}{}".format(ttc_host_input,ttc_port_input,URL))
		r = requests.put("http://{}:{}{}".format(ttc_host_input,ttc_port_input,URL), data = F, headers = headers)		
		if r.status_code == 200:
			print("Successfully sent activation request from PIS for {} to TTC, return: {} OK".format(DEV_ID,r.status_code))
			logging.info("Successfully sent activation request from PIS for {} to TTC, return: {} OK".format(DEV_ID,r.status_code))
			#print("Successfully sent request to TTC, return: {} OK".format(r.status_code))
		else:
			print("Failed to send activation request from PIS for {} to TTC, return: Error {}".format(DEV_ID,r.status_code))
			logging.error("Failed to send activation request from PIS for {} to TTC, return: Error {}".format(DEV_ID,r.status_code))
			#print("Failed to send request to TTC, return: Error {}, exit...".format(r.status_code))
	except requests.exceptions.RequestException as e:
		print('Failed to send activation request from PIS to TTC : ' +str(e) + '.')
		logging.error('Failed to send activation request from PIS to TTC : ' +str(e) + '.')





# PIS configuration required
def tcp_start():

	## Create a socket
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	##binding the host and port with the socket
	s.bind((HOST,PORT))

	##make the socket to listening mode
	s.listen(5)

	print("Socket now listening to {}:{}".format(HOST,PORT))
	logging.info("TCP Server now started, Socket now listening to {}:{}".format(HOST,PORT))

	while True:
		conn,addr=s.accept()
		print("Connected with {}".format(addr))
		logging.info("Connected with {}".format(addr))	
		while True:
			#ready=select.select([s],[],[],2)
			#if ready[0]:
			data=conn.recv(4096)
			if not data.hex().strip():
				print('{} connection disconnected'.format(addr))
				logging.info('{} connection disconnected'.format(addr))
				break
			STR='{}'.format(data.hex())
			# value = [DEV_ID，HSM_ID，ACT_MSG]
			DEV_ID = STR[8:-8][12:28].upper()
			HSM_ID = STR[8:-8][28:44].upper()
			ACT_MSG = STR[8:-8][86:].upper()

			if not os.path.exists(DIR_PIS):
				os.makedirs(DIR_PIS)
				logging.info("PATH {} has been created".format(DIR_PIS))
			FILE_PIS = os.path.join(DIR_PIS,"{}_pis.txt".format(DEV_ID))
			try:
				if not os.path.exists(FILE_PIS):
					with open(FILE_PIS, 'w') as f:
						f.write("{},{},{}".format(DEV_ID,HSM_ID,ACT_MSG))
					print('{} has been created.'.format(FILE_PIS))
					logging.info('{} has been created.'.format(FILE_PIS))
				else:
					with open(FILE_PIS, 'w') as f:
						f.write("{},{},{}".format(DEV_ID,HSM_ID,ACT_MSG))
					print('{} has been updated.'.format(FILE_PIS))				
					logging.info('{} has been updated.'.format(FILE_PIS))
				act_send(DEV_ID, HSM_ID, ACT_MSG)				
			except Exception as e:
				print(e)
				logging.error(e)
				break
			return_value = bytes.fromhex('deadbeef')
			#value=bytes(value,encoding='utf-8')
			conn.send(return_value)		
			#else:
				#STR='Timeout'
		conn.close()
	s.close()



def tk_start():
	ttc_host_input = ttc_host.get()
	ttc_port_input = ttc_port.get()
	cmd_input = v.get()
	device_input = DEVICE.get().upper()
	HSM_input = HSM.get().upper()
	bouquet_input = bouquet.get()
	ZIPCODE_input = ZIPCODE.get()
	SRV_ID_input=re.sub(r'\s+','',SRV_ID.get())	
	SRV_ID_input = SRV_ID_input.split(',')
	services=[]
	DISTANCE_input = DISTANCE.get()
	LATITUDE_input = LATITUDE.get()
	LONGOTUDE_input = LONGOTUDE.get()
	BITMAP_b_input = BITMAP.get()
	BITMAP_input = '0{}00000000000000000000000000000000000000000000000000000000000000'.format(BITMAP_b_input)
	#配置URL和json文件
	if cmd_input == 1: # Create
		FILE=os.path.join(DIR,'activation_update.json')
		URL='/management/activation/serializationIds/chipID-{}'.format(device_input)
#		print("Sending device <{}> activation request to {}:{}".format(device,ttc_host,ttc_port))
		Label(master,text="{}: Sending device <{}> activation request to {}:{}".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),device_input,ttc_host_input,ttc_port_input)).grid(row=22, columnspan=2, sticky=W, pady=4)

	elif cmd_input == 2: #update
		FILE=os.path.join(DIR,'activation_update.json')
		URL='/management/updatedevice/serializationIds/chipID-{}'.format(device_input)				
		Label(master,text="{}: Sending device <{}> update request to {}:{}".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),device_input,ttc_host_input,ttc_port_input)).grid(row=22, columnspan=2, sticky=W, pady=4)


	elif cmd_input == 3: # delete
		FILE=os.path.join(DIR,'deactivation.json')
		URL='/management/deactivation/serializationIds/chipID-{}'.format(device_input)
#		print("Sending device <{}> De-activation request to {}:{}".format(device_input,ttc_host_input,ttc_port_input))
		Label(master,text="{}: Sending device <{}> De-activation request to {}:{}".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),device_input,ttc_host_input,ttc_port_input)).grid(row=22, columnspan=2, sticky=W, pady=4)


	elif cmd_input == 4 or cmd_input == 5: # OSD send and removal
		FILE=os.path.join(DIR,'osdsend.json')
		URL='/messaging/messageId/msg-osd-001'
		if cmd_input == 4:
		#print("Sending device <{}> OSD send request to {}:{}".format(device_input,ttc_host_input,ttc_port_input))
			Label(master,text="{}: Sending OSD send request to {}:{}".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),ttc_host_input,ttc_port_input)).grid(row=22, columnspan=2, sticky=W, pady=4)
		else:
		#print("Sending device <{}> OSD send request to {}:{}".format(device_input,ttc_host_input,ttc_port_input))
			Label(master,text="{}: Sending OSD Removal request to {}:{}".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),ttc_host_input,ttc_port_input)).grid(row=22, columnspan=2, sticky=W, pady=4)

	elif cmd_input == 6 or cmd_input == 7: #  发送指纹 and 删除指纹
		FILE=os.path.join(DIR,'fingerprint.json')
		URL='/messaging/messageId/msg-fp-001'
		if cmd_input == 6:
			#print("Sending device <{}> OSD send request to {}:{}".format(device_input,ttc_host_input,ttc_port_input))
			Label(master,text="{}: Sending Fingerprint send request to {}:{}".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),ttc_host_input,ttc_port_input)).grid(row=22, columnspan=2, sticky=W, pady=4)
		else:
			Label(master,text="{}: Sending Fingerprint Removal request to {}:{}".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),ttc_host_input,ttc_port_input)).grid(row=22, columnspan=2, sticky=W, pady=4)			

	elif cmd_input == 8 or cmd_input == 9 or cmd_input ==10: #  发送和删除应急广播
		FILE=os.path.join(DIR,'emmergency.json')
		URL='/messaging/messageId/msg-emb-001'
		if cmd_input == 8 or cmd_input ==9:
			Label(master,text="{}: Sending Emergency Broadcast send request to {}:{}".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),ttc_host_input,ttc_port_input)).grid(row=22, columnspan=2, sticky=W, pady=4)
		else:
			Label(master,text="{}: Sending Emergency Broadcast Removal request to {}:{}".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),ttc_host_input,ttc_port_input)).grid(row=22, columnspan=2, sticky=W, pady=4)			

	else:
		print("wrong command: {}, exit..".format(cmd_input))
		exit()
	##处理http删除
	if cmd_input == 5 or cmd_input == 7: #OSD， 指纹的删除, 
		try:
			r = requests.delete("http://{}:{}{}".format(ttc_host_input,ttc_port_input,URL))
			if r.status_code == 200:
				#print("{} Successfully sent request to TTC, return: {} OK".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),r.status_code))
				Label(master,text="{}: Successfully sent request to TTC, return: {} OK".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),r.status_code)).grid(row=23, columnspan=2, sticky=W, pady=4)
			else:
				#print("Failed to send request to TTC, return: Error {}, exit...".format(r.status_code))
				Label(master,text="{}: Failed to send request to TTC, return: Error {}, exit...".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),r.status_code)).grid(row=23, columnspan=2, sticky=W, pady=4)				
		except requests.exceptions.RequestException as e:
			#print('Failed to send request to TTC : '+str(e) + '. Exit.')
			logging.error('Failed to send request to TTC : '+str(e) + '. Exit.')
			Label(master,text="{}: Failed to send request to TTC, return: Error Something Went Wrong".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))).grid(row=23, columnspan=2, sticky=W, pady=4)				
	#处理http put
	else:
		PIS_FILE = os.path.join(DIR_PIS,"{}_pis.txt".format(device_input))
		#当是激活或者更新的时候，如果没有PIS文件就返回错误
		if not os.path.exists(PIS_FILE) and (cmd_input == 1 or cmd_input == 2):
			Label(master,text="{}: ERROR - Cannot find {} PIS data !!!".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),device_input)).grid(row=23, columnspan=2, sticky=W, pady=4)
			logging.error('Cannot find {} PIS data !!!'.format(device_input))
		##如果是删除device时，没有PIS文件或者没有HSM的输出就返回错误
		elif cmd_input == 3 and not os.path.exists(PIS_FILE) and not HSM_input:
			Label(master,text="{}: ERROR - {} PIS data not found for Delete, Please input HSMID!!!".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),device_input)).grid(row=23, columnspan=2, sticky=W, pady=4)
			logging.error('Cannot find {} PIS data for Delete, Please input HSMID !!!'.format(device_input))
		else:
			##打开json文件，将json文件转成python内容	
			with open (FILE,'r') as f:
				D=json.load(f)
			if cmd_input == 1 or cmd_input == 2:
				#Based on Device ID, get actMSG				
				with open (PIS_FILE,'r') as f:
					MSG=f.read()
				ACT_MSG = MSG.split(',')[-1]
				D['deviceData']['activationMsg'] = ACT_MSG 
				#服务的处理		
				for i in SRV_ID_input:
					services.append({'authorizationElementId': i})
				D['authorizations']['authorizationElements']=services
				#bouquets
				D['bouquet'] = bouquet_input
				#zipcode
				D['zipCode'] = ZIPCODE_input
				#locationDistanceControl
				D['deviceData']['deviceLocation']['locationDistanceControl'] = DISTANCE_input
				# latitude 
				D['deviceData']['deviceLocation']['locationData']['latitude'] = LATITUDE_input
				# longitude 
				D['deviceData']['deviceLocation']['locationData']['longitude'] = LONGOTUDE_input
				# lock
				D['regionBits'][0]['bitmap'] = BITMAP_input
			elif cmd_input == 3:
				#Based on Device ID, get HSM ID
				if HSM_input:
					HSMID_MSG = HSM_input
				else:
					with open (PIS_FILE,'r') as f:
						MSG=f.read()
					HSMID_MSG = MSG.split(',')[1]
				D['deviceData']['deactivationMsg'] = "135912D5B7{}{}0009".format(device_input,HSMID_MSG)
			elif cmd_input == 8: #应急广播发送-音频 跳转音频节目121（TS1)
				D[0]['payload'] ='41095A3F3F3F3F3F3F3F3F450E0100000000000000007900010001'
			elif cmd_input == 9: #跳转视频节目101（TS1)
				D[0]['payload'] = '41095A3F3F3F3F3F3F3F3F450E0100000000000000006500010001'
			elif cmd_input ==10: #应急广播删除
				D[0]['payload'] = '41095A3F3F3F3F3F3F3F3F450E0000000000000000006500010001'
			# dict --> json
			F = json.dumps(D)
			#print(F)
			# Send http requests put
			try:
				#print ("http://{}:{}{}".format(ttc_host_input,ttc_port_input,URL))
				r = requests.put("http://{}:{}{}".format(ttc_host_input,ttc_port_input,URL), data = F, headers = headers)		
				if r.status_code == 200:
					#print("Successfully sent request to TTC, return: {} OK".format(r.status_code))
					Label(master,text="{}: Successfully sent request to TTC, return: {} OK".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),r.status_code)).grid(row=23, columnspan=2, sticky=W, pady=4)
				else:
					#print("Failed to send request to TTC, return: Error {}, exit...".format(r.status_code))
					Label(master,text="{}: Failed to send request to TTC, return: Error {}, exit...".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),r.status_code)).grid(row=23, columnspan=2, sticky=W, pady=4)
			except requests.exceptions.RequestException as e:
				logging.error('Failed to send request to TTC : '+str(e) + '. Exit.')
				Label(master,text="{}: Failed to send request to TTC, return: Error Something Went Wrong...".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))).grid(row=23, columnspan=2, sticky=W, pady=4)


if __name__ == '__main__':
	master = Tk()
	master.title('DCAS PostMan')
	master.minsize(500,200)
	# configure labels
	Label(master, text="TTC地址").grid(row=0,sticky=W)
	Label(master, text="端口").grid(row=1,sticky=W)
	#Label(master, text="CMD").grid(row=2,sticky=W)
	Label(master, text="设备ID").grid(row=2,sticky=W)
	Label(master, text="HSMID(选填)").grid(row=3,sticky=W)
	Label(master, text="BouquetID").grid(row=4,sticky=W)
	Label(master, text="Zipcode").grid(row=5,sticky=W)
	Label(master, text="服务").grid(row=6,sticky=W)
	Label(master, text="位置范围").grid(row=7,sticky=W)
	Label(master, text="纬度").grid(row=8,sticky=W)
	Label(master, text="经度").grid(row=9,sticky=W)
	Label(master, text="比特位(0-3)").grid(row=10,sticky=W)


	#Configure Entries
	ttc_host = Entry(master)
	ttc_host.insert(END,'10.149.90.154')
	ttc_port = Entry(master)
	ttc_port.insert(END,'6566')
#	cmd = Entry(master)
#	cmd.insert(END,'create')
	DEVICE = Entry(master)
	DEVICE.insert(END,'01007FFF00000003')
	HSM = Entry(master)
	bouquet = Entry(master)
	bouquet.insert(END,'0x6050')
	ZIPCODE = Entry(master)
	ZIPCODE.insert(END,'U0000001')
	SRV_ID = Entry(master)
	SRV_ID.insert(END,'10')
	DISTANCE = Entry(master)
	DISTANCE.insert(END,'5000')
	LATITUDE = Entry(master)
	LATITUDE.insert(END,'39907074')
	LONGOTUDE = Entry(master)
	LONGOTUDE.insert(END,'116346613')
	BITMAP = Entry(master)
	BITMAP.insert(END,'0')		

	#configure the table using grid
	ttc_host.grid(row=0, column=1, sticky=W)
	ttc_port.grid(row=1, column=1, sticky=W)
#	cmd.grid(row=2, column=1, sticky=W)
	DEVICE.grid(row=2, column=1, sticky=W)
	HSM.grid(row=3, column=1,sticky=W)
	bouquet.grid(row=4, column=1, sticky=W)
	ZIPCODE.grid(row=5, column=1, sticky=W)
	SRV_ID.grid(row=6, column=1, sticky=W)
	DISTANCE.grid(row=7,column=1,sticky=W)
	LATITUDE.grid(row=8,column=1,sticky=W)
	LONGOTUDE.grid(row=9,column=1,sticky=W)
	BITMAP.grid(row=10,column=1,sticky=W)

	v = IntVar()
	v.set(1)
	Radiobutton(master,text='Activation',variable=v,value=1,indicatoron=True).grid(row=11,column=0,sticky=W)
	Radiobutton(master,text='Update',variable=v,value=2,indicatoron=True).grid(row=12,column=0,sticky=W)
	Radiobutton(master,text='Delete',variable=v,value=3,indicatoron=True).grid(row=13,column=0,sticky=W)
	Radiobutton(master,text='OSD Send',variable=v,value=4,indicatoron=True).grid(row=14,column=0,sticky=W)
	Radiobutton(master,text='OSD Delete',variable=v,value=5,indicatoron=True).grid(row=15,column=0,sticky=W)
	Radiobutton(master,text='指纹发送',variable=v,value=6,indicatoron=True).grid(row=16,column=0,sticky=W)
	Radiobutton(master,text='指纹删除',variable=v,value=7,indicatoron=True).grid(row=17,column=0,sticky=W)
	Radiobutton(master,text='应急广播发送-音频',variable=v,value=8,indicatoron=True).grid(row=18,column=0,sticky=W)
	Radiobutton(master,text='应急广播发送-频道',variable=v,value=9,indicatoron=True).grid(row=19,column=0,sticky=W)
	Radiobutton(master,text='应急广播删除',variable=v,value=10,indicatoron=True).grid(row=20,column=0,sticky=W)


	Button(master, text='SEND', command = tk_start).grid(row=21, column=0, sticky=W, pady=4)
	Button(master, text='QUIT', command = master.quit).grid(row=21, column=1, sticky=W, pady=4)
	#Start TCP server 
#	t=threading.Thread(target=tcp_start)
#	t.setDaemon(True)
#	t.start()

	mainloop()
	

	

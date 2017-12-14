#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from lxml import html

# Get login data from an external file
f = open("login_data","r")
USERNAME = f.readline().strip()
PASSWORD = f.readline().strip()
f.close()

# Get url´s from an external file
f = open("urls","r")
URL_LOGIN = f.readline().strip()
URL_UEBERSICHT = f.readline().strip()
URL_KESSEL = f.readline().strip()
URL_SAUGANLAGE = f.readline().strip()
URL_SAUGZEITEN = f.readline().strip()
URL_HEIZKREIS = f.readline().strip()
URL_HEIZZEITEN = f.readline().strip()
URL_BRAUCHWASSER = f.readline().strip()
URL_PUFFER = f.readline().strip()
URL_ZIRKULATION = f.readline().strip()
URL_ALLGEMEIN = f.readline().strip()
f.close()

# Init session
session_requests = requests.session()

# Get login token
result = session_requests.get(URL_LOGIN)
tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='__RequestVerificationToken']/@value")))

# Create payload
payload = {
	"UserName": USERNAME,
	"Password": PASSWORD,
	"__RequestVerificationToken": authenticity_token
}

# Perform login
result = session_requests.post(URL_LOGIN, data = payload, headers = dict(referer = URL_LOGIN))

# Uebersicht-Elemente UE_
result = session_requests.get(URL_UEBERSICHT, headers = dict(referer = URL_UEBERSICHT))
tree = html.fromstring(result.content.decode('UTF-8'))
UE_K_TempIst			= tree.get_element_by_id("val_000_00590").text 	#°C
UE_K_RueckLaufTempIst	= tree.get_element_by_id("val_000_00590").text 	#°C
UE_HK_RaumTempIst		= tree.get_element_by_id("val_002_00335").text 	#°C
UE_HK_VorlaufTempIst	= tree.get_element_by_id("val_002_00336").text 	#°C
UE_BW_TempIst			= tree.get_element_by_id("val_001_00487").text 	#°C
UE_P_TempOben			= tree.get_element_by_id("val_000_00442").text 	#°C
UE_P_TempUnten			= tree.get_element_by_id("val_000_00446").text	#°C

# Kessel-Elemente KE_
result = session_requests.get(URL_KESSEL, headers = dict(referer = URL_KESSEL))
tree = html.fromstring(result.content.decode('UTF-8'))
KE_Status				= tree.get_element_by_id("val_000_00939").text 	#none
KE_Leistung				= tree.get_element_by_id("val_000_00002").text 	#%
KE_TempIst				= tree.get_element_by_id("val_000_00589").text 	#°C
KE_TempSoll				= tree.get_element_by_id("val_000_00617").text 	#°C
KE_Pumpe				= tree.get_element_by_id("val_000_00608").text 	#none
KE_RueckLaufTempIst		= tree.get_element_by_id("val_000_00590").text 	#°C
KE_RueckLaufTempSoll	= tree.get_element_by_id("val_000_00625").text 	#°C
KE_VollLastStunden		= tree.get_element_by_id("val_000_00729").text 	#h
KE_StatusRLA			= tree.get_element_by_id("val_000_00622").text 	#none
KE_AussenTemp			= tree.get_element_by_id("val_000_00390").text 	#°C

# Saugzeiten-Elemente SZ_
result = session_requests.get(URL_SAUGZEITEN, headers = dict(referer = URL_SAUGZEITEN))
tree = html.fromstring(result.content.decode('UTF-8'))
SZ_Beforzugt_On1		= tree.get_element_by_id("SwitchOn1").value 	#hh:mm
SZ_Beforzugt_Off1		= tree.get_element_by_id("SwitchOff1").value 	#hh:mm
SZ_Beforzugt_On2		= tree.get_element_by_id("SwitchOn2").value 	#hh:mm
SZ_Beforzugt_Off2		= tree.get_element_by_id("SwitchOff2").value 	#hh:mm

# Sauganlage-Elemente SA_
result = session_requests.get(URL_SAUGANLAGE, headers = dict(referer = URL_SAUGANLAGE))
tree = html.fromstring(result.content.decode('UTF-8'))
#SA_BeforzugteZeit1		= tree.get_element_by_id("switch_000_00045")[0].getnext().getnext().text	#none
SA_SaugTurbine			= tree.get_element_by_id("val_000_00637").text 	#none
SA_Status				= tree.get_element_by_id("val_000_00079").text 	#none
SA_Ueberfuellschutz		= tree.get_element_by_id("val_000_00660").text 	#none
SA_TemperaturAntrieb	= tree.get_element_by_id("val_000_00947").text 	#none

# Heizkreis-Elemente HK_
result = session_requests.get(URL_HEIZKREIS, headers = dict(referer = URL_HEIZKREIS))
tree = html.fromstring(result.content.decode('UTF-8'))
HZ_Status				= tree.get_element_by_id("val_002_00346").text 		#none
HZ_StatusUrsache		= tree.get_element_by_id("val_002_00347").text 		#none
HZ_RaumTempIst			= tree.get_element_by_id("val_002_00335").text 		#°C
HZ_RaumTempSoll			= tree.get_element_by_id("val_002_00343").text 		#°C
HZ_AussenTemp			= tree.get_element_by_id("val_002_00334").text 		#°C
HZ_VorlaufTempIst		= tree.get_element_by_id("val_002_00336").text 		#°C
HZ_Pumpe				= tree.get_element_by_id("val_002_00340").text 		#none
HZ_Mischer				= tree.get_element_by_id("val_002_00338").text 		#°C
HZ_Program				= tree.get_element_by_id("switch_002_00342").xpath("//*[@selected='selected']")[0].text 	#none
HZ_AbsenkTemp			= tree.get_element_by_id("slider_002_00344").value 	#°C
HZ_KomfortTemp			= tree.get_element_by_id("slider_002_00345").value 	#°C

# Heizzeiten-Elemente HZ_
result = session_requests.get(URL_HEIZZEITEN, headers = dict(referer = URL_HEIZZEITEN))
tree = html.fromstring(result.content.decode('UTF-8'))
HZ_Montag_Sonntag		= tree.get_element_by_id("WeekdayId").xpath("//*[@value='800']/@data-ip-heating-values") 	#arrayOf(hh:mm)
HZ_Montag_Freitag		= tree.get_element_by_id("WeekdayId").xpath("//*[@value='900']/@data-ip-heating-values") 	#arrayOf(hh:mm)
HZ_Sonntag				= tree.get_element_by_id("WeekdayId").xpath("//*[@value='0']/@data-ip-heating-values") 		#arrayOf(hh:mm)
HZ_Montag				= tree.get_element_by_id("WeekdayId").xpath("//*[@value='1']/@data-ip-heating-values") 		#arrayOf(hh:mm)
HZ_Dienstag				= tree.get_element_by_id("WeekdayId").xpath("//*[@value='2']/@data-ip-heating-values") 		#arrayOf(hh:mm)
HZ_Mittwoch				= tree.get_element_by_id("WeekdayId").xpath("//*[@value='3']/@data-ip-heating-values") 		#arrayOf(hh:mm)
HZ_Donnerstag			= tree.get_element_by_id("WeekdayId").xpath("//*[@value='4']/@data-ip-heating-values") 		#arrayOf(hh:mm)
HZ_Freitag				= tree.get_element_by_id("WeekdayId").xpath("//*[@value='5']/@data-ip-heating-values") 		#arrayOf(hh:mm)
HZ_Samstag				= tree.get_element_by_id("WeekdayId").xpath("//*[@value='6']/@data-ip-heating-values") 		#arrayOf(hh:mm)

# Print data (Debug)
print(HZ_Dienstag)
print(HZ_Mittwoch)

#input()













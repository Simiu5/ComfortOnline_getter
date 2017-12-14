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

# Init lists
nameList = list()
valList = list()

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

nameList.append("Kessel-Temperatur Ist [°C]")
UE_K_TempIst = tree.get_element_by_id("val_000_00589").text
valList.append(UE_K_TempIst)

nameList.append("Kessel-Rücklauftemperatur Ist [°C]")
UE_K_RueckLaufTempIst = tree.get_element_by_id("val_000_00590").text 
valList.append(UE_K_RueckLaufTempIst)

nameList.append("Heizkreis-Raumtemperatur Ist [°C]")
UE_HK_RaumTempIst = tree.get_element_by_id("val_002_00335").text
valList.append(UE_HK_RaumTempIst)

nameList.append("Heizkreis-Vorlauftemperatur Ist [°C]")
UE_HK_VorlaufTempIst = tree.get_element_by_id("val_002_00336").text
valList.append(UE_HK_VorlaufTempIst)

nameList.append("Brauchwasser-Temperatur Ist [°C]")
UE_BW_TempIst = tree.get_element_by_id("val_001_00487").text
valList.append(UE_BW_TempIst)

nameList.append("Puffer-Temperatur Oben [°C]")
UE_P_TempOben = tree.get_element_by_id("val_000_00442").text
valList.append(UE_P_TempOben)

nameList.append("Puffer-Temperatur Unten [°C]")
UE_P_TempUnten = tree.get_element_by_id("val_000_00446").text
valList.append(UE_P_TempUnten)


# Kessel-Elemente KE_
result = session_requests.get(URL_KESSEL, headers = dict(referer = URL_KESSEL))
tree = html.fromstring(result.content.decode('UTF-8'))

nameList.append("Kessel [0=Aus|1=Ein]")
HK_KesselEinAus	= tree.xpath("//*[@id='switch_000_00001']/@data-cop-oldvaluetext")[0]
valList.append(HK_KesselEinAus)

nameList.append("Kessel-Status")
KE_Status = tree.get_element_by_id("val_000_00939").text
valList.append(KE_Status)

nameList.append("Kessel-Leistung [%]")
KE_Leistung	= tree.get_element_by_id("val_000_00002").text
valList.append(KE_Leistung)

nameList.append("Kessel-Temperatur Ist [°C]")
KE_TempIst = tree.get_element_by_id("val_000_00589").text
valList.append(KE_TempIst)

nameList.append("Kessel-Temperatur Soll [°C]")
KE_TempSoll = tree.get_element_by_id("val_000_00617").text
valList.append(KE_TempSoll)

nameList.append("Kessel-Pumpe")
KE_Pumpe = tree.get_element_by_id("val_000_00608").text
valList.append(KE_Pumpe)

nameList.append("Kessel-Rücklauftemperatur Ist [°C]")
KE_RueckLaufTempIst = tree.get_element_by_id("val_000_00590").text
valList.append(KE_RueckLaufTempIst)

nameList.append("Kessel-Rücklauftemperatur Soll [°C]")
KE_RueckLaufTempSoll = tree.get_element_by_id("val_000_00625").text
valList.append(KE_RueckLaufTempSoll)

nameList.append("Kessel-Volllaststunden [h]")
KE_VollLastStunden = tree.get_element_by_id("val_000_00729").text
valList.append(KE_VollLastStunden)

nameList.append("Kessel-Nennleistung [kW]")
KE_NennLeistung = tree.get_element_by_id("val_000_00019").text
valList.append(KE_NennLeistung)

nameList.append("KKessel-Status RLA")
KE_StatusRLA = tree.get_element_by_id("val_000_00622").text
valList.append(KE_StatusRLA)

nameList.append("Kessel-Fördersystem")
KE_FoederSystem = tree.get_element_by_id("val_000_00914").text
valList.append(KE_FoederSystem)

nameList.append("Kessel-Aussentemperatur Ist [°C]")
KE_AussenTemp = tree.get_element_by_id("val_000_00390").text
valList.append(KE_AussenTemp)


# Saugzeiten-Elemente SZ_
result = session_requests.get(URL_SAUGZEITEN, headers = dict(referer = URL_SAUGZEITEN))
tree = html.fromstring(result.content.decode('UTF-8'))

nameList.append("Saugzeit 1 Ein [hh:mm]")
SZ_Beforzugt_On1 = tree.get_element_by_id("SwitchOn1").value
valList.append(SZ_Beforzugt_On1)

nameList.append("Saugzeit 1 Aus [hh:mm]")
SZ_Beforzugt_Off1 = tree.get_element_by_id("SwitchOff1").value
valList.append(SZ_Beforzugt_Off1)

nameList.append("Saugzeit 2 Ein [hh:mm]")
SZ_Beforzugt_On2 = tree.get_element_by_id("SwitchOn2").value
valList.append(SZ_Beforzugt_On2)

nameList.append("Saugzeit 2 Aus [hh:mm]")
SZ_Beforzugt_Off2 = tree.get_element_by_id("SwitchOff2").value
valList.append(SZ_Beforzugt_Off2)


# Sauganlage-Elemente SA_
result = session_requests.get(URL_SAUGANLAGE, headers = dict(referer = URL_SAUGANLAGE))
tree = html.fromstring(result.content.decode('UTF-8'))
SA_TUBBrennstoff			= tree.get_element_by_id("val_000_00605").text 	#none
SA_SaugTurbine				= tree.get_element_by_id("val_000_00637").text 	#none
SA_Status					= tree.get_element_by_id("val_000_00079").text 	#none
SA_Ueberfuellschutz			= tree.get_element_by_id("val_000_00660").text 	#none
SA_TemperaturAntrieb		= tree.get_element_by_id("val_000_00947").text 	#none

# Heizkreis-Elemente HK_
result = session_requests.get(URL_HEIZKREIS, headers = dict(referer = URL_HEIZKREIS))
tree = html.fromstring(result.content.decode('UTF-8'))
HK_Status					= tree.get_element_by_id("val_002_00346").text 		#none
HK_StatusUrsache			= tree.get_element_by_id("val_002_00347").text 		#none
HK_RaumTempIst				= tree.get_element_by_id("val_002_00335").text 		#°C
HK_RaumTempSoll				= tree.get_element_by_id("val_002_00343").text 		#°C
HK_AussenTemp				= tree.get_element_by_id("val_002_00334").text 		#°C
HK_VorlaufTempIst			= tree.get_element_by_id("val_002_00336").text 		#°C
HK_Pumpe					= tree.get_element_by_id("val_002_00340").text 		#none
HK_Mischer					= tree.get_element_by_id("val_002_00338").text 		#°C
HK_Program					= tree.xpath("//*[@selected='selected']")[0].text 	#none
HK_AbsenkTemp				= tree.get_element_by_id("slider_002_00344").value 	#°C
HK_KomfortTemp				= tree.get_element_by_id("slider_002_00345").value 	#°C
HK_UrlaubsFunktion			= tree.xpath("//*[@id='switch_002_00389']/@data-cop-oldvaluetext")[0] 	#0=AUS;1=EIN
HK_UrlaubTemp				= tree.get_element_by_id("slider_002_00361").value 	#°C
HK_UrlaubBeginn				= tree.get_element_by_id("date_002_00348").value 	#dd.mm.yyyy
HK_UrlaubEnde				= tree.get_element_by_id("date_002_00349").value 	#dd.mm.yyyy
HK_PartyBetrieb				= tree.xpath("//*[@id='switch_002_00341']/@data-cop-oldvaluetext")[0]	#0=AUS;1=EIN
HK_PartyDurchheizenBis 		= tree.get_element_by_id("date_002_00362").value 	#hh:mm
HK_AussenTempAbschaltung	= tree.xpath("//*[@id='switch_002_00328']/@data-cop-oldvaluetext")[0] 	#0=AUS;1=EIN
HK_AussenTempAbschaltKomfort= tree.get_element_by_id("slider_002_00332").value 	#°C
HK_AussenTempAbschaltAbsenk	= tree.get_element_by_id("slider_002_00331").value 	#°C
HK_Raumeinfluss				= tree.get_element_by_id("slider_002_00355").value 	#none
HK_Steigung					= tree.get_element_by_id("slider_002_00356").value 	#none
HK_OffSet					= tree.get_element_by_id("slider_002_00367").value 	#none
HK_EcoBetrieb				= tree.xpath("//*[@id='switch_002_00329']/@data-cop-oldvaluetext")[0] 	##0=AUS;1=ImAbsenk;2=ImKomfort;3=Immer

# Heizzeiten-Elemente HZ_
result = session_requests.get(URL_HEIZZEITEN, headers = dict(referer = URL_HEIZZEITEN))
tree = html.fromstring(result.content.decode('UTF-8'))
HZ_Montag_Sonntag			= tree.get_element_by_id("WeekdayId").xpath("//*[@value='800']/@data-ip-heating-values") 	#arrayOf(hh:mm)
HZ_Montag_Freitag			= tree.get_element_by_id("WeekdayId").xpath("//*[@value='900']/@data-ip-heating-values") 	#arrayOf(hh:mm)
HZ_Sonntag					= tree.get_element_by_id("WeekdayId").xpath("//*[@value='0']/@data-ip-heating-values") 		#arrayOf(hh:mm)
HZ_Montag					= tree.get_element_by_id("WeekdayId").xpath("//*[@value='1']/@data-ip-heating-values") 		#arrayOf(hh:mm)
HZ_Dienstag					= tree.get_element_by_id("WeekdayId").xpath("//*[@value='2']/@data-ip-heating-values") 		#arrayOf(hh:mm)
HZ_Mittwoch					= tree.get_element_by_id("WeekdayId").xpath("//*[@value='3']/@data-ip-heating-values") 		#arrayOf(hh:mm)
HZ_Donnerstag				= tree.get_element_by_id("WeekdayId").xpath("//*[@value='4']/@data-ip-heating-values") 		#arrayOf(hh:mm)
HZ_Freitag					= tree.get_element_by_id("WeekdayId").xpath("//*[@value='5']/@data-ip-heating-values") 		#arrayOf(hh:mm)
HZ_Samstag					= tree.get_element_by_id("WeekdayId").xpath("//*[@value='6']/@data-ip-heating-values") 		#arrayOf(hh:mm)

# Print data (Debug)
for x,y in zip(nameList,valList):
    print(x,"-->",y)

#input()













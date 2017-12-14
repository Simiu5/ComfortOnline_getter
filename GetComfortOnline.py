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

nameList.append("UE_K_TempIst [°C]")
UE_K_TempIst = tree.get_element_by_id("val_000_00589").text
valList.append(UE_K_TempIst)

nameList.append("UE_K_RueckLaufTempIst [°C]")
UE_K_RueckLaufTempIst = tree.get_element_by_id("val_000_00590").text 
valList.append(UE_K_RueckLaufTempIst)

nameList.append("UE_HK_RaumTempIst [°C]")
UE_HK_RaumTempIst = tree.get_element_by_id("val_002_00335").text
valList.append(UE_HK_RaumTempIst)

nameList.append("UE_HK_VorlaufTempIst [°C]")
UE_HK_VorlaufTempIst = tree.get_element_by_id("val_002_00336").text
valList.append(UE_HK_VorlaufTempIst)

nameList.append("UE_BW_TempIst [°C]")
UE_BW_TempIst = tree.get_element_by_id("val_001_00487").text
valList.append(UE_BW_TempIst)

nameList.append("UE_P_TempOben [°C]")
UE_P_TempOben = tree.get_element_by_id("val_000_00442").text
valList.append(UE_P_TempOben)

nameList.append("UE_P_TempUnten [°C]")
UE_P_TempUnten = tree.get_element_by_id("val_000_00446").text
valList.append(UE_P_TempUnten)


# Kessel-Elemente KE_
result = session_requests.get(URL_KESSEL, headers = dict(referer = URL_KESSEL))
tree = html.fromstring(result.content.decode('UTF-8'))

nameList.append("KE_KesselEinAus [0=Aus|1=Ein]")
KE_KesselEinAus	= tree.xpath("//*[@id='switch_000_00001']/@data-cop-oldvaluetext")[0]
valList.append(KE_KesselEinAus)

nameList.append("KE_Status")
KE_Status = tree.get_element_by_id("val_000_00939").text
valList.append(KE_Status)

nameList.append("KE_Leistung [%]")
KE_Leistung	= tree.get_element_by_id("val_000_00002").text
valList.append(KE_Leistung)

nameList.append("KE_TempIst [°C]")
KE_TempIst = tree.get_element_by_id("val_000_00589").text
valList.append(KE_TempIst)

nameList.append("KE_TempSoll [°C]")
KE_TempSoll = tree.get_element_by_id("val_000_00617").text
valList.append(KE_TempSoll)

nameList.append("KE_Pumpe")
KE_Pumpe = tree.get_element_by_id("val_000_00608").text
valList.append(KE_Pumpe)

nameList.append("KE_RueckLaufTempIst [°C]")
KE_RueckLaufTempIst = tree.get_element_by_id("val_000_00590").text
valList.append(KE_RueckLaufTempIst)

nameList.append("KE_RueckLaufTempSoll [°C]")
KE_RueckLaufTempSoll = tree.get_element_by_id("val_000_00625").text
valList.append(KE_RueckLaufTempSoll)

nameList.append("KE_VollLastStunden [h]")
KE_VollLastStunden = tree.get_element_by_id("val_000_00729").text
valList.append(KE_VollLastStunden)

nameList.append("KE_NennLeistung [kW]")
KE_NennLeistung = tree.get_element_by_id("val_000_00019").text
valList.append(KE_NennLeistung)

nameList.append("KE_StatusRLA")
KE_StatusRLA = tree.get_element_by_id("val_000_00622").text
valList.append(KE_StatusRLA)

nameList.append("KE_FoederSystem")
KE_FoederSystem = tree.get_element_by_id("val_000_00914").text
valList.append(KE_FoederSystem)

nameList.append("KE_AussenTemp [°C]")
KE_AussenTemp = tree.get_element_by_id("val_000_00390").text
valList.append(KE_AussenTemp)


# Sauganlage-Elemente SA_
result = session_requests.get(URL_SAUGANLAGE, headers = dict(referer = URL_SAUGANLAGE))
tree = html.fromstring(result.content.decode('UTF-8'))

nameList.append("SA_BeforzugtZeit1 [0=Aus|1=Ein]")
SA_BeforzugtZeit1 = tree.xpath("//*[@id='switch_000_00045']/@data-cop-oldvaluetext")[0]
valList.append(SA_BeforzugtZeit1)

nameList.append("SA_BeforzugtZeit2 [0=Aus|1=Ein]")
SA_BeforzugtZeit2 = tree.xpath("//*[@id='switch_000_00046']/@data-cop-oldvaluetext")[0]
valList.append(SA_BeforzugtZeit2)

nameList.append("SA_TUBBrennstoff")
SA_TUBBrennstoff = tree.get_element_by_id("val_000_00605").text
valList.append(SA_TUBBrennstoff)

nameList.append("SA_SaugTurbine")
SA_SaugTurbine = tree.get_element_by_id("val_000_00637").text
valList.append(SA_SaugTurbine)

nameList.append("SA_Status")
SA_Status = tree.get_element_by_id("val_000_00079").text
valList.append(SA_Status)

nameList.append("SA_Ueberfuellschutz")
SA_Ueberfuellschutz	= tree.get_element_by_id("val_000_00660").text
valList.append(SA_Ueberfuellschutz)

nameList.append("SA_TemperaturAntrieb")
SA_TemperaturAntrieb = tree.get_element_by_id("val_000_00947").text
valList.append(SA_TemperaturAntrieb)

nameList.append("SA_HaendischFuellen [0=Aus|1=Ein]")
SA_HaendischFuellen = tree.xpath("//*[@id='switch_000_00640']/@data-cop-oldvaluetext")[0]
valList.append(SA_HaendischFuellen)


# Saugzeiten-Elemente SZ_
result = session_requests.get(URL_SAUGZEITEN, headers = dict(referer = URL_SAUGZEITEN))
tree = html.fromstring(result.content.decode('UTF-8'))

nameList.append("SZ_BevorzugtEin1 [hh:mm]")
SZ_BevorzugtEin1 = tree.get_element_by_id("SwitchOn1").value
valList.append(SZ_BevorzugtEin1)

nameList.append("SZ_BevorzugtAus1 [hh:mm]")
SZ_BevorzugtAus1 = tree.get_element_by_id("SwitchOff1").value
valList.append(SZ_BevorzugtAus1)

nameList.append("SZ_BevorzugtEin2 [hh:mm]")
SZ_BevorzugtEin2 = tree.get_element_by_id("SwitchOn2").value
valList.append(SZ_BevorzugtEin2)

nameList.append("SZ_BevorzugtAus2 [hh:mm]")
SZ_BevorzugtAus2 = tree.get_element_by_id("SwitchOff2").value
valList.append(SZ_BevorzugtAus2)


# Heizkreis-Elemente HK_
result = session_requests.get(URL_HEIZKREIS, headers = dict(referer = URL_HEIZKREIS))
tree = html.fromstring(result.content.decode('UTF-8'))

nameList.append("HK_Status")
HK_Status = tree.get_element_by_id("val_002_00346").text
valList.append(HK_Status)

nameList.append("HK_StatusUrsache")
HK_StatusUrsache = tree.get_element_by_id("val_002_00347").text
valList.append(HK_StatusUrsache)

nameList.append("HK_RaumTempIst [°C]")
HK_RaumTempIst = tree.get_element_by_id("val_002_00335").text
valList.append(HK_RaumTempIst)

nameList.append("HK_RaumTempSoll [°C]")
HK_RaumTempSoll	= tree.get_element_by_id("val_002_00343").text
valList.append(HK_RaumTempSoll)

nameList.append("HK_AussenTemp [°C]")
HK_AussenTemp = tree.get_element_by_id("val_002_00334").text
valList.append(HK_AussenTemp)

nameList.append("HK_VorlaufTempIst [°C]")
HK_VorlaufTempIst = tree.get_element_by_id("val_002_00336").text
valList.append(HK_VorlaufTempIst)

nameList.append("HK_Pumpe")
HK_Pumpe = tree.get_element_by_id("val_002_00340").text
valList.append(HK_Pumpe)

nameList.append("HK_Mischer")
HK_Mischer = tree.get_element_by_id("val_002_00338").text
valList.append(HK_Mischer)

nameList.append("HK_Program")
HK_Program = tree.xpath("//*[@selected='selected']")[0].text
valList.append(HK_Program)

nameList.append("HK_AbsenkTemp [°C]")
HK_AbsenkTemp = tree.get_element_by_id("slider_002_00344").value
valList.append(HK_AbsenkTemp)

nameList.append("HK_KomfortTemp [°C]")
HK_KomfortTemp = tree.get_element_by_id("slider_002_00345").value
valList.append(HK_KomfortTemp)

nameList.append("HK_UrlaubsFunktion [0=Aus|1=Ein]")
HK_UrlaubsFunktion = tree.xpath("//*[@id='switch_002_00389']/@data-cop-oldvaluetext")[0]
valList.append(HK_UrlaubsFunktion)

nameList.append("HK_UrlaubTemp [°C]")
HK_UrlaubTemp = tree.get_element_by_id("slider_002_00361").value
valList.append(HK_UrlaubTemp)

nameList.append("HK_UrlaubBeginn [dd.mm.yyyy]")
HK_UrlaubBeginn = tree.get_element_by_id("date_002_00348").value
valList.append(HK_UrlaubBeginn)

nameList.append("HK_UrlaubEnde [dd.mm.yyyy]")
HK_UrlaubEnde = tree.get_element_by_id("date_002_00349").value
valList.append(HK_UrlaubEnde)

nameList.append("HK_PartyBetrieb [0=Aus|1=Ein]")
HK_PartyBetrieb = tree.xpath("//*[@id='switch_002_00341']/@data-cop-oldvaluetext")[0]
valList.append(HK_PartyBetrieb)

nameList.append("HK_PartyDurchheizenBis [hh:mm]")
HK_PartyDurchheizenBis = tree.get_element_by_id("date_002_00362").value
valList.append(HK_PartyDurchheizenBis)

nameList.append("HK_AussenTempAbschaltung [0=Aus|1=Ein]")
HK_AussenTempAbschaltung = tree.xpath("//*[@id='switch_002_00328']/@data-cop-oldvaluetext")[0]
valList.append(HK_AussenTempAbschaltung)

nameList.append("HK_AussenTempAbschaltKomfort [°C]")
HK_AussenTempAbschaltKomfort= tree.get_element_by_id("slider_002_00332").value
valList.append(HK_AussenTempAbschaltKomfort)

nameList.append("HK_AussenTempAbschaltAbsenk [°C]")
HK_AussenTempAbschaltAbsenk	= tree.get_element_by_id("slider_002_00331").value
valList.append(HK_AussenTempAbschaltAbsenk)

nameList.append("HK_Raumeinfluss")
HK_Raumeinfluss = tree.get_element_by_id("slider_002_00355").value
valList.append(HK_Raumeinfluss)

nameList.append("HK_Steigung")
HK_Steigung	= tree.get_element_by_id("slider_002_00356").value
valList.append(HK_Steigung)

nameList.append("HK_OffSet")
HK_OffSet = tree.get_element_by_id("slider_002_00367").value
valList.append(HK_OffSet)

nameList.append("HK_EcoBetrieb [0=Aus|1=ImAbsenk|2=ImKomfort|3=Immer]")
HK_EcoBetrieb = tree.xpath("//*[@id='switch_002_00329']/@data-cop-oldvaluetext")[0]
valList.append(HK_EcoBetrieb)


# Heizzeiten-Elemente HZ_
result = session_requests.get(URL_HEIZZEITEN, headers = dict(referer = URL_HEIZZEITEN))
tree = html.fromstring(result.content.decode('UTF-8'))

nameList.append("HZ_Montag_Sonntag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]")
HZ_Montag_Sonntag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='800']/@data-ip-heating-values")[0]
valList.append(HZ_Montag_Sonntag)

nameList.append("HZ_Montag_Freitag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]")
HZ_Montag_Freitag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='900']/@data-ip-heating-values")[0]
valList.append(HZ_Montag_Sonntag)

nameList.append("HZ_Sonntag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]")
HZ_Sonntag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='0']/@data-ip-heating-values")[0]
valList.append(HZ_Montag_Sonntag)

nameList.append("HZ_Montag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]")
HZ_Montag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='1']/@data-ip-heating-values")[0]
valList.append(HZ_Montag_Sonntag)

nameList.append("HZ_Dienstag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]")
HZ_Dienstag	= tree.get_element_by_id("WeekdayId").xpath("//*[@value='2']/@data-ip-heating-values")[0]
valList.append(HZ_Montag_Sonntag)

nameList.append("HZ_Mittwoch [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]")
HZ_Mittwoch	= tree.get_element_by_id("WeekdayId").xpath("//*[@value='3']/@data-ip-heating-values")[0]
valList.append(HZ_Montag_Sonntag)

nameList.append("HZ_Donnerstag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]")
HZ_Donnerstag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='4']/@data-ip-heating-values")[0]
valList.append(HZ_Montag_Sonntag)

nameList.append("HZ_Freitag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]")
HZ_Freitag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='5']/@data-ip-heating-values")[0]
valList.append(HZ_Montag_Sonntag)

nameList.append("HZ_Samstag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]")
HZ_Samstag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='6']/@data-ip-heating-values")[0]
valList.append(HZ_Montag_Sonntag)


# Print data (Debug)
for x,y in zip(nameList,valList):
    print(x,"-->",y)

#input()













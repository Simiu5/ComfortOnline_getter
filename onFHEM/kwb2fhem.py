#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from lxml import html
import socket


# Connection to FHEM
# fhem's telnet port
host = 'localhost'
port = 7072


# Get login data from an external file
f = open("/opt/fhem/scripts/login_data","r")
USERNAME = f.readline().strip()
PASSWORD = f.readline().strip()
f.close()


# Get url´s from an external file
f = open("/opt/fhem/scripts/urls","r")
URL_LOGIN = f.readline().strip()
URL_UEBERSICHT = f.readline().strip()
URL_KESSEL = f.readline().strip()
URL_SAUGANLAGE = f.readline().strip()
URL_SAUGZEITEN = f.readline().strip()
URL_HEIZKREIS = f.readline().strip()
URL_HEIZZEITEN = f.readline().strip()
URL_BRAUCHWASSER = f.readline().strip()
URL_BRAUCHZEITEN = f.readline().strip()
URL_PUFFER = f.readline().strip()
URL_PUFFERZEITEN = f.readline().strip()
URL_ZUBRINGERPUMPE = f.readline().strip()
URL_ZIRKULATION = f.readline().strip()
URL_ZIRKZEITEN = f.readline().strip()
URL_ALLGEMEIN = f.readline().strip()
URL_ALARMEAKTIV = f.readline().strip()
URL_ALARMEALLE = f.readline().strip()
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

nameList.append("UE_Name")
valList.append("Uebersicht")

nameList.append("UE_KE_TempIst [°C]")
UE_KE_TempIst = tree.get_element_by_id("val_000_00589").text
valList.append(UE_KE_TempIst)

nameList.append("UE_KE_RuecklaufTempIst [°C]")
UE_KE_RuecklaufTempIst = tree.get_element_by_id("val_000_00590").text 
valList.append(UE_KE_RuecklaufTempIst)

nameList.append("UE_HK_RaumTempIst [°C]")
UE_HK_RaumTempIst = tree.get_element_by_id("val_002_00335").text
valList.append(UE_HK_RaumTempIst)

nameList.append("UE_HK_VorlaufTempIst [°C]")
UE_HK_VorlaufTempIst = tree.get_element_by_id("val_002_00336").text
valList.append(UE_HK_VorlaufTempIst)

nameList.append("UE_BW_TempIst [°C]")
UE_BW_TempIst = tree.get_element_by_id("val_001_00487").text
valList.append(UE_BW_TempIst)

nameList.append("UE_PU_TempOben [°C]")
UE_PU_TempOben = tree.get_element_by_id("val_000_00442").text
valList.append(UE_PU_TempOben)

nameList.append("UE_PU_TempUnten [°C]")
UE_PU_TempUnten = tree.get_element_by_id("val_000_00446").text
valList.append(UE_PU_TempUnten)


# Kessel-Elemente KE_
result = session_requests.get(URL_KESSEL, headers = dict(referer = URL_KESSEL))
tree = html.fromstring(result.content.decode('UTF-8'))

nameList.append("KE_Name")
valList.append("Kessel")

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

nameList.append("KE_RuecklaufTempIst [°C]")
KE_RuecklaufTempIst = tree.get_element_by_id("val_000_00590").text
valList.append(KE_RuecklaufTempIst)

nameList.append("KE_RuecklaufTempSoll [°C]")
KE_RuecklaufTempSoll = tree.get_element_by_id("val_000_00625").text
valList.append(KE_RuecklaufTempSoll)

nameList.append("KE_Volllaststunden [h]")
KE_Volllaststunden = tree.get_element_by_id("val_000_00729").text
valList.append(KE_Volllaststunden)

nameList.append("KE_Nennleistung [kW]")
KE_Nennleistung = tree.get_element_by_id("val_000_00019").text
valList.append(KE_Nennleistung)

nameList.append("KE_RLAMischer")
KE_RLAMischer = tree.get_element_by_id("val_000_00622").text
valList.append(KE_RLAMischer)

nameList.append("KE_Foedersystem")
KE_Foedersystem = tree.get_element_by_id("val_000_00914").text
valList.append(KE_Foedersystem)

nameList.append("KE_AussenTemp [°C]")
KE_AussenTemp = tree.get_element_by_id("val_000_00390").text
valList.append(KE_AussenTemp)


# Sauganlage-Elemente SA_
result = session_requests.get(URL_SAUGANLAGE, headers = dict(referer = URL_SAUGANLAGE))
tree = html.fromstring(result.content.decode('UTF-8'))

nameList.append("SA_Name")
valList.append("Sauganlage")

nameList.append("SA_BeforzugteZeit1 [0=Aus|1=Ein]")
SA_BeforzugteZeit1 = tree.xpath("//*[@id='switch_000_00045']/@data-cop-oldvaluetext")[0]
valList.append(SA_BeforzugteZeit1)

nameList.append("SA_BeforzugteZeit2 [0=Aus|1=Ein]")
SA_BeforzugteZeit2 = tree.xpath("//*[@id='switch_000_00046']/@data-cop-oldvaluetext")[0]
valList.append(SA_BeforzugteZeit2)

nameList.append("SA_TUBBrennstoff")
SA_TUBBrennstoff = tree.get_element_by_id("val_000_00605").text
valList.append(SA_TUBBrennstoff)

nameList.append("SA_Saugturbine")
SA_Saugturbine = tree.get_element_by_id("val_000_00637").text
valList.append(SA_Saugturbine)

nameList.append("SA_Status")
SA_Status = tree.get_element_by_id("val_000_00079").text
valList.append(SA_Status)

nameList.append("SA_Fuellstand")
SA_Fuellstand	= tree.get_element_by_id("val_000_00660").text
valList.append(SA_Fuellstand)

nameList.append("SA_HaendischFuellen [0=Aus|1=Ein]")
SA_HaendischFuellen = tree.xpath("//*[@id='switch_000_00640']/@data-cop-oldvaluetext")[0]
valList.append(SA_HaendischFuellen)


# # Saugzeiten-Elemente SZ_
# result = session_requests.get(URL_SAUGZEITEN, headers = dict(referer = URL_SAUGZEITEN))
# tree = html.fromstring(result.content.decode('UTF-8'))

# nameList.append("SZ_BevorzugtEin1 [hh:mm]")
# SZ_BevorzugtEin1 = tree.get_element_by_id("SwitchOn1").value
# valList.append(SZ_BevorzugtEin1)

# nameList.append("SZ_BevorzugtAus1 [hh:mm]")
# SZ_BevorzugtAus1 = tree.get_element_by_id("SwitchOff1").value
# valList.append(SZ_BevorzugtAus1)

# nameList.append("SZ_BevorzugtEin2 [hh:mm]")
# SZ_BevorzugtEin2 = tree.get_element_by_id("SwitchOn2").value
# valList.append(SZ_BevorzugtEin2)

# nameList.append("SZ_BevorzugtAus2 [hh:mm]")
# SZ_BevorzugtAus2 = tree.get_element_by_id("SwitchOff2").value
# valList.append(SZ_BevorzugtAus2)


# Heizkreis-Elemente HK_
result = session_requests.get(URL_HEIZKREIS, headers = dict(referer = URL_HEIZKREIS))
tree = html.fromstring(result.content.decode('UTF-8'))

nameList.append("HK_Name")
HK_Name = tree.get_element_by_id("val_002_00337").text
valList.append(HK_Name)

nameList.append("HK_Status")
HK_Status = tree.get_element_by_id("val_002_00346").text
valList.append(HK_Status)

nameList.append("HK_Statusursache")
HK_Statusursache = tree.get_element_by_id("val_002_00347").text
valList.append(HK_Statusursache)

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

nameList.append("HK_UrlaubsTemp [°C]")
HK_UrlaubsTemp = tree.get_element_by_id("slider_002_00361").value
valList.append(HK_UrlaubsTemp)

nameList.append("HK_UrlaubsBeginn [dd.mm.yyyy]")
HK_UrlaubsBeginn = tree.get_element_by_id("date_002_00348").value
valList.append(HK_UrlaubsBeginn)

nameList.append("HK_UrlaubsEnde [dd.mm.yyyy]")
HK_UrlaubsEnde = tree.get_element_by_id("date_002_00349").value
valList.append(HK_UrlaubsEnde)

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

nameList.append("HK_Offset")
HK_Offset = tree.get_element_by_id("slider_002_00367").value
valList.append(HK_Offset)

nameList.append("HK_Ecobetrieb [0=Aus|1=ImAbsenk|2=ImKomfort|3=Immer]")
HK_Ecobetrieb = tree.xpath("//*[@id='switch_002_00329']/@data-cop-oldvaluetext")[0]
valList.append(HK_Ecobetrieb)


# # Heizzeiten-Elemente HZ_
# result = session_requests.get(URL_HEIZZEITEN, headers = dict(referer = URL_HEIZZEITEN))
# tree = html.fromstring(result.content.decode('UTF-8'))

# nameList.append("HZ_Montag_Sonntag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# HZ_Montag_Sonntag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='800']/@data-ip-heating-values")[0]
# valList.append(HZ_Montag_Sonntag)

# nameList.append("HZ_Montag_Freitag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# HZ_Montag_Freitag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='900']/@data-ip-heating-values")[0]
# valList.append(HZ_Montag_Freitag)

# nameList.append("HZ_Sonntag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# HZ_Sonntag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='0']/@data-ip-heating-values")[0]
# valList.append(HZ_Sonntag)

# nameList.append("HZ_Montag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# HZ_Montag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='1']/@data-ip-heating-values")[0]
# valList.append(HZ_Montag)

# nameList.append("HZ_Dienstag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# HZ_Dienstag	= tree.get_element_by_id("WeekdayId").xpath("//*[@value='2']/@data-ip-heating-values")[0]
# valList.append(HZ_Dienstag)

# nameList.append("HZ_Mittwoch [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# HZ_Mittwoch	= tree.get_element_by_id("WeekdayId").xpath("//*[@value='3']/@data-ip-heating-values")[0]
# valList.append(HZ_Mittwoch)

# nameList.append("HZ_Donnerstag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# HZ_Donnerstag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='4']/@data-ip-heating-values")[0]
# valList.append(HZ_Donnerstag)

# nameList.append("HZ_Freitag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# HZ_Freitag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='5']/@data-ip-heating-values")[0]
# valList.append(HZ_Freitag)

# nameList.append("HZ_Samstag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# HZ_Samstag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='6']/@data-ip-heating-values")[0]
# valList.append(HZ_Samstag)


# Brauchwasser-Elemente BW_
result = session_requests.get(URL_BRAUCHWASSER, headers = dict(referer = URL_BRAUCHWASSER))
tree = html.fromstring(result.content.decode('UTF-8'))

nameList.append("BW_Name")
BW_Name = tree.get_element_by_id("val_001_00488").text
valList.append(BW_Name)

nameList.append("BW_Status")
BW_Status = tree.get_element_by_id("val_001_00513").text
valList.append(BW_Status)

nameList.append("BW_TempIst [°C]")
BW_TempIst = tree.get_element_by_id("val_001_00487").text
valList.append(BW_TempIst)

nameList.append("BW_TempSoll [°C]")
BW_TempSoll = tree.get_element_by_id("val_001_00507").text
valList.append(BW_TempSoll)

nameList.append("BW_Ladepumpe")
BW_Ladepumpe = tree.get_element_by_id("val_001_00491").text
valList.append(BW_Ladepumpe)

nameList.append("BW_Anforderung")
BW_Anforderung = tree.get_element_by_id("val_001_00485").text
valList.append(BW_Anforderung)

nameList.append("BW_Programm")
BW_Programm = tree.xpath("//*[@selected='selected']")[0].text
valList.append(BW_Programm)

nameList.append("BW_EinmalErhitzen [0=Aus|1=Ein]")
BW_EinmalErhitzen = tree.xpath("//*[@id='switch_001_00493']/@data-cop-oldvaluetext")[0]
valList.append(BW_EinmalErhitzen)

nameList.append("BW_TempMin [°C]")
BW_TempMin = tree.get_element_by_id("rslider_001_00981").value
valList.append(BW_TempMin)

nameList.append("BW_TempMax [°C]")
BW_TempMax = tree.get_element_by_id("rslider_001_00981_2").value
valList.append(BW_TempMax)

nameList.append("BW_UrlaubsFunktion [0=Aus|1=Ein]")
BW_UrlaubsFunktion = tree.xpath("//*[@id='switch_001_00511']/@data-cop-oldvaluetext")[0]
valList.append(BW_UrlaubsFunktion)

nameList.append("BW_UrlaubsTemp [°C]")
BW_UrlaubsTemp = tree.get_element_by_id("slider_001_00498").value
valList.append(BW_UrlaubsTemp)

nameList.append("BW_UrlaubsBeginn [dd.mm.yyyy]")
BW_UrlaubsBeginn = tree.get_element_by_id("date_001_00496").value
valList.append(BW_UrlaubsBeginn)

nameList.append("BW_UrlaubsEnde [dd.mm.yyyy]")
BW_UrlaubsEnde = tree.get_element_by_id("date_001_00497").value
valList.append(BW_UrlaubsEnde)

nameList.append("BW_LegioSchutzWochentag [0=Sonntag|1=Montag|2=Dienstag|3=Mittwoch|4=Donnerstag|5=Freitag|6=Samstag|7=Aus]")
BW_LegioSchutzWochentag = tree.xpath("//*[@id='switch_001_00501']/@data-cop-oldvaluetext")[0]
valList.append(BW_LegioSchutzWochentag)

nameList.append("BW_LegioSchutzTemp [°C]")
BW_LegioSchutzTemp = tree.get_element_by_id("slider_001_00504").value
valList.append(BW_LegioSchutzTemp)


# # BrauchwasserZeiten-Elemente BZ_
# result = session_requests.get(URL_BRAUCHZEITEN, headers = dict(referer = URL_BRAUCHZEITEN))
# tree = html.fromstring(result.content.decode('UTF-8'))

# nameList.append("BZ_Montag_Sonntag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# BZ_Montag_Sonntag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='800']/@data-ip-heating-values")[0]
# valList.append(BZ_Montag_Sonntag)

# nameList.append("BZ_Montag_Freitag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# BZ_Montag_Freitag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='900']/@data-ip-heating-values")[0]
# valList.append(BZ_Montag_Freitag)

# nameList.append("BZ_Sonntag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# BZ_Sonntag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='0']/@data-ip-heating-values")[0]
# valList.append(BZ_Sonntag)

# nameList.append("BZ_Montag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# BZ_Montag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='1']/@data-ip-heating-values")[0]
# valList.append(BZ_Montag)

# nameList.append("BZ_Dienstag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# BZ_Dienstag	= tree.get_element_by_id("WeekdayId").xpath("//*[@value='2']/@data-ip-heating-values")[0]
# valList.append(BZ_Dienstag)

# nameList.append("BZ_Mittwoch [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# BZ_Mittwoch	= tree.get_element_by_id("WeekdayId").xpath("//*[@value='3']/@data-ip-heating-values")[0]
# valList.append(BZ_Mittwoch)

# nameList.append("BZ_Donnerstag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# BZ_Donnerstag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='4']/@data-ip-heating-values")[0]
# valList.append(BZ_Donnerstag)

# nameList.append("BZ_Freitag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# BZ_Freitag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='5']/@data-ip-heating-values")[0]
# valList.append(BZ_Freitag)

# nameList.append("BZ_Samstag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# BZ_Samstag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='6']/@data-ip-heating-values")[0]
# valList.append(BZ_Samstag)


# Puffer-Elemente PU_
result = session_requests.get(URL_PUFFER, headers = dict(referer = URL_PUFFER))
tree = html.fromstring(result.content.decode('UTF-8'))

nameList.append("PU_Name")
PU_Name = tree.get_element_by_id("val_000_00447").text
valList.append(PU_Name)

nameList.append("PU_Status")
PU_Status = tree.get_element_by_id("val_000_00483").text
valList.append(PU_Status)

nameList.append("PU_TempOben [°C]")
PU_TempOben = tree.get_element_by_id("val_000_00442").text
valList.append(PU_TempOben)

nameList.append("PU_TempUnten [°C]")
PU_TempUnten = tree.get_element_by_id("val_000_00446").text
valList.append(PU_TempUnten)

nameList.append("PU_TempSoll [°C]")
PU_TempSoll = tree.get_element_by_id("val_000_00469").text
valList.append(PU_TempSoll)

nameList.append("PU_Anforderung")
PU_Anforderung = tree.get_element_by_id("val_000_00440").text
valList.append(PU_Anforderung)

nameList.append("PU_Pumpe")
PU_Pumpe = tree.get_element_by_id("val_000_00450").text
valList.append(PU_Pumpe)

nameList.append("PU_PumpeInfo")
PU_PumpeInfo = tree.get_element_by_id("val_000_00484").text
valList.append(PU_PumpeInfo)

nameList.append("PU_BrauchwasserTempMin [°C]")
PU_BrauchwasserTempMin = tree.get_element_by_id("slider_000_00479").value
valList.append(PU_BrauchwasserTempMin)

nameList.append("PU_TempMin [°C]")
PU_TempMin = tree.get_element_by_id("rslider_000_00982").value
valList.append(PU_TempMin)

nameList.append("PU_TempMax [°C]")
PU_TempMax = tree.get_element_by_id("rslider_000_00982_2").value
valList.append(PU_TempMax)

nameList.append("PU_Umschaltventil")
PU_Umschaltventil = tree.get_element_by_id("val_000_00468").text
valList.append(PU_Umschaltventil)

nameList.append("PU_UmschaltTemp [°C]")
PU_UmschaltTemp = tree.get_element_by_id("slider_000_00464").value
valList.append(PU_UmschaltTemp)

nameList.append("PU_Programm")
PU_Programm = tree.xpath("//*[@selected='selected']")[0].text
valList.append(PU_Programm)

nameList.append("PU_Typ")
PU_Typ = tree.get_element_by_id("val_000_00473").text
valList.append(PU_Typ)

nameList.append("PU_LegioSchutzWochentag [0=Sonntag|1=Montag|2=Dienstag|3=Mittwoch|4=Donnerstag|5=Freitag|6=Samstag|7=Aus]")
PU_LegioSchutzWochentag = tree.xpath("//*[@id='switch_000_00480']/@data-cop-oldvaluetext")[0]
valList.append(PU_LegioSchutzWochentag)

nameList.append("PU_LegioSchutzTemp [°C]")
PU_LegioSchutzTemp = tree.get_element_by_id("slider_000_00481").value
valList.append(PU_LegioSchutzTemp)


# # PufferZeiten-Elemente PZ_
# result = session_requests.get(URL_PUFFERZEITEN, headers = dict(referer = URL_PUFFERZEITEN))
# tree = html.fromstring(result.content.decode('UTF-8'))

# nameList.append("PZ_Montag_Sonntag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# PZ_Montag_Sonntag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='800']/@data-ip-heating-values")[0]
# valList.append(PZ_Montag_Sonntag)

# nameList.append("PZ_Montag_Freitag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# PZ_Montag_Freitag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='900']/@data-ip-heating-values")[0]
# valList.append(PZ_Montag_Freitag)

# nameList.append("PZ_Sonntag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# PZ_Sonntag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='0']/@data-ip-heating-values")[0]
# valList.append(PZ_Sonntag)

# nameList.append("PZ_Montag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# PZ_Montag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='1']/@data-ip-heating-values")[0]
# valList.append(PZ_Montag)

# nameList.append("PZ_Dienstag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# PZ_Dienstag	= tree.get_element_by_id("WeekdayId").xpath("//*[@value='2']/@data-ip-heating-values")[0]
# valList.append(PZ_Dienstag)

# nameList.append("PZ_Mittwoch [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# PZ_Mittwoch	= tree.get_element_by_id("WeekdayId").xpath("//*[@value='3']/@data-ip-heating-values")[0]
# valList.append(PZ_Mittwoch)

# nameList.append("PZ_Donnerstag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# PZ_Donnerstag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='4']/@data-ip-heating-values")[0]
# valList.append(PZ_Donnerstag)

# nameList.append("PZ_Freitag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# PZ_Freitag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='5']/@data-ip-heating-values")[0]
# valList.append(PZ_Freitag)

# nameList.append("PZ_Samstag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# PZ_Samstag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='6']/@data-ip-heating-values")[0]
# valList.append(PZ_Samstag)


# Zubringerpumpe-Elemente ZU_
result = session_requests.get(URL_ZUBRINGERPUMPE, headers = dict(referer = URL_ZUBRINGERPUMPE))
tree = html.fromstring(result.content.decode('UTF-8'))

nameList.append("ZU_Name")
ZU_Name = tree.get_element_by_id("val_001_01133").text
valList.append(ZU_Name)

nameList.append("ZU_TempSoll")
ZU_TempSoll = tree.get_element_by_id("val_001_01135").text
valList.append(ZU_TempSoll)

nameList.append("ZU_Anforderung")
ZU_Anforderung = tree.get_element_by_id("val_001_01134").text
valList.append(ZU_Anforderung)

nameList.append("ZU_Pumpe")
ZU_Pumpe = tree.get_element_by_id("val_001_00450").text
valList.append(ZU_Pumpe)


# Zirkulation-Elemente ZI_
result = session_requests.get(URL_ZIRKULATION, headers = dict(referer = URL_ZIRKULATION))
tree = html.fromstring(result.content.decode('UTF-8'))

nameList.append("ZI_Name")
valList.append("Zirkulation")

nameList.append("ZI_Pumpe")
ZI_Pumpe = tree.get_element_by_id("val_001_00904").text
valList.append(ZI_Pumpe)

nameList.append("ZI_Taster")
ZI_Taster = tree.get_element_by_id("val_001_00901").text
valList.append(ZI_Taster)

nameList.append("ZI_Temp [°C]")
ZI_Temp = tree.get_element_by_id("val_001_00902").text
valList.append(ZI_Temp)

nameList.append("ZI_Program")
ZI_Program = tree.xpath("//*[@selected='selected']")[0].text
valList.append(ZI_Program)


# # ZirkZeiten-Elemente ZZ_
# result = session_requests.get(URL_ZIRKZEITEN, headers = dict(referer = URL_ZIRKZEITEN))
# tree = html.fromstring(result.content.decode('UTF-8'))

# nameList.append("ZZ_Montag_Sonntag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# ZZ_Montag_Sonntag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='800']/@data-ip-heating-values")[0]
# valList.append(ZZ_Montag_Sonntag)

# nameList.append("ZZ_Montag_Freitag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# ZZ_Montag_Freitag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='900']/@data-ip-heating-values")[0]
# valList.append(ZZ_Montag_Freitag)

# nameList.append("ZZ_Sonntag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# ZZ_Sonntag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='0']/@data-ip-heating-values")[0]
# valList.append(ZZ_Sonntag)

# nameList.append("ZZ_Montag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# ZZ_Montag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='1']/@data-ip-heating-values")[0]
# valList.append(ZZ_Montag)

# nameList.append("ZZ_Dienstag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# ZZ_Dienstag	= tree.get_element_by_id("WeekdayId").xpath("//*[@value='2']/@data-ip-heating-values")[0]
# valList.append(ZZ_Dienstag)

# nameList.append("ZZ_Mittwoch [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# ZZ_Mittwoch	= tree.get_element_by_id("WeekdayId").xpath("//*[@value='3']/@data-ip-heating-values")[0]
# valList.append(ZZ_Mittwoch)

# nameList.append("ZZ_Donnerstag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# ZZ_Donnerstag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='4']/@data-ip-heating-values")[0]
# valList.append(ZZ_Donnerstag)

# nameList.append("ZZ_Freitag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# ZZ_Freitag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='5']/@data-ip-heating-values")[0]
# valList.append(ZZ_Freitag)

# nameList.append("ZZ_Samstag [\"SwitchOn/OffX {1-4}\":\"hh:mm\"]\n")
# ZZ_Samstag = tree.get_element_by_id("WeekdayId").xpath("//*[@value='6']/@data-ip-heating-values")[0]
# valList.append(ZZ_Samstag)


# Allgemein-Elemente AG_
result = session_requests.get(URL_ALLGEMEIN, headers = dict(referer = URL_ALLGEMEIN))
tree = html.fromstring(result.content.decode('UTF-8'))

nameList.append("AG_Name")
valList.append("Allgemeines")

nameList.append("AG_Kesselname")
AG_Kesselname = tree.get_element_by_id("val_000_00391").text
valList.append(AG_Kesselname)

nameList.append("AG_Kesseltyp")
AG_Kesseltyp = tree.get_element_by_id("val_000_00951").text
valList.append(AG_Kesseltyp)

nameList.append("AG_Seriennummer")
AG_Seriennummer = tree.get_element_by_id("val_000_00407").text
valList.append(AG_Seriennummer)

nameList.append("AG_Serienstand")
AG_Serienstand = tree.get_element_by_id("val_000_00408").text
valList.append(AG_Serienstand)

nameList.append("AG_WartungAnzahl")
AG_WartungAnzahl = tree.get_element_by_id("val_000_00690").text
valList.append(AG_WartungAnzahl)

nameList.append("AG_LetzteWartung [dd.mm.yyyy]")
AG_LetzteWartung = tree.get_element_by_id("val_000_00698").text
valList.append(AG_LetzteWartung)

nameList.append("AG_WartungIntervall [h]")
AG_WartungIntervall = tree.get_element_by_id("val_000_00695").text
valList.append(AG_WartungIntervall)

nameList.append("AG_NaechsteWartung [h]")
AG_NaechsteWartung = tree.get_element_by_id("val_000_00739").text
valList.append(AG_NaechsteWartung)

nameList.append("AG_KontrolleAnzahl")
AG_KontrolleAnzahl = tree.get_element_by_id("spin_000_00691").value
valList.append(AG_KontrolleAnzahl)

nameList.append("AG_KontrolleIntervall")
AG_KontrolleIntervall = tree.get_element_by_id("spin_000_00694").value
valList.append(AG_KontrolleIntervall)

nameList.append("AG_KontrolleRestdauer [h]")
AG_KontrolleRestdauer = tree.get_element_by_id("val_000_00740").text
valList.append(AG_KontrolleRestdauer)

nameList.append("AG_MailSenden [0=Aus|1=Ein]")
AG_MailSenden = tree.xpath("//*[@id='switch_000_00434']/@data-cop-oldvaluetext")[0]
valList.append(AG_MailSenden)

nameList.append("AG_EMail")
AG_EMail = tree.get_element_by_id("text_000_00413").value
valList.append(AG_EMail)

nameList.append("AG_Zeitabstand [min]")
AG_Zeitabstand = tree.get_element_by_id("slider_000_00435").value
valList.append(AG_Zeitabstand)


#AlarmeAktiv-Elemente
result = session_requests.get(URL_ALARMEAKTIV, headers = dict(referer = URL_ALARMEAKTIV))
tree = html.fromstring(result.content.decode('UTF-8'))

nameList.append("AL_AktivList")
try: AL_AktivList = tree.get_element_by_id("alarmList").text_content()
except: AL_AktivList = "Es sind keine Einträge vorhanden"
valList.append(AL_AktivList)


# # AlarmeAlle-Elemente
# result = session_requests.get(URL_ALARMEALLE, headers = dict(referer = URL_ALARMEALLE))
# tree = html.fromstring(result.content.decode('UTF-8'))

# nameList.append("AL_AlleList")
# AL_AlleList = tree.get_element_by_id("alarmList").text_content()
# valList.append(AL_AlleList)


# Print data (Debug)
# for x,y in zip(nameList,valList):
	# print(x,"\n-->",y)


def netcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(content)
    s.shutdown(socket.SHUT_WR)
    while 1:
        data = s.recv(1024)
        if data == "":
            break
    if data:
        print "Received:", repr(data)
    s.close()


# empty netcat string
s = "";


# Send 2 fhem
# Uebersicht
s += 'setreading {0} UE_KE_TempIst {1}\n'.format("KWB_Uebersicht",UE_KE_TempIst) 
s += 'setreading {0} UE_KE_RuecklaufTempIst {1}\n'.format("KWB_Uebersicht",UE_KE_RuecklaufTempIst) 
s += 'setreading {0} UE_HK_RaumTempIst {1}\n'.format("KWB_Uebersicht",UE_HK_RaumTempIst) 
s += 'setreading {0} UE_HK_VorlaufTempIst {1}\n'.format("KWB_Uebersicht",UE_HK_VorlaufTempIst) 
s += 'setreading {0} UE_BW_TempIst {1}\n'.format("KWB_Uebersicht",UE_BW_TempIst)
s += 'setreading {0} UE_PU_TempOben {1}\n'.format("KWB_Uebersicht",UE_PU_TempOben)
s += 'setreading {0} UE_PU_TempUnten {1}\n'.format("KWB_Uebersicht",UE_PU_TempUnten)

# Kessel
s += 'setreading {0} KE_KesselEinAus {1}\n'.format("KWB_Kessel",KE_KesselEinAus)
s += 'setreading {0} KE_Status {1}\n'.format("KWB_Kessel",KE_Status)
s += 'setreading {0} KE_Leistung {1}\n'.format("KWB_Kessel",KE_Leistung)
s += 'setreading {0} KE_TempIst {1}\n'.format("KWB_Kessel",KE_TempIst)
s += 'setreading {0} KE_TempSoll {1}\n'.format("KWB_Kessel",KE_TempSoll)
s += 'setreading {0} KE_Pumpe {1}\n'.format("KWB_Kessel",KE_Pumpe)
s += 'setreading {0} KE_RuecklaufTempIst {1}\n'.format("KWB_Kessel",KE_RuecklaufTempIst)
s += 'setreading {0} KE_RuecklaufTempSoll {1}\n'.format("KWB_Kessel",KE_RuecklaufTempSoll)
s += 'setreading {0} KE_Volllaststunden {1}\n'.format("KWB_Kessel",KE_Volllaststunden)
s += 'setreading {0} KE_Nennleistung {1}\n'.format("KWB_Kessel",KE_Nennleistung)
s += 'setreading {0} KE_RLAMischer {1}\n'.format("KWB_Kessel",KE_RLAMischer)
s += 'setreading {0} KE_Foedersystem {1}\n'.format("KWB_Kessel",KE_Foedersystem)
s += 'setreading {0} KE_AussenTemp {1}\n'.format("KWB_Kessel",KE_AussenTemp)

# Sauganlage
s += 'setreading {0} SA_BeforzugteZeit1 {1}\n'.format("KWB_Sauganlage",SA_BeforzugteZeit1)
s += 'setreading {0} SA_BeforzugteZeit2 {1}\n'.format("KWB_Sauganlage",SA_BeforzugteZeit2)
s += 'setreading {0} SA_TUBBrennstoff {1}\n'.format("KWB_Sauganlage",SA_TUBBrennstoff)
s += 'setreading {0} SA_Saugturbine {1}\n'.format("KWB_Sauganlage",SA_Saugturbine)
s += 'setreading {0} SA_Status {1}\n'.format("KWB_Sauganlage",SA_Status)
s += 'setreading {0} SA_Fuellstand {1}\n'.format("KWB_Sauganlage",SA_Fuellstand)
s += 'setreading {0} SA_HaendischFuellen {1}\n'.format("KWB_Sauganlage",SA_HaendischFuellen)

# Heizkreis
s += 'setreading {0} HK_Status {1}\n'.format("KWB_Heizkeis",HK_Status)
s += 'setreading {0} HK_Statusursache {1}\n'.format("KWB_Heizkeis",HK_Statusursache)
s += 'setreading {0} HK_RaumTempIst {1}\n'.format("KWB_Heizkeis",HK_RaumTempIst)
s += 'setreading {0} HK_RaumTempSoll {1}\n'.format("KWB_Heizkeis",HK_RaumTempSoll)
s += 'setreading {0} HK_AussenTemp {1}\n'.format("KWB_Heizkeis",HK_AussenTemp)
s += 'setreading {0} HK_VorlaufTempIst {1}\n'.format("KWB_Heizkeis",HK_VorlaufTempIst)
s += 'setreading {0} HK_Pumpe {1}\n'.format("KWB_Heizkeis",HK_Pumpe)
s += 'setreading {0} HK_Mischer {1}\n'.format("KWB_Heizkeis",HK_Mischer)
s += 'setreading {0} HK_Program {1}\n'.format("KWB_Heizkeis",HK_Program)
s += 'setreading {0} HK_AbsenkTemp {1}\n'.format("KWB_Heizkeis",HK_AbsenkTemp)
s += 'setreading {0} HK_KomfortTemp {1}\n'.format("KWB_Heizkeis",HK_KomfortTemp)
s += 'setreading {0} HK_UrlaubsFunktion {1}\n'.format("KWB_Heizkeis",HK_UrlaubsFunktion)
s += 'setreading {0} HK_UrlaubsTemp {1}\n'.format("KWB_Heizkeis",HK_UrlaubsTemp)
s += 'setreading {0} HK_UrlaubsBeginn {1}\n'.format("KWB_Heizkeis",HK_UrlaubsBeginn)
s += 'setreading {0} HK_UrlaubsEnde {1}\n'.format("KWB_Heizkeis",HK_UrlaubsEnde)
s += 'setreading {0} HK_PartyBetrieb {1}\n'.format("KWB_Heizkeis",HK_PartyBetrieb)
s += 'setreading {0} HK_PartyDurchheizenBis {1}\n'.format("KWB_Heizkeis",HK_PartyDurchheizenBis)
s += 'setreading {0} HK_AussenTempAbschaltung {1}\n'.format("KWB_Heizkeis",HK_AussenTempAbschaltung)
s += 'setreading {0} HK_AussenTempAbschaltKomfort {1}\n'.format("KWB_Heizkeis",HK_AussenTempAbschaltKomfort)
s += 'setreading {0} HK_AussenTempAbschaltAbsenk {1}\n'.format("KWB_Heizkeis",HK_AussenTempAbschaltAbsenk)
s += 'setreading {0} HK_Raumeinfluss {1}\n'.format("KWB_Heizkeis",HK_Raumeinfluss)
s += 'setreading {0} HK_Steigung {1}\n'.format("KWB_Sauganlage",HK_Steigung)
s += 'setreading {0} HK_Offset {1}\n'.format("KWB_Heizkeis",HK_Offset)
s += 'setreading {0} HK_Ecobetrieb {1}\n'.format("KWB_Heizkeis",HK_Ecobetrieb)

# Brauchwasser
s += 'setreading {0} BW_Status {1}\n'.format("KWB_Brauchwasser",BW_Status)
s += 'setreading {0} BW_TempIst {1}\n'.format("KWB_Brauchwasser",BW_TempIst)
s += 'setreading {0} BW_TempSoll {1}\n'.format("KWB_Brauchwasser",BW_TempSoll)
s += 'setreading {0} BW_Ladepumpe {1}\n'.format("KWB_Brauchwasser",BW_Ladepumpe)
s += 'setreading {0} BW_Anforderung {1}\n'.format("KWB_Brauchwasser",BW_Anforderung)
s += 'setreading {0} BW_Programm {1}\n'.format("KWB_Brauchwasser",BW_Programm)
s += 'setreading {0} BW_EinmalErhitzen {1}\n'.format("KWB_Brauchwasser",BW_EinmalErhitzen)
s += 'setreading {0} BW_TempMin {1}\n'.format("KWB_Brauchwasser",BW_TempMin)
s += 'setreading {0} BW_TempMax {1}\n'.format("KWB_Brauchwasser",BW_TempMax)
s += 'setreading {0} BW_UrlaubsFunktion {1}\n'.format("KWB_Brauchwasser",BW_UrlaubsFunktion)
s += 'setreading {0} BW_UrlaubsTemp {1}\n'.format("KWB_Brauchwasser",BW_UrlaubsTemp)
s += 'setreading {0} BW_UrlaubsBeginn {1}\n'.format("KWB_Brauchwasser",BW_UrlaubsBeginn)
s += 'setreading {0} BW_UrlaubsEnde {1}\n'.format("KWB_Brauchwasser",HK_Raumeinfluss)
s += 'setreading {0} BW_LegioSchutzWochentag {1}\n'.format("KWB_Brauchwasser",BW_LegioSchutzWochentag)
s += 'setreading {0} BW_LegioSchutzTemp {1}\n'.format("KWB_Brauchwasser",BW_LegioSchutzTemp)

# Puffer
s += 'setreading {0} PU_Status {1}\n'.format("KWB_Puffer",PU_Status)
s += 'setreading {0} PU_TempOben {1}\n'.format("KWB_Puffer",PU_TempOben)
s += 'setreading {0} PU_TempUnten {1}\n'.format("KWB_Puffer",PU_TempUnten)
s += 'setreading {0} PU_TempSoll {1}\n'.format("KWB_Puffer",PU_TempSoll)
s += 'setreading {0} PU_Anforderung {1}\n'.format("KWB_Puffer",PU_Anforderung)
s += 'setreading {0} PU_Pumpe {1}\n'.format("KWB_Puffer",PU_Pumpe)
s += 'setreading {0} PU_PumpeInfo {1}\n'.format("KWB_Puffer",PU_PumpeInfo)
s += 'setreading {0} PU_BrauchwasserTempMin {1}\n'.format("KWB_Puffer",PU_BrauchwasserTempMin)
s += 'setreading {0} PU_TempMin {1}\n'.format("KWB_Puffer",PU_TempMin)
s += 'setreading {0} PU_TempMax {1}\n'.format("KWB_Puffer",PU_TempMax)
s += 'setreading {0} PU_Umschaltventil {1}\n'.format("KWB_Puffer",PU_Umschaltventil)
s += 'setreading {0} PU_UmschaltTemp {1}\n'.format("KWB_Puffer",PU_UmschaltTemp)
s += 'setreading {0} PU_Programm {1}\n'.format("KWB_Puffer",PU_Programm)
s += 'setreading {0} PU_LegioSchutzWochentag {1}\n'.format("KWB_Puffer",PU_LegioSchutzWochentag)
s += 'setreading {0} PU_LegioSchutzTemp {1}\n'.format("KWB_Puffer",PU_LegioSchutzTemp)

# Zubringerpumpe
s += 'setreading {0} ZU_TempSoll {1}\n'.format("KWB_Zubringerpumpe",ZU_TempSoll)
s += 'setreading {0} ZU_Anforderung {1}\n'.format("KWB_Zubringerpumpe",ZU_Anforderung)
s += 'setreading {0} ZU_Pumpe {1}\n'.format("KWB_Zubringerpumpe",ZU_Pumpe)

# Zirkulation
s += 'setreading {0} ZI_Pumpe {1}\n'.format("KWB_Zirkulation",ZI_Pumpe)
s += 'setreading {0} ZI_Taster {1}\n'.format("KWB_Zirkulation",ZI_Taster)
s += 'setreading {0} ZI_Temp {1}\n'.format("KWB_Zirkulation",ZI_Temp)
s += 'setreading {0} ZI_Program {1}\n'.format("KWB_Zirkulation",ZI_Program)

# Allgemein
s += 'setreading {0} AG_Kesselname {1}\n'.format("KWB_Allgemein",AG_Kesselname)
s += 'setreading {0} AG_Kesseltyp {1}\n'.format("KWB_Allgemein",AG_Kesseltyp)
s += 'setreading {0} AG_Seriennummer {1}\n'.format("KWB_Allgemein",AG_Seriennummer)
s += 'setreading {0} AG_Serienstand {1}\n'.format("KWB_Allgemein",AG_Serienstand)
s += 'setreading {0} AG_WartungAnzahl {1}\n'.format("KWB_Allgemein",AG_WartungAnzahl)
s += 'setreading {0} AG_LetzteWartung {1}\n'.format("KWB_Allgemein",AG_LetzteWartung)
s += 'setreading {0} AG_WartungIntervall {1}\n'.format("KWB_Allgemein",AG_WartungIntervall)
s += 'setreading {0} AG_NaechsteWartung {1}\n'.format("KWB_Allgemein",AG_NaechsteWartung)
s += 'setreading {0} AG_KontrolleAnzahl {1}\n'.format("KWB_Allgemein",AG_KontrolleAnzahl)
s += 'setreading {0} AG_KontrolleIntervall {1}\n'.format("KWB_Allgemein",AG_KontrolleIntervall)
s += 'setreading {0} AG_KontrolleRestdauer {1}\n'.format("KWB_Allgemein",AG_KontrolleRestdauer)
s += 'setreading {0} AG_MailSenden {1}\n'.format("KWB_Allgemein",AG_MailSenden)
s += 'setreading {0} AG_EMail {1}\n'.format("KWB_Allgemein",AG_EMail)
s += 'setreading {0} AG_Zeitabstand {1}\n'.format("KWB_Allgemein",AG_Zeitabstand)

# Aktive Alarme
s += 'setreading {0} AL_AktivList {1}\n'.format("KWB_Alarme",AL_AktivList)


s += "quit"

netcat(host, port, s)


























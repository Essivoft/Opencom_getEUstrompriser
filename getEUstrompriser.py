import requests
import os
import time
from datetime import datetime, timedelta
import json
import csv
import zipfile
import logging
import creds
import xml.etree.ElementTree as ET
from currency_converter import ECB_URL, SINGLE_DAY_ECB_URL, CurrencyConverter
import pandas as pd
from ckanapi import RemoteCKAN

# Lag mapper for lagring av data og feil
os.makedirs("StromPriserNorge", exist_ok=True )
os.makedirs("StromPriserNorgeErrors", exist_ok=True)

# Variables
baseUrl = "https://web-api.tp.entsoe.eu/api"
timeString2= time.strftime('%Y-%m-%d')
timeString3 = time.strftime("%d-%B-%Y")
ckanAPIKey = creds.ckan_api_key
# Yesterday
yesterday = datetime.now() - timedelta(days=1)
yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
yesterday_str = yesterday.strftime('%Y%m%d%H%M')
norges_bank_yesterday_str = yesterday.strftime('%Y-%m-%d')
# Tomorrow 
tomorrow = datetime.now() + timedelta(days=1)
tomorrow = tomorrow.replace(hour=00, minute=0, second=0, microsecond=0)
tomorrow_str = tomorrow.strftime('%Y%m%d%H%M')
tomorrow_str_2format = tomorrow.strftime('%Y-%m-%d')
print (tomorrow_str)
# Overmorrow
overmorrow = datetime.now() + timedelta(days=2)
overmorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
overmorrow_str = tomorrow.strftime('%Y%m%d%H%M')
overmorrow_str_2format = tomorrow.strftime('%Y-%m-%d')
# Time now
today = datetime.now()
today = today.replace(hour=00, minute=0, second=0, microsecond=0)
today_str = today.strftime('%Y%m%d%H%M')
print (today_str)

#Set up logging
log_file = os.path.join('StromPriserNorgeErrors', f'StromPriserNorgeErrors.log')
logging.basicConfig(filename=log_file, level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

# First we fetch the latest currency data from https://www.ecb.europa.eu
zip_filename = 'eurofxref.zip'
csv_filename = 'eurofxref.csv'

url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip'
response = requests.get(url)
with open(zip_filename, 'wb') as file:
    file.write(response.content)

# Ectract the CSV file from the ZIP archive
with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
    for filename in zip_ref.namelist():
        if filename.endswith('.csv'):
            zip_ref.extract(filename, '.')
os.remove(zip_filename)

# Get the exchange rate for NOK from the CSV file
with open(csv_filename, 'r', newline='') as file:
    reader = csv.reader(file)
    header = next(reader)
    exchange_rate = None
    nok_index = header.index(' NOK')
    for row in reader:
        if row[nok_index]: # Check if the NOK column is not empty
            exchange_rate = float(row[nok_index])
            break

if exchange_rate is not None:
    print(f'Valutakurs (NOK): {exchange_rate}')
else:
    logging.error('Ingen valutakurs funnet for NOK i csv-filen.')

#===========================================================================        
headers = {
    "securityToken" : creds.eu_secutiry_token
}
#Sone 1 = Østlandet og Nordvestlandet
params_sone_1 = {
    "securityToken" : creds.eu_secutiry_token,
    "documentType" : "A44",
    "In_Domain" : "10YNO-1--------2",
    "Out_Domain" : "10YNO-1--------2",
    "periodStart" : today_str,
    "periodEnd" : tomorrow_str
}
#Sone 2 = Sørvestlandet
params_sone_2 = {
    "securityToken" : creds.eu_secutiry_token,
    "documentType" : "A44",
    "In_Domain" : "10YNO-2--------T",
    "Out_Domain" : "10YNO-2--------T",
    "periodStart" : today_str,
    "periodEnd" : tomorrow_str
}
#Sone 3 = Midt-Norge
params_sone_3 = {
    "securityToken" : creds.eu_secutiry_token,
    "documentType" : "A44",
    "In_Domain" : "10YNO-3--------J",
    "Out_Domain" : "10YNO-3--------J",
    "periodStart" : today_str,
    "periodEnd" : tomorrow_str
}
#Sone 4 = Nord-Norge
params_sone_4 = {
    "securityToken" : creds.eu_secutiry_token,
    "documentType" : "A44",
    "In_Domain" : "10YNO-4--------9",
    "Out_Domain" : "10YNO-4--------9",
    "periodStart" : today_str,
    "periodEnd" : tomorrow_str
}
#Sone 5 = Vestlandet-Norge
params_sone_5 = {
    "securityToken" : creds.eu_secutiry_token,
    "documentType" : "A44",
    "In_Domain" : "10Y1001A1001A48H",
    "Out_Domain" : "10Y1001A1001A48H",
    "periodStart" : today_str,
    "periodEnd" : tomorrow_str
}

#Sone 1
try:
    sporring = requests.get(url = baseUrl, params=params_sone_1, headers=headers)
    print (sporring)
    sporring.raise_for_status()
    data = sporring.content
    with open(f"StromPriserNorge\\StromPriserNorgeSone1.xml", "wb") as outfile:
        outfile.write(data)
except Exception as e:
    logging.error(f"{timeString2}-Error under request for Sone NO-1: {str(e)}")
    raise

#Sone 2
try:
    sporring = requests.get(url = baseUrl, params=params_sone_2, headers=headers)
    #print (sporring)
    sporring.raise_for_status()
    data = sporring.content
    with open(f"StromPriserNorge\\StromPriserNorgeSone2.xml", "wb") as outfile:
        outfile.write(data)
except Exception as e:
    logging.error(f"{timeString2}-Error under request for Sone NO-2: {str(e)}")
    raise

#Sone 3
try:
    sporring = requests.get(url = baseUrl, params=params_sone_3, headers=headers)
    #print (sporring)
    sporring.raise_for_status()
    data = sporring.content
    with open(f"StromPriserNorge\\StromPriserNorgeSone3.xml", "wb") as outfile:
        outfile.write(data)
except Exception as e:
    logging.error(f"{timeString2}-Error under request for Sone NO-3: {str(e)}")
    raise

#Sone 4
try:
    sporring = requests.get(url = baseUrl, params=params_sone_4, headers=headers)
    #print (sporring)
    sporring.raise_for_status()
    data = sporring.content
    with open(f"StromPriserNorge\\StromPriserNorgeSone4.xml", "wb") as outfile:
        outfile.write(data)
except Exception as e:
    logging.error(f"{timeString2}-Error under request for Sone NO-4: {str(e)}")
    raise

#Sone 5
try:
    sporring = requests.get(url = baseUrl, params=params_sone_5, headers=headers)
    #print (sporring)
    sporring.raise_for_status()
    data = sporring.content
    with open(f"StromPriserNorge\\StromPriserNorgeSone5.xml", "wb") as outfile:
        outfile.write(data)
except Exception as e:
    logging.error(f"{timeString2}-Error under request for Sone NO-5: {str(e)}")
    raise

# XML to JSON conversion for Sone 1 ===========================================================================
tree = ET.parse("StromPriserNorge\\StromPriserNorgeSone1.xml")
root = tree.getroot()

# Få navnerommet dynamisk fra rot-elementet uten å sjekke versjonsnummeret
namespace = {'ns': root.tag.split('}')[0].strip('{')}

# Hente ut ønskede felt fra XML og lage et JSON-objekt
try:
    data = {
        "currency_Unit.name": root.findtext(".//ns:currency_Unit.name", namespaces=namespace),
        "price_Measure_Unit.name": root.findtext(".//ns:price_Measure_Unit.name", namespaces=namespace),
        "Periods": []
    }

    # Loop gjennom alle periodene
    for period in root.findall(".//ns:TimeSeries/ns:Period", namespaces=namespace):
        period_start = period.findtext("ns:timeInterval/ns:start", namespaces=namespace)
        period_end = period.findtext("ns:timeInterval/ns:end", namespaces=namespace)

        # Konverter start- og sluttdato til datetime-objekter
        period_start_dt = datetime.strptime(period_start, "%Y-%m-%dT%H:%MZ")
        period_end_dt = datetime.strptime(period_end, "%Y-%m-%dT%H:%MZ")

        # Fjern datofilteret for å teste om periodene hentes korrekt
        period_data = {
            "timeInterval": {
                "start": period_start,
                "end": period_end
            },
            "resolution": period.findtext("ns:resolution", namespaces=namespace),
            "Points": []
        }

        # Loop gjennom alle punktene i perioden
        for point in period.findall("ns:Point", namespaces=namespace):
            position = point.findtext("ns:position", namespaces=namespace)
            price_amount = point.findtext("ns:price.amount", namespaces=namespace)
            period_data["Points"].append({"position": position, "price.amount": price_amount})

        # Legg perioden til i data
        data["Periods"].append(period_data)

    # Konvertere til JSON og lagre i fil
    json_data = json.dumps(data, indent=4)
    with open("StromPriserNorge\\StromPriserNorgeSone1.json", "w") as outfile:
        outfile.write(json_data)

except Exception as e:
    logging.error(f"Error during XML to JSON conversion for Sone 1: {str(e)}")

#XML to JSON convert Sone 2===========================================================================
tree = ET.parse("StromPriserNorge\\StromPriserNorgeSone2.xml")
root = tree.getroot()

# Få navnerommet dynamisk fra rot-elementet uten å sjekke versjonsnummeret
namespace = {'ns': root.tag.split('}')[0].strip('{')}

# Hente ut ønskede felt fra XML og lage et JSON-objekt
try:
    data = {
        "currency_Unit.name": root.findtext(".//ns:currency_Unit.name", namespaces=namespace),
        "price_Measure_Unit.name": root.findtext(".//ns:price_Measure_Unit.name", namespaces=namespace),
        "Periods": []
    }

    # Loop gjennom alle periodene
    for period in root.findall(".//ns:TimeSeries/ns:Period", namespaces=namespace):
        period_start = period.findtext("ns:timeInterval/ns:start", namespaces=namespace)
        period_end = period.findtext("ns:timeInterval/ns:end", namespaces=namespace)

        # Konverter start- og sluttdato til datetime-objekter
        period_start_dt = datetime.strptime(period_start, "%Y-%m-%dT%H:%MZ")
        period_end_dt = datetime.strptime(period_end, "%Y-%m-%dT%H:%MZ")

        # Fjern datofilteret for å teste om periodene hentes korrekt
        period_data = {
            "timeInterval": {
                "start": period_start,
                "end": period_end
            },
            "resolution": period.findtext("ns:resolution", namespaces=namespace),
            "Points": []
        }

        # Loop gjennom alle punktene i perioden
        for point in period.findall("ns:Point", namespaces=namespace):
            position = point.findtext("ns:position", namespaces=namespace)
            price_amount = point.findtext("ns:price.amount", namespaces=namespace)
            period_data["Points"].append({"position": position, "price.amount": price_amount})

        # Legg perioden til i data
        data["Periods"].append(period_data)

    # Konvertere til JSON og lagre i fil
    json_data = json.dumps(data, indent=4)
    with open("StromPriserNorge\\StromPriserNorgeSone2.json", "w") as outfile:
        outfile.write(json_data)

except Exception as e:
    logging.error(f"Error during XML to JSON conversion for Sone 2: {str(e)}")

# #XML to JSON convert Sone 3===========================================================================
tree = ET.parse("StromPriserNorge\\StromPriserNorgeSone3.xml")
root = tree.getroot()

# Få navnerommet dynamisk fra rot-elementet uten å sjekke versjonsnummeret
namespace = {'ns': root.tag.split('}')[0].strip('{')}

# Hente ut ønskede felt fra XML og lage et JSON-objekt
try:
    data = {
        "currency_Unit.name": root.findtext(".//ns:currency_Unit.name", namespaces=namespace),
        "price_Measure_Unit.name": root.findtext(".//ns:price_Measure_Unit.name", namespaces=namespace),
        "Periods": []
    }

    # Loop gjennom alle periodene
    for period in root.findall(".//ns:TimeSeries/ns:Period", namespaces=namespace):
        period_start = period.findtext("ns:timeInterval/ns:start", namespaces=namespace)
        period_end = period.findtext("ns:timeInterval/ns:end", namespaces=namespace)

        # Konverter start- og sluttdato til datetime-objekter
        period_start_dt = datetime.strptime(period_start, "%Y-%m-%dT%H:%MZ")
        period_end_dt = datetime.strptime(period_end, "%Y-%m-%dT%H:%MZ")

        # Fjern datofilteret for å teste om periodene hentes korrekt
        period_data = {
            "timeInterval": {
                "start": period_start,
                "end": period_end
            },
            "resolution": period.findtext("ns:resolution", namespaces=namespace),
            "Points": []
        }

        # Loop gjennom alle punktene i perioden
        for point in period.findall("ns:Point", namespaces=namespace):
            position = point.findtext("ns:position", namespaces=namespace)
            price_amount = point.findtext("ns:price.amount", namespaces=namespace)
            period_data["Points"].append({"position": position, "price.amount": price_amount})

        # Legg perioden til i data
        data["Periods"].append(period_data)

    # Konvertere til JSON og lagre i fil
    json_data = json.dumps(data, indent=4)
    with open("StromPriserNorge\\StromPriserNorgeSone3.json", "w") as outfile:
        outfile.write(json_data)

except Exception as e:
    logging.error(f"Error during XML to JSON conversion for Sone 3: {str(e)}")


# #XML to JSON convert Sone 4===========================================================================
tree = ET.parse("StromPriserNorge\\StromPriserNorgeSone4.xml")
root = tree.getroot()

# Få navnerommet dynamisk fra rot-elementet uten å sjekke versjonsnummeret
namespace = {'ns': root.tag.split('}')[0].strip('{')}

# Hente ut ønskede felt fra XML og lage et JSON-objekt
try:
    data = {
        "currency_Unit.name": root.findtext(".//ns:currency_Unit.name", namespaces=namespace),
        "price_Measure_Unit.name": root.findtext(".//ns:price_Measure_Unit.name", namespaces=namespace),
        "Periods": []
    }

    # Loop gjennom alle periodene
    for period in root.findall(".//ns:TimeSeries/ns:Period", namespaces=namespace):
        period_start = period.findtext("ns:timeInterval/ns:start", namespaces=namespace)
        period_end = period.findtext("ns:timeInterval/ns:end", namespaces=namespace)

        # Konverter start- og sluttdato til datetime-objekter
        period_start_dt = datetime.strptime(period_start, "%Y-%m-%dT%H:%MZ")
        period_end_dt = datetime.strptime(period_end, "%Y-%m-%dT%H:%MZ")

        # Fjern datofilteret for å teste om periodene hentes korrekt
        period_data = {
            "timeInterval": {
                "start": period_start,
                "end": period_end
            },
            "resolution": period.findtext("ns:resolution", namespaces=namespace),
            "Points": []
        }

        # Loop gjennom alle punktene i perioden
        for point in period.findall("ns:Point", namespaces=namespace):
            position = point.findtext("ns:position", namespaces=namespace)
            price_amount = point.findtext("ns:price.amount", namespaces=namespace)
            period_data["Points"].append({"position": position, "price.amount": price_amount})

        # Legg perioden til i data
        data["Periods"].append(period_data)

    # Konvertere til JSON og lagre i fil
    json_data = json.dumps(data, indent=4)
    with open("StromPriserNorge\\StromPriserNorgeSone4.json", "w") as outfile:
        outfile.write(json_data)

except Exception as e:
    logging.error(f"Error during XML to JSON conversion for Sone 4: {str(e)}")


# #XML to JSON convert Sone 5===========================================================================
tree = ET.parse("StromPriserNorge\\StromPriserNorgeSone5.xml")
root = tree.getroot()

# Få navnerommet dynamisk fra rot-elementet uten å sjekke versjonsnummeret
namespace = {'ns': root.tag.split('}')[0].strip('{')}

# Hente ut ønskede felt fra XML og lage et JSON-objekt
try:
    data = {
        "currency_Unit.name": root.findtext(".//ns:currency_Unit.name", namespaces=namespace),
        "price_Measure_Unit.name": root.findtext(".//ns:price_Measure_Unit.name", namespaces=namespace),
        "Periods": []
    }

    # Loop gjennom alle periodene
    for period in root.findall(".//ns:TimeSeries/ns:Period", namespaces=namespace):
        period_start = period.findtext("ns:timeInterval/ns:start", namespaces=namespace)
        period_end = period.findtext("ns:timeInterval/ns:end", namespaces=namespace)

        # Konverter start- og sluttdato til datetime-objekter
        period_start_dt = datetime.strptime(period_start, "%Y-%m-%dT%H:%MZ")
        period_end_dt = datetime.strptime(period_end, "%Y-%m-%dT%H:%MZ")

        # Fjern datofilteret for å teste om periodene hentes korrekt
        period_data = {
            "timeInterval": {
                "start": period_start,
                "end": period_end
            },
            "resolution": period.findtext("ns:resolution", namespaces=namespace),
            "Points": []
        }

        # Loop gjennom alle punktene i perioden
        for point in period.findall("ns:Point", namespaces=namespace):
            position = point.findtext("ns:position", namespaces=namespace)
            price_amount = point.findtext("ns:price.amount", namespaces=namespace)
            period_data["Points"].append({"position": position, "price.amount": price_amount})

        # Legg perioden til i data
        data["Periods"].append(period_data)

    # Konvertere til JSON og lagre i fil
    json_data = json.dumps(data, indent=4)
    with open("StromPriserNorge\\StromPriserNorgeSone5.json", "w") as outfile:
        outfile.write(json_data)

except Exception as e:
    logging.error(f"Error during XML to JSON conversion for Sone 5: {str(e)}")

###Convert JSON to JSON adding NOK Zone 1===========================================================================
# Leser JSON-filen
try:
    with open("StromPriserNorge\\StromPriserNorgeSone1.json", "r", encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Sjekk at "Periods" eksisterer i JSON-strukturen
    if "Periods" in data:
        for period in data["Periods"]:
            if "Points" in period:
                # Går gjennom hvert prisobjekt og endrer feltet "price.amount" til "price.amount.MWh.EUR"
                for point in period["Points"]:
                    if "price.amount" in point:
                        # Bevarer original pris i EUR og konverterer
                        point["price.amount.MWh.EUR"] = float(point.pop("price.amount"))

                        # Utfører konvertering fra EUR til NOK
                        price_eur_mw = point["price.amount.MWh.EUR"]
                        price_eur_kw = price_eur_mw / 1000
                        price_nok_kw = round(price_eur_kw * exchange_rate, 5)

                        # Legger til konverterte verdier
                        point["price.amount.KWh.EUR"] = price_eur_kw
                        point["price.amount.KWh.EUR.Cent"] = price_eur_kw * 100
                        point["price.amount.MWh.NOK"] = round(price_nok_kw * 1000, 6)
                        point["price.amount.KWh.NOK.KR"] = price_nok_kw
                        point["price.amount.KWh.NOK.Ore"] = round(price_nok_kw * 100, 5)

    # Skriver oppdatert JSON-data til fil
    with open("StromPriserNorge\\StromPriserSørlandetEURogNOKSone1.json", "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)
except Exception as e:
    logging.error(f"Error under JSON to JSON Conversion adding NOK Sone 1: {str(e)}")

###Convert JSON to JSON adding NOK Zone 2===========================================================================
# Leser JSON-filen
try:
    with open("StromPriserNorge\\StromPriserNorgeSone2.json", "r", encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Sjekk at "Periods" eksisterer i JSON-strukturen
    if "Periods" in data:
        for period in data["Periods"]:
            if "Points" in period:
                # Går gjennom hvert prisobjekt og endrer feltet "price.amount" til "price.amount.MWh.EUR"
                for point in period["Points"]:
                    if "price.amount" in point:
                        # Bevarer original pris i EUR og konverterer
                        point["price.amount.MWh.EUR"] = float(point.pop("price.amount"))

                        # Utfører konvertering fra EUR til NOK
                        price_eur_mw = point["price.amount.MWh.EUR"]
                        price_eur_kw = price_eur_mw / 1000
                        price_nok_kw = round(price_eur_kw * exchange_rate, 5)

                        # Legger til konverterte verdier
                        point["price.amount.KWh.EUR"] = price_eur_kw
                        point["price.amount.KWh.EUR.Cent"] = price_eur_kw * 100
                        point["price.amount.MWh.NOK"] = round(price_nok_kw * 1000, 6)
                        point["price.amount.KWh.NOK.KR"] = price_nok_kw
                        point["price.amount.KWh.NOK.Ore"] = round(price_nok_kw * 100, 5)

    # Skriver oppdatert JSON-data til fil
    with open("StromPriserNorge\\StromPriserSørlandetEURogNOKSone2.json", "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)
except Exception as e:
    logging.error(f"Error under JSON to JSON Conversion adding NOK Sone 2: {str(e)}")


###Convert JSON to JSON adding NOK Zone 3===========================================================================
# Leser JSON-filen
try:
    with open("StromPriserNorge\\StromPriserNorgeSone3.json", "r", encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Sjekk at "Periods" eksisterer i JSON-strukturen
    if "Periods" in data:
        for period in data["Periods"]:
            if "Points" in period:
                # Går gjennom hvert prisobjekt og endrer feltet "price.amount" til "price.amount.MWh.EUR"
                for point in period["Points"]:
                    if "price.amount" in point:
                        # Bevarer original pris i EUR og konverterer
                        point["price.amount.MWh.EUR"] = float(point.pop("price.amount"))

                        # Utfører konvertering fra EUR til NOK
                        price_eur_mw = point["price.amount.MWh.EUR"]
                        price_eur_kw = price_eur_mw / 1000
                        price_nok_kw = round(price_eur_kw * exchange_rate, 5)

                        # Legger til konverterte verdier
                        point["price.amount.KWh.EUR"] = price_eur_kw
                        point["price.amount.KWh.EUR.Cent"] = price_eur_kw * 100
                        point["price.amount.MWh.NOK"] = round(price_nok_kw * 1000, 6)
                        point["price.amount.KWh.NOK.KR"] = price_nok_kw
                        point["price.amount.KWh.NOK.Ore"] = round(price_nok_kw * 100, 5)

    # Skriver oppdatert JSON-data til fil
    with open("StromPriserNorge\\StromPriserSørlandetEURogNOKSone3.json", "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)
except Exception as e:
    logging.error(f"Error under JSON to JSON Conversion adding NOK Sone 3: {str(e)}")

###Convert JSON to JSON adding NOK Zone 4===========================================================================
# Leser JSON-filen
try:
    with open("StromPriserNorge\\StromPriserNorgeSone4.json", "r", encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Sjekk at "Periods" eksisterer i JSON-strukturen
    if "Periods" in data:
        for period in data["Periods"]:
            if "Points" in period:
                # Går gjennom hvert prisobjekt og endrer feltet "price.amount" til "price.amount.MWh.EUR"
                for point in period["Points"]:
                    if "price.amount" in point:
                        # Bevarer original pris i EUR og konverterer
                        point["price.amount.MWh.EUR"] = float(point.pop("price.amount"))

                        # Utfører konvertering fra EUR til NOK
                        price_eur_mw = point["price.amount.MWh.EUR"]
                        price_eur_kw = price_eur_mw / 1000
                        price_nok_kw = round(price_eur_kw * exchange_rate, 5)

                        # Legger til konverterte verdier
                        point["price.amount.KWh.EUR"] = price_eur_kw
                        point["price.amount.KWh.EUR.Cent"] = price_eur_kw * 100
                        point["price.amount.MWh.NOK"] = round(price_nok_kw * 1000, 6)
                        point["price.amount.KWh.NOK.KR"] = price_nok_kw
                        point["price.amount.KWh.NOK.Ore"] = round(price_nok_kw * 100, 5)

    # Skriver oppdatert JSON-data til fil
    with open("StromPriserNorge\\StromPriserSørlandetEURogNOKSone4.json", "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)
except Exception as e:
    logging.error(f"Error under JSON to JSON Conversion adding NOK Sone 4: {str(e)}")


###Convert JSON to JSON adding NOK Zone 5===========================================================================
# Leser JSON-filen
try:
    with open("StromPriserNorge\\StromPriserNorgeSone5.json", "r", encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Sjekk at "Periods" eksisterer i JSON-strukturen
    if "Periods" in data:
        for period in data["Periods"]:
            if "Points" in period:
                # Går gjennom hvert prisobjekt og endrer feltet "price.amount" til "price.amount.MWh.EUR"
                for point in period["Points"]:
                    if "price.amount" in point:
                        # Bevarer original pris i EUR og konverterer
                        point["price.amount.MWh.EUR"] = float(point.pop("price.amount"))

                        # Utfører konvertering fra EUR til NOK
                        price_eur_mw = point["price.amount.MWh.EUR"]
                        price_eur_kw = price_eur_mw / 1000
                        price_nok_kw = round(price_eur_kw * exchange_rate, 5)

                        # Legger til konverterte verdier
                        point["price.amount.KWh.EUR"] = price_eur_kw
                        point["price.amount.KWh.EUR.Cent"] = price_eur_kw * 100
                        point["price.amount.MWh.NOK"] = round(price_nok_kw * 1000, 6)
                        point["price.amount.KWh.NOK.KR"] = price_nok_kw
                        point["price.amount.KWh.NOK.Ore"] = round(price_nok_kw * 100, 5)

    # Skriver oppdatert JSON-data til fil
    with open("StromPriserNorge\\StromPriserSørlandetEURogNOKSone5.json", "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)
except Exception as e:
    logging.error(f"Error under JSON to JSON Conversion adding NOK Sone 5: {str(e)}")

#Make a CSV file from JSON =================================================================================================
# Åpne JSON-filen
try:
    
    # Angi mappen hvor JSON-filene ligger
    folder_path = 'StromPriserNorge\\'

    # Angi de gitte filnavnene du leter etter
    target_filenames_json = ['StromPriserSørlandetEURogNOKSone1.json', 'StromPriserSørlandetEURogNOKSone2.json',
                             'StromPriserSørlandetEURogNOKSone3.json', 'StromPriserSørlandetEURogNOKSone4.json',
                             'StromPriserSørlandetEURogNOKSone5.json']

    # Angi CSV-kolonnene du ønsker å inkludere
    columns = ['start', 'end', 'position', 'price.amount.MWh.EUR', 'price.amount.KWh.EUR',
               'price.amount.KWh.EUR.Cent', 'price.amount.MWh.NOK', 'price.amount.KWh.NOK.KR',
               'price.amount.KWh.NOK.Ore']

    # Gå gjennom filene i mappen
    for filename in os.listdir(folder_path):
        if filename in target_filenames_json:
            # Les JSON-dataene fra filen
            json_path = os.path.join(folder_path, filename)
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)

            # Sjekk at "Periods" eksisterer i JSON-strukturen
            if "Periods" in data:
                # Angi CSV-filnavnet basert på JSON-filnavnet
                csv_filename = os.path.splitext(filename)[0] + '.csv'

                # Skriv dataene til CSV-filen
                csv_path = os.path.join(folder_path, csv_filename)
                with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=columns)
                    writer.writeheader()

                    # Gå gjennom hver periode og legg til punktene i CSV
                    for period in data["Periods"]:
                        start_time = period['timeInterval']['start']
                        end_time = period['timeInterval']['end']
                        points = period['Points']

                        # Skriv hvert punkt til CSV
                        for point in points:
                            row = {
                                'start': start_time,
                                'end': end_time,
                                'position': point['position'],
                                'price.amount.MWh.EUR': point['price.amount.MWh.EUR'],
                                'price.amount.KWh.EUR': point['price.amount.KWh.EUR'],
                                'price.amount.KWh.EUR.Cent': point['price.amount.KWh.EUR.Cent'],
                                'price.amount.MWh.NOK': point['price.amount.MWh.NOK'],
                                'price.amount.KWh.NOK.KR': point['price.amount.KWh.NOK.KR'],
                                'price.amount.KWh.NOK.Ore': point['price.amount.KWh.NOK.Ore']
                            }
                            writer.writerow(row)

except Exception as e:
    logging.error(f"Error under JSON to CSV conversion: {str(e)}")

#CSV to XLSX ================================================================================================= 
# Angi de gitte filnavnene du leter etter
target_filenames_csv = ['StromPriserSørlandetEURogNOKSone1.csv', 'StromPriserSørlandetEURogNOKSone2.csv',
                        'StromPriserSørlandetEURogNOKSone3.csv', 'StromPriserSørlandetEURogNOKSone4.csv',
                        'StromPriserSørlandetEURogNOKSone5.csv']

# Gå gjennom filene i mappen
try:
    for filename in os.listdir(folder_path):
        if filename in target_filenames_csv:            
            # Les CSV-dataene
            csv_path = os.path.join(folder_path, filename)
            df = pd.read_csv(csv_path, encoding="utf-8-sig")

            # Angi XLSX-filnavnet basert på CSV-filnavnet
            xlsx_filename = os.path.splitext(filename)[0] + '.xlsx'

            # Lagre DataFrame som XLSX-fil
            xlsx_path = os.path.join(folder_path, xlsx_filename)
            df.to_excel(xlsx_path, index=False, sheet_name=f"{timeString2}", engine="xlsxwriter")
except Exception as e:
    logging.error(f"{timeString2}-Error under CSV to XLSX convertion: {str(e)}")

# ###BLOKK MED KODE FOR Å LAGE NYE DATASETT UNDER mypackage_id. KOMMENTERES UT MED MINDRE DEN TRENGS FOR Å LAGE NYE DATASETT. OPPDATERER IKKE ALLEREDE EKSISTERENDE DATASETT
# ua = 'ckanapiexample/1.0 (+https://opencom.no)'
# mypackage_id = '7a65063c-7fbe-4926-82a5-bbcf074cba07'
# mysite = RemoteCKAN('https://opencom.no', apikey=ckanAPIKey, user_agent=ua)

# target_filenames_xlsx = ['StromPriserSørlandetEURogNOKSone1.xlsx', 'StromPriserSørlandetEURogNOKSone2.xlsx',
#                         'StromPriserSørlandetEURogNOKSone3.xlsx', 'StromPriserSørlandetEURogNOKSone4.xlsx',
#                         'StromPriserSørlandetEURogNOKSone5.xlsx']


# json_path = "StromPriserNorge\\"
# csv_path = "StromPriserNorge\\"
# xlsx_path = "StromPriserNorge\\"

# ###BLOKK MED KODE FOR Å LAGE NYE DATASETT UNDER mypackage_id. KOMMENTERES UT MED MINDRE DEN TRENGS FOR Å LAGE NYE DATASETT. OPPDATERER IKKE ALLEREDE EKSISTERENDE DATASETT
# # # Opprett en tom ordbok for å lagre filnavn, filtype og id for hver fil
# json_file_dict = {}
# csv_file_dict = {}
# xlsx_file_dict = {}

# # Loop gjennom alle JSON-filer i mappen
# for file in os.listdir(json_path):
#     if file in target_filenames_json:
#         filename, file_extension = os.path.splitext(file)
#         file_path = os.path.join(json_path, file)

#         # Last opp filen til CKAN
#         try:
#             result = mysite.action.resource_create(
#                 package_id=mypackage_id,
#                 name=filename,
#                 format=file_extension,
#                 upload=open(file_path, 'rb')
#             )
#             print(f'Successfully uploaded {filename}{file_extension} with id: {result["id"]}')
#             json_file_dict[filename + file_extension] = result["id"]
#         except Exception as e:
#             print(f'Error uploading {filename}{file_extension}: {e}')
#             logging.error(f'{timeString2}-Error uploading JSON file to opencom.no: {str(e)}')

# # Skriv ordboken til filen "json_resource_dict.json"
# with open("StromPriserNorge\\fileDicts\\json_resource_dict.json", 'w') as f:
#     json.dump(json_file_dict, f)

# # Loop gjennom alle CSV-filer i mappen
# for file in os.listdir(csv_path):
#     if file in target_filenames_csv:
#         filename, file_extension = os.path.splitext(file)
#         file_path = os.path.join(json_path, file)

#         # Last opp filen til CKAN
#         try:
#             result = mysite.action.resource_create(
#                 package_id=mypackage_id,
#                 name=filename,
#                 format=file_extension,
#                 upload=open(file_path, 'rb')
#             )
#             print(f'Successfully uploaded {filename}{file_extension} with id: {result["id"]}')
#             csv_file_dict[filename + file_extension] = result["id"]
#         except Exception as e:
#             print(f'Error uploading {filename}{file_extension}: {e}')
#             logging.error(f'{timeString2}-Error uploading JSON file to opencom.no: {str(e)}')

# # Skriv ordboken til filen "json_resource_dict.json"
# with open("StromPriserNorge\\fileDicts\\csv_resource_dict.json", 'w') as f:
#     json.dump(csv_file_dict, f)

# # Loop gjennom alle XLSX-filer i mappen
# for file in os.listdir(xlsx_path):
#     if file in target_filenames_xlsx:
#         filename, file_extension = os.path.splitext(file)
#         file_path = os.path.join(json_path, file)

#         # Last opp filen til CKAN
#         try:
#             result = mysite.action.resource_create(
#                 package_id=mypackage_id,
#                 name=filename,
#                 format=file_extension,
#                 upload=open(file_path, 'rb')
#             )
#             print(f'Successfully uploaded {filename}{file_extension} with id: {result["id"]}')
#             xlsx_file_dict[filename + file_extension] = result["id"]
#         except Exception as e:
#             print(f'Error uploading {filename}{file_extension}: {e}')
#             logging.error(f'{timeString2}-Error uploading JSON file to opencom.no: {str(e)}')

# # Skriv ordboken til filen "json_resource_dict.json"
# with open("StromPriserNorge\\fileDicts\\xlsx_resource_dict.json", 'w') as f:
#     json.dump(xlsx_file_dict, f)
# ##BLOKK MED KODE FOR Å LAGE NYE DATASETT UNDER mypackage_id. KOMMENTERES UT MED MINDRE DEN TRENGS FOR Å LAGE NYE DATASETT. OPPDATERER IKKE ALLEREDE EKSISTERENDE DATASETT


###BLOKK MED KODE FOR Å OPPDATERE DATASETT SOM ALLEREDE ER LAGET I CKAN================================================================================================
#Leser ifra FILTYPE_file_dict, som opprettes i det nye ressurser lagesi koden over, og oppdaterer de id'ene som finnes der. 
# with open("fileDicts\\json_resource_dict.json", 'r', encoding='utf-8') as f:
#     json_file_dict = json.load(f)

# for file_name, resource_id in json_file_dict.items():
#     try:
#         file_path = os.path.join(json_path, file_name)
#         result = mysite.action.resource_update(
#             id=resource_id,
#             format='json',
#             name=f"{file_name} {timeString2}-{tomorrow_str_2format}.json",
#             upload=open(file_path, 'rb')
#         )
#         print(f'Successfully updated resource with id: {result["id"]}')
#     except Exception as e:
#         print(f'Error updating resource with id {resource_id}: {e}')
#         logging.error(f'{timeString2}-Error updating resource with id {resource_id}: {str(e)}')

# #Oppdater CSV filer
# with open("fileDicts\\csv_resource_dict.json", 'r', encoding='utf-8') as f:
#     csv_file_dict = json.load(f)

# for file_name, resource_id in csv_file_dict.items():
#     try:
#         file_path = os.path.join(csv_path, file_name)
#         result = mysite.action.resource_update(
#             id=resource_id,
#             format='csv',
#             name=f"{file_name} {timeString2}-{tomorrow_str_2format}.csv",
#             upload=open(file_path, 'rb')
#         )
#         print(f'Successfully updated resource with id: {result["id"]}')
#     except Exception as e:
#         print(f'Error updating resource with id {resource_id}: {e}')
#         logging.error(f'{timeString2}-Error updating resource with id {resource_id}: {str(e)}')

# #Oppdater XLSX filer
# with open("fileDicts\\xlsx_resource_dict.json", 'r', encoding='utf-8') as f:
#     xlsx_file_dict = json.load(f)

# for file_name, resource_id in xlsx_file_dict.items():
#     try:
#         file_path = os.path.join(xlsx_path, file_name)
#         result = mysite.action.resource_update(
#             id=resource_id,
#             format='xlsx',
#             name=f"{file_name} {timeString2}-{tomorrow_str_2format}.xlsx",
#             upload=open(file_path, 'rb')
#         )
#         print(f'Successfully updated resource with id: {result["id"]}')
#     except Exception as e:
#         print(f'Error updating resource with id {resource_id}: {e}')
#         logging.error(f'{timeString2}-Error updating resource with id {resource_id}: {str(e)}')

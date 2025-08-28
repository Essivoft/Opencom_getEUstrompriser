# EU Strømpriser Norge

Dette prosjektet henter strømprisdata fra ENTSO-E Transparency Platform for de norske strømsonene og publiserer dataene i ulike formater (JSON, CSV, XLSX) til et CKAN-datasett.

## 📋 Oversikt

Prosjektet består av flere Python-skript som:
- Henter timebaserte strømpriser fra ENTSO-E API for alle 5 norske strømsoner
- Konverterer prisdata fra EUR til NOK ved hjelp av valutakurser fra ECB
- Lagrer dataene i flere formater (XML, JSON, CSV, XLSX)
- Publiserer dataene til et CKAN-datasett for offentlig tilgang

## 🗺️ Norske Strømsoner

Prosjektet henter data for alle 5 norske strømsoner:

- **Sone 1**: Østlandet og Nordvestlandet (`10YNO-1--------2`)
- **Sone 2**: Sørvestlandet (`10YNO-2--------T`) 
- **Sone 3**: Midt-Norge (`10YNO-3--------J`)
- **Sone 4**: Nord-Norge (`10YNO-4--------9`)
- **Sone 5**: Vestlandet (`10Y1001A1001A48H`)

## 📁 Prosjektstruktur

```
EUStrompriser/
├── getEUstrompriser.py        # Hovedskript som henter alle strømpriser
├── getExchangeNOK.py          # Henter valutakurser EUR/NOK fra ECB
├── hentKursFraNorgesBank.py   # Alternativ valutakurs fra Norges Bank
├── jsonToCSV.py               # Konverterer JSON til CSV-format
├── eurofxref.csv              # Valutakursdata fra ECB
├── StromPriserNorge/          # Mappe med genererte datafiler
│   ├── *.json                 # JSON-filer for hver sone
│   ├── *.xml                  # Rå XML-data fra ENTSO-E
│   ├── *.csv                  # CSV-filer med pris i EUR og NOK
│   ├── *.xlsx                 # Excel-filer
│   └── fileDicts/             # Metadata for CKAN-opplasting
└── StromPriserNorgeErrors/    # Loggfiler for feilhåndtering
```

## 🛠️ Installasjon

### Forutsetninger

- Python 3.7+
- ENTSO-E Transparency Platform API-nøkkel
- CKAN API-nøkkel (hvis du vil publisere data)

### Nødvendige pakker

```bash
pip install requests pandas ckanapi currency-converter openpyxl
```

### API-nøkler

1. **ENTSO-E API-nøkkel**: Registrer deg på [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/) og få din `securityToken`
2. **CKAN API-nøkkel**: Få tilgang til ditt CKAN-datasett

## ⚙️ Konfigurasjon

Rediger `getEUstrompriser.py` og oppdater følgende variabler:

```python
# ENTSO-E API konfigurasjon
headers = {
    "securityToken" : "DIN_ENTSO_E_API_NOKKEL"
}

# CKAN konfigurasjon  
ckanAPIKey = 'DIN_CKAN_API_NOKKEL'
```

## 🚀 Bruk

### Kjør hovedskriptet

```bash
python getEUstrompriser.py
```

Dette vil:
1. Hente valutakurser fra ECB
2. Hente strømprisdata fra ENTSO-E for alle 5 norske soner
3. Konvertere XML til JSON-format
4. Beregne priser i NOK basert på EUR-kursen
5. Generere CSV og XLSX-filer
6. Laste opp dataene til CKAN

### Kjør individuelle skript

```bash
# Kun hente valutakurser
python getExchangeNOK.py

# Konvertere eksisterende JSON til CSV
python jsonToCSV.py

# Hente valutakurser fra Norges Bank (alternativ)
python hentKursFraNorgesBank.py
```

## 📊 Dataformat

### JSON-struktur

```json
{
    "currency_Unit.name": "EUR",
    "price_Measure_Unit.name": "MWh",
    "Period": {
        "timeInterval": {
            "start": "2024-10-18T22:00Z",
            "end": "2024-10-19T22:00Z"
        },
        "resolution": "PT60M",
        "Points": [
            {
                "position": "1",
                "price.amount": "45.67",
                "price.amount.MWh.EUR": "45.67",
                "price.amount.KWh.EUR": "0.04567",
                "price.amount.KWh.EUR.Cent": "4.567",
                "price.amount.MWh.NOK": "512.34",
                "price.amount.KWh.NOK.KR": "0.51234",
                "price.amount.KWh.NOK.Ore": "51.234"
            }
        ]
    }
}
```

### CSV-kolonner

- `start`: Startdato for tidsperioden
- `end`: Sluttdato for tidsperioden  
- `position`: Timeposisjon (1-24)
- `price.amount.MWh.EUR`: Pris per MWh i EUR
- `price.amount.KWh.EUR`: Pris per kWh i EUR
- `price.amount.KWh.EUR.Cent`: Pris per kWh i EUR-cent
- `price.amount.MWh.NOK`: Pris per MWh i NOK
- `price.amount.KWh.NOK.KR`: Pris per kWh i NOK kroner
- `price.amount.KWh.NOK.Ore`: Pris per kWh i NOK øre

## 🔧 Feilhåndtering

Alle feil logges til `StromPriserNorgeErrors/StromPriserNorgeErrors.log` med:
- Tidsstempel
- Feilnivå
- Detaljert feilbeskrivelse

## 📅 Tidsintervaller

Skriptet henter data for:
- **Fra**: I dag klokka 00:00
- **Til**: I morgen klokka 00:00

Dette gir 24 timers prognosedata for kommende dag.

## 🌐 Datakilder

- **Strømpriser**: [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/)
- **Valutakurser**: [European Central Bank](https://www.ecb.europa.eu/stats/eurofxref/)
- **Alternativ valutakurs**: [Norges Bank](https://data.norges-bank.no/)

## 📄 Lisens

Dette prosjektet er utviklet for Stavanger kommune for å gjøre strømprisdata tilgjengelig for allmennheten.

## 🤝 Bidrag

For spørsmål eller forbedringer, kontakt utvikler eller opprett en issue.

## ⚠️ Merknader

- API-nøkler må holdes konfidensielle
- ENTSO-E har rategrenser på API-kall
- Valutakurser oppdateres daglig av ECB
- Data publiseres automatisk til CKAN ved vellykket kjøring

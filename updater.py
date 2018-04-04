from freshsales import FreshsalesAnalytics
import requests as r

api_file = open("secrets/apiKey", "r")
apiKey = api_file.read()

freshsales = FreshsalesAnalytics("https://dragonveterinary.freshsales.io", apiKey)

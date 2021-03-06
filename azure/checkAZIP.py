#!/usr/bin/env python3
import requests
import subprocess
import sys
import yaml

CONFIG_YML= 'checkAZIP.yml'

with open (CONFIG_YML, 'r') as ymlfile:
  cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

ip = sys.argv[1]

token = subprocess.Popen("az account get-access-token -o=yaml | grep accessToken | sed -e 's/accessToken: //g'", stdout=subprocess.PIPE, universal_newlines=True, shell=True ).communicate()[0].strip()
auth = {'Authorization': "Bearer " + str(token) }
URL = "https://management.azure.com/subscriptions/" + cfg['subscription'] + "/resourceGroups/" + cfg['rg'] + "/providers/Microsoft.Network/virtualNetworks/" + cfg['vnet'] + "/CheckIPAddressAvailability?api-version=2020-07-01&ipAddress=" + ip

r = requests.get(url = URL, headers=auth)

print(r.text)

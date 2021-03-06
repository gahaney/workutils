#!/usr/bin/env python3
import requests
import sys
import os.path
from os import path
import yaml
import argparse

CONFIG_YML = 'builds.yml'
API = '/rest/build-status/1.0/commits/'

user = None
commit = None
host = None
port = None 

if path.exists(CONFIG_YML):
  with open (CONFIG_YML, 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
  if 'User' in cfg.keys(): user = cfg['User']
  if 'Server' in cfg.keys():
    if 'Hostname' in cfg['Server'].keys(): host = cfg['Server']['Hostname']
    if 'Port' in cfg['Server'].keys(): port = cfg['Server']['Port']

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', default='', help='User name')
parser.add_argument('-c', '--commit', default='', help='Commit sha')
parser.add_argument('-H', '--host', default='', help='Host')
parser.add_argument('-p', '--port', default='', help='Port')
args = parser.parse_args()

if args.user: user=args.user
if args.host: host=args.host
if args.port: port=args.port
if args.commit: commit=args.commit

if user==None or host==None or commit==None:
    if user==None: print('You must specify a user.') 
    if host==None: print('You must specify a host.')
    if commit==None: print('You must specify a commit.')
    exit()

os.system("stty -echo")
password = input("Enter your password: ")
os.system("stty echo")
print()

url = 'https://' + host
if port!=None: url += ':' + str(port)
url += API + commit
r = requests.get(url = url, auth=(user, password))
builds = r.json()


for build in range(len(builds["values"])):
    print("----------")
    print("Build #....", build)
    print("State......: ",builds["values"][build]["state"])
    print("Name.......: ",builds["values"][build]["name"])
    print("URL........: ",builds["values"][build]["url"])
    print("Description: ",builds["values"][build]["description"])

print("----------\n")
choice = input("Enter build number to update: ")

data = { 'key': builds["values"][int(choice)]["key"],
         'name': builds["values"][int(choice)]["name"],
         'url': builds["values"][int(choice)]["url"],
         'description': builds["values"][int(choice)]["description"],
         'state': 'SUCCESSFUL' }
       
p = requests.post(url = url, auth=(user, password), json = data)
print("Success: ",p.ok)

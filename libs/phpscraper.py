import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests
import json
import re
import random
import urllib
from lxml import html

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'}

def build_list(_pid, _handle, addon, action, title, link):
  xbmcplugin.setPluginCategory(_handle, title)

  listitem = xbmcgui.ListItem(label=' Refresh list')
  listitem.setInfo('video', {'title': ' Refresh list', 'mediatype': 'video'})
  data = {
      "provider": "phpscraper",
      "action": action,
      "title": title,
      "link": link
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  hosts = ['syco.netsons.org']

  link = "http://{}/scrapers/acestream/?action={}&link={}".format(random.choice(hosts), urllib.quote(action), urllib.quote(link))
  xbmc.log(link, xbmc.LOGNOTICE)

  page = requests.get(link, headers=headers).content
  xbmc.log(page, xbmc.LOGNOTICE)

  phpscrapers = json.loads(page)
  for phpscraper in phpscrapers:
    listitem = xbmcgui.ListItem(label=phpscraper['title'])
    listitem.setInfo('video', {'title': phpscraper['title'], 'mediatype': 'video'})
    if phpscraper['action'] == "ace":
      listitem.setProperty('IsPlayable', 'true')
      data = {
          "action": "play",
          "video" : 'http://{0}:{1}/ace/manifest.m3u8?id={2}'.format(addon.getSetting('ace_host'), addon.getSetting('ace_port'), phpscraper['link'])
          }
      xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=False)
    else:
      data = {
          "provider": "phpscraper",
          "action": phpscraper['action'],
          "title": phpscraper['title'],
          "link": phpscraper['link']
          }
      xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
  xbmcplugin.endOfDirectory(_handle)

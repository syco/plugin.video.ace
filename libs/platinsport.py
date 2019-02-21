import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests
import json
import re
import urllib
from lxml import html
from urlparse import parse_qsl
from datetime import datetime, timedelta

headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36'}


def build_list0(_pid, _handle, addon, title):
  xbmcplugin.setPluginCategory(_handle, title)

  listitem = xbmcgui.ListItem(label=' Refresh list')
  listitem.setInfo('video', {'title': ' Refresh list', 'mediatype': 'video'})
  data = {
      "provider": "platinsport",
      "action": "list0",
      "title": "PlatinSport"
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  page = requests.get('http://www.platinsport.com/', headers=headers).content
  tree = html.fromstring(page)

  for item in tree.xpath('//article[@class="item-list"]'):
    try:
      date = item.xpath('./h2[@class="post-box-title"]/a')[0].text_content().encode('utf-8').strip()
      for row in tree.xpath('.//tr'):
        title = date[0:10] + ' ' + row.xpath('.//td[2]')[0].text_content().encode('utf-8').strip()
        url = row.xpath('.//td[3]/a')[0].get('href').encode('utf-8').strip()
        listitem = xbmcgui.ListItem(label=title)
        listitem.setInfo('video', {'title': title, 'mediatype': 'video'})
        data = {
            "provider": "platinsport",
            "action": "list1",
            "title" : title,
            "url" : url[20:]
            }
        xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)
    except Exception as ex:
      xbmc.log(html.tostring(item), xbmc.LOGERROR)
      xbmc.log(str(ex), xbmc.LOGERROR)
  xbmcplugin.endOfDirectory(_handle)

def build_list1(_pid, _handle, addon, title, url):
  xbmcplugin.setPluginCategory(_handle, title)

  listitem = xbmcgui.ListItem(label=' Refresh List')
  listitem.setInfo('video', {'title': ' Refresh List', 'mediatype': 'video'})
  data = {
      "provider": "platinsport",
      "action": "list1",
      "title" : title,
      "url" : url
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  added = []

  pattern = re.compile(r'acestream:\/\/([0-z]{40})', re.IGNORECASE)
  page = requests.get(url, headers=headers).content
  for m in re.finditer(pattern, page):
    a_url = m.group(1)
    if a_url in added:
      continue
    added.append(a_url)
    listitem = xbmcgui.ListItem(label=title)
    listitem.setInfo('video', {'title': title, 'mediatype': 'video'})
    listitem.setProperty('IsPlayable', 'true')
    data = {
        "action": "play",
        "video" : 'http://{0}:{1}/ace/manifest.m3u8?id={2}'.format(addon.getSetting('ace_host'), addon.getSetting('ace_port'), a_url)
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=False)

  xbmcplugin.endOfDirectory(_handle)


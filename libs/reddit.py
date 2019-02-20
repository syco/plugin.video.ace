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

headers_mobile = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36'
    }
headers_desktop = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
    }


def build_list0(_pid, _handle, addon, title, subs):
  xbmcplugin.setPluginCategory(_handle, title)
  for data in subs:
    listitem = xbmcgui.ListItem(label=data['title'])
    listitem.setInfo('video', {'title': data['title'], 'mediatype': 'video'})
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  xbmcplugin.endOfDirectory(_handle)

def build_list1(_pid, _handle, addon, title, sub, sep):
  xbmcplugin.setPluginCategory(_handle, title)

  listitem = xbmcgui.ListItem(label=' Refresh List')
  listitem.setInfo('video', {'title': ' Refresh List', 'mediatype': 'video'})
  data = {
      "provider": "reddit",
      "action": "list1",
      "title": title,
      "sub": sub,
      "sep": sep
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  plus = ""
  while True:
    page = requests.get('https://www.reddit.com/r/{0}.json{1}'.format(sub, plus), headers=headers_mobile).content
    js = json.loads(page)
    for t3 in js["data"]["children"]:
      title = t3["data"]["title"].encode('utf-8').strip()
      if title.lower().find(sep) != -1:
        title2 = "{0}, by {1}".format(title, t3["data"]["author"].encode('utf-8').strip())
        url2 = t3["data"]["url"].encode('utf-8').strip()
        listitem = xbmcgui.ListItem(label=title)
        listitem.setInfo('video', {'title': title, 'mediatype': 'video'})
        data = {
            "provider": "reddit",
            "action": "list2",
            "title": title,
            "url": url2
            }
        xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)
    after = js["data"]["after"]
    if after is None:
      break
    else:
      plus = "?after=" + after
  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
  xbmcplugin.endOfDirectory(_handle)

def findAllData(js, ks):
  arr = []
  if isinstance(js, dict):
    for k in js:
      if k == ks and "body" in js[k]:
        arr.append(js[k])
      arr.extend(findAllData(js[k], ks))
  elif isinstance(js, list):
    for sjs in js:
      arr.extend(findAllData(sjs, ks))
  return arr

def build_list2(_pid, _handle, addon, title, url):
  xbmcplugin.setPluginCategory(_handle, title)

  listitem = xbmcgui.ListItem(label=' Refresh List')
  listitem.setInfo('video', {'title': ' Refresh List', 'mediatype': 'video'})
  data = {
      "provider": "reddit",
      "action": "list2",
      "title": title,
      "url": url
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  pattern = re.compile(r'((?:\[[^\[\]]+\]\s+)*)acestream:\/\/([0-z]{40})((?:\s+\[[^\[\]]+\])*)', re.IGNORECASE)
  plus = ""
  while True:
    page = requests.get(url[:-1] + ".json" + plus, headers=headers_mobile).content
    js = json.loads(page)
    arr = findAllData(js, "data")
    for t3 in arr:
      for m in re.finditer(pattern, t3["body"]):
        acedesc = "{0} - {1}{2} by {3}".format(m.group(2), m.group(1), m.group(3), t3["author"])
        listitem = xbmcgui.ListItem(label=acedesc)
        listitem.setInfo('video', {'title': acedesc, 'mediatype': 'video'})
        listitem.setProperty('IsPlayable', 'true')
        data = {
            "action": "play",
            "video" : 'http://{0}:{1}/ace/manifest.m3u8?id={2}'.format(addon.getSetting('ace_host'), addon.getSetting('ace_port'), m.group(2))
            }
        xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=False)
    after = js[0]["data"]["after"]
    if after is None:
      break
    else:
      plus = "?after=" + after
  xbmcplugin.endOfDirectory(_handle)


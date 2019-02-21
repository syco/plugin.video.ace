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

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'}


def build_list0(_pid, _handle, addon, title):
  xbmcplugin.setPluginCategory(_handle, title)

  listitem = xbmcgui.ListItem(label=' Refresh list')
  listitem.setInfo('video', {'title': ' Refresh list', 'mediatype': 'video'})
  data = {
      "provider": "livetvsx",
      "action": "list0",
      "title": "LiveTV.sx"
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  page = requests.get('http://livetv.sx/enx/allupcoming/', headers=headers).content
  tree = html.fromstring(page)

  for item in tree.xpath('//div[@id="aul"]//a[@class="main"][not(img)]'):
    try:
      xbmc.log(html.tostring(item), xbmc.LOGNOTICE)
      title = item.text_content().encode('utf-8').strip()
      if title != '':
        url = item.get('href').encode('utf-8').strip()
        listitem = xbmcgui.ListItem(label=title)
        listitem.setInfo('video', {'title': title, 'mediatype': 'video'})
        data = {
            "provider": "livetvsx",
            "action": "list1",
            "title" : title,
            "url" : 'http://livetv.sx{0}'.format(url)
            }
        xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)
    except Exception as ex:
      xbmc.log(html.tostring(item), xbmc.LOGERROR)
      xbmc.log(str(ex), xbmc.LOGERROR)
  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
  xbmcplugin.endOfDirectory(_handle)

def build_list1(_pid, _handle, addon, title, url):
  xbmcplugin.setPluginCategory(_handle, title)

  listitem = xbmcgui.ListItem(label=' Refresh List')
  listitem.setInfo('video', {'title': ' Refresh List', 'mediatype': 'video'})
  data = {
      "provider": "livetvsx",
      "action": "list1",
      "title" : title,
      "url" : url
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  page = requests.get(url, headers=headers).content
  tree = html.fromstring(page)

  added = []

  for item in tree.xpath('//img[@src="//cdn.livetvcdn.net/img/live.gif"]/parent::*/a'):
    try:
      xbmc.log(html.tostring(item), xbmc.LOGNOTICE)
      title = item.text_content().encode('utf-8').strip()
      if title != '':
        url = item.get('href').encode('utf-8').strip()
        if url in added:
          continue
        added.append(url)
        listitem = xbmcgui.ListItem(label=title)
        listitem.setInfo('video', {'title': title, 'mediatype': 'video'})
        data = {
            "provider": "livetvsx",
            "action": "list2",
            "title" : title,
            "url" : 'http://livetv.sx{0}'.format(url)
            }
        xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)
    except Exception as ex:
      xbmc.log(html.tostring(item), xbmc.LOGERROR)
      xbmc.log(str(ex), xbmc.LOGERROR)
  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
  xbmcplugin.endOfDirectory(_handle)

def build_list2(_pid, _handle, addon, title, url):
  xbmcplugin.setPluginCategory(_handle, title)

  listitem = xbmcgui.ListItem(label=' Refresh List')
  listitem.setInfo('video', {'title': ' Refresh List', 'mediatype': 'video'})
  data = {
      "provider": "livetvsx",
      "action": "list2",
      "title" : title,
      "url" : url
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  page = requests.get(url, headers=headers).content
  tree = html.fromstring(page)

  for item in tree.xpath('//a[starts-with(@href, "acestream://")]/parent::*/parent::*'):
    try:
      ptitle = item.xpath('./td/img')[0].get('title').encode('utf-8').strip()
      purl = item.xpath('./td[7]/a')[0].get('href').encode('utf-8').strip()
      xbmc.log(purl, xbmc.LOGNOTICE)
      listitem = xbmcgui.ListItem(label=ptitle)
      listitem.setInfo('video', {'title': ptitle, 'mediatype': 'video'})
      listitem.setProperty('IsPlayable', 'true')
      data = {
          "action": "play",
          "video" : 'http://{0}:{1}/ace/manifest.m3u8?id={2}'.format(addon.getSetting('ace_host'), addon.getSetting('ace_port'), purl)
          }
      xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=False)
    except Exception as ex:
      xbmc.log(html.tostring(item), xbmc.LOGERROR)
      xbmc.log(str(ex), xbmc.LOGERROR)
  xbmcplugin.endOfDirectory(_handle)


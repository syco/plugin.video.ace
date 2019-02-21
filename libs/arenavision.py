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


def build_list0(_pid, _handle, addon, title):
  xbmcplugin.setPluginCategory(_handle, title)

  listitem = xbmcgui.ListItem(label=' Refresh List')
  listitem.setInfo('video', {'title': ' Refresh List', 'mediatype': 'video'})
  data = {
      "provider": "arenavision",
      "action": "list0",
      "title": "Arenavision"
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  today = '{:%d/%m/%Y}'.format(datetime.utcnow())
  tomorrow = '{:%d/%m/%Y}'.format(datetime.utcnow() + timedelta(days=1))
  page = requests.get('http://arenavision.in/guide', cookies={'Cookie': 'beget=begetok; expires=' + ('{:%a, %d %b %Y %H:%M:%S GMT}'.format(datetime.utcnow() + timedelta(seconds=19360000))) + '; path=/'}, headers=headers_mobile).content
  tree = html.fromstring(page)
  pattern = re.compile(r'([0-9-]+)\W*([A-Z]+)', re.IGNORECASE)

  for item in tree.xpath('//tr[count(./td)>=6]'):
    try:
      av_date = item.xpath('./td[1]')[0].text_content().encode('utf-8').strip()
      if today != av_date and tomorrow !=av_date:
        continue
      av_time = item.xpath('./td[2]')[0].text_content().encode('utf-8').strip()
      av_sport = item.xpath('./td[3]')[0].text_content().encode('utf-8').strip()
      av_tournament = item.xpath('./td[4]')[0].text_content().encode('utf-8').strip()
      av_match = item.xpath('./td[5]')[0].text_content().encode('utf-8').strip()
      av_langs = '' 
      urls = []
      for t1 in item.xpath('./td[6]'):
        m = re.match(pattern, t1.text)
        av_langs = av_langs + ' ' + m.group(2)
        for c in m.group(1).split('-'):
          c = c.strip()
          if c[0] == 'W':
            urls.append(m.group(2) + ' ' + c + '!' + (tree.xpath('//a[text()="World Cup ' + c[1:] + '"]')[0]).get('href'))
          else:
            urls.append(m.group(2) + ' ' + c + '!' + (tree.xpath('//a[text()="ArenaVision ' + c + '"]')[0]).get('href'))
      title = av_date + ' ' + av_time + ' | ' + av_sport + ' | ' + av_tournament + ' | ' + av_match + ' |' + av_langs
      listitem = xbmcgui.ListItem(label=title)
      listitem.setInfo('video', {'title': title, 'mediatype': 'video'})
      data = {
          "provider": "arenavision",
          "action": "list1",
          "title" : title,
          "url" : urls
          }
      xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)
    except Exception as ex:
      xbmc.log(html.tostring(item), xbmc.LOGERROR)
      xbmc.log(str(ex), xbmc.LOGERROR)

  xbmcplugin.endOfDirectory(_handle)

def build_list1(_pid, _handle, addon, title, urls):
  xbmcplugin.setPluginCategory(_handle, title)

  listitem = xbmcgui.ListItem(label=' Refresh List')
  listitem.setInfo('video', {'title': ' Refresh List', 'mediatype': 'video'})
  data = {
      "provider": "arenavision",
      "action": "list1",
      "title" : title,
      "url" : urls
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  pattern = re.compile(r'acestream:\/\/([0-z]{40})', re.IGNORECASE)
  for r in urls:
    t = r.split('!')
    page = requests.get(t[1], cookies={'Cookie': 'beget=begetok; expires=' + ('{:%a, %d %b %Y %H:%M:%S GMT}'.format(datetime.utcnow() + timedelta(seconds=19360000))) + '; path=/'}, headers=headers_mobile).content
    for m in re.finditer(pattern, page):
      listitem = xbmcgui.ListItem(label=t[0])
      listitem.setInfo('video', {'title': t[0], 'mediatype': 'video'})
      listitem.setProperty('IsPlayable', 'true')
      data = {
          "action": "play",
          "video" : 'http://{0}:{1}/ace/manifest.m3u8?id={2}'.format(addon.getSetting('ace_host'), addon.getSetting('ace_port'), m.group(1))
          }
      xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=False)
  xbmcplugin.endOfDirectory(_handle)


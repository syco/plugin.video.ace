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
      "provider": "livefootballol",
      "action": "list0",
      "title": "Live Football OL"
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  page = requests.get('https://www.livefootballol.me/acestream-channel-list-2017.html', headers=headers_desktop).content
  tree = html.fromstring(page)

  for item in tree.xpath('//table[@class="uk-table uk-table-hover uk-table-striped"]/tr'):
    try:
      lf_title = item.xpath('./td[2]')[0].text_content().encode('utf-8').strip()
      lf_link = item.xpath('./td[3]')[0].text_content().encode('utf-8').strip()
      lf_lang = item.xpath('./td[4]')[0].text_content().encode('utf-8').strip()
      lf_kbps = item.xpath('./td[5]')[0].text_content().encode('utf-8').strip()

      lf_title2 = lf_title + ' [' + lf_lang + ' ~ ' + lf_kbps + ']'
      listitem = xbmcgui.ListItem(label=lf_title2)
      listitem.setInfo('video', {'title': lf_title2, 'mediatype': 'video'})
      listitem.setProperty('IsPlayable', 'true')
      data = {
          "action": "play",
          "video" : 'http://{0}:{1}/ace/manifest.m3u8?id={2}'.format(addon.getSetting('ace_host'), addon.getSetting('ace_port'), lf_link)
          }
      xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=False)
    except Exception as ex:
      xbmc.log('ERROR: {}'.format(html.tostring(item)), xbmc.LOGERROR)
      xbmc.log('ERROR: {}'.format(str(ex)), xbmc.LOGERROR)
  xbmcplugin.endOfDirectory(_handle)


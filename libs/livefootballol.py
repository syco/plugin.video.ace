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

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'}

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

  pages = ['https://www.livefootballol.me/channels/']
  for i in range(2, 10):
    pages.append("https://www.livefootballol.me/channels/page-{}.html".format(i))
  try:
    for purl in pages:
      page = requests.get(purl, headers=headers).content
      #xbmc.log(page, xbmc.LOGNOTICE)
      tree = html.fromstring(page)

      for item in tree.xpath('//table[@class="uk-table uk-table-striped"]/*/tr/td/a'):
        lf_title = item.text_content().encode('utf-8').strip()
        if "bulgaria" in lf_title.lower():
          continue
        if "czech" in lf_title.lower():
          continue
        if "germany" in lf_title.lower():
          continue
        if "hungary" in lf_title.lower():
          continue
        if "jazeera" in lf_title.lower():
          continue
        if "russia" in lf_title.lower():
          continue
        if "serbia" in lf_title.lower():
          continue
        if "sopcast" in lf_title.lower():
          continue
        xbmc.log(lf_title, xbmc.LOGNOTICE)
        lf_link = "https://www.livefootballol.me" + item.get('href').encode('utf-8').strip()
        xbmc.log(lf_link, xbmc.LOGNOTICE)

        listitem = xbmcgui.ListItem(label=lf_title)
        listitem.setInfo('video', {'title': lf_title, 'mediatype': 'video'})
        data = {
            "provider": "livefootballol",
            "action": "list1",
            "title" : lf_title,
            "url" : lf_link
            }
        xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)
  except Exception as ex:
    xbmc.log(html.tostring(item), xbmc.LOGERROR)
    xbmc.log(str(ex), xbmc.LOGERROR)
  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
  xbmcplugin.endOfDirectory(_handle)

def build_list1(_pid, _handle, addon, title, url):
  xbmcplugin.setPluginCategory(_handle, title)

  xbmc.log(url, xbmc.LOGNOTICE)
  pattern = re.compile(r'acestream:\/\/([0-z]{40})', re.IGNORECASE)
  page = requests.get(url, headers=headers).content
  tree = html.fromstring(page)

  items = tree.xpath('//table[@class="uk-table"]/*/tr/td');

  lf_title = items[2].text_content().encode('utf-8').strip()
  lf_brate = items[4].text_content().encode('utf-8').strip()
  lf_lang = items[8].text_content().encode('utf-8').strip()

  lf_title2 = lf_title + " [" + lf_lang + " @ " + lf_brate + "]"

  added = []

  for m in re.finditer(pattern, page):
    a_url = m.group(1)
    if a_url in added:
      continue
    added.append(a_url)
    xbmc.log(a_url, xbmc.LOGNOTICE)
    listitem = xbmcgui.ListItem(label=lf_title2)
    listitem.setInfo('video', {'title': lf_title2, 'mediatype': 'video'})
    listitem.setProperty('IsPlayable', 'true')
    data = {
        "action": "play",
        "video" : 'http://{0}:{1}/ace/manifest.m3u8?id={2}'.format(addon.getSetting('ace_host'), addon.getSetting('ace_port'), a_url)
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=False)
  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
  xbmcplugin.endOfDirectory(_handle)

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

from libs import phpscraper

# https://forum.kodi.tv/showthread.php?tid=324570

addon = xbmcaddon.Addon()

_pid = sys.argv[0]
_handle = int(sys.argv[1])



def list_categories():
  xbmcplugin.setPluginCategory(_handle, 'ACE')
  xbmcplugin.setContent(_handle, 'videos')

  listitem = xbmcgui.ListItem(label=' Refresh List')
  listitem.setInfo('video', {'title': ' Refresh List', 'mediatype': 'video'})
  xbmcplugin.addDirectoryItem(handle=_handle, url=_pid, listitem=listitem, isFolder=True)

  listitem = xbmcgui.ListItem(label="PHP Scrapers")
  listitem.setInfo('video', {'title': "PHP Scrapers", 'mediatype': 'video'})
  data = {
      "provider": 'phpscraper',
      "action": "list",
      "title": "PHP Scrapers",
      "link": ""
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  for tmp in addon.getSetting('acestreamsearch_terms').split(","):
    listitem = xbmcgui.ListItem(label='ASS {}'.format(tmp))
    listitem.setInfo('video', {'title': 'ASS {}'.format(tmp), 'mediatype': 'video'})
    data = {
        "provider": 'phpscraper',
        "action": "acestreamsearch-search-0",
        "title": 'ASS {}'.format(tmp),
        "link": tmp
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  xbmcplugin.endOfDirectory(_handle)



def play_video(path):
  xbmcplugin.setResolvedUrl(_handle, True, listitem=xbmcgui.ListItem(path=path))



xbmc.log(" ".join(sys.argv), xbmc.LOGNOTICE)



def router(paramstring):
  try:
    params = json.loads(urllib.unquote(paramstring[5:]))
  except Exception as e:
    xbmc.log("type error: " + str(e), xbmc.LOGERROR)
    params = False

  if params:
    if params['action'] == 'play':
      play_video(params['video'])

    elif params['provider'] == 'phpscraper':
      try:
        phpscraper.build_list(_pid, _handle, addon, params['action'], params['title'], params['link'])
      except Exception as e:
        xbmc.log("type error: " + str(e), xbmc.LOGERROR)

  else:
    list_categories()

if __name__ == '__main__':
  router(sys.argv[2][1:])

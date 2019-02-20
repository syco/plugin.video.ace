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

from libs import livefootballol
from libs import arenavision
from libs import livetvsx
from libs import platinsport
from libs import reddit

# https://forum.kodi.tv/showthread.php?tid=324570

addon = xbmcaddon.Addon()

_pid = sys.argv[0]
_handle = int(sys.argv[1])
headers_mobile = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36'
    }
headers_desktop = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
    }



def list_categories():
  xbmcplugin.setPluginCategory(_handle, 'ACE')
  xbmcplugin.setContent(_handle, 'videos')

  listitem = xbmcgui.ListItem(label=' Refresh List')
  listitem.setInfo('video', {'title': ' Refresh List', 'mediatype': 'video'})
  xbmcplugin.addDirectoryItem(handle=_handle, url=_pid, listitem=listitem, isFolder=True)

  if addon.getSetting('show_livefootballol') == "true":
    listitem = xbmcgui.ListItem(label='Live Football OL')
    listitem.setInfo('video', {'title': 'Live Football OL', 'mediatype': 'video'})
    data = {
        "provider": "livefootballol",
        "action": "list0",
        "title": "Live Football OL"
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  if addon.getSetting('show_arenavision') == "true":
    listitem = xbmcgui.ListItem(label='Arenavision')
    listitem.setInfo('video', {'title': 'Arenavision', 'mediatype': 'video'})
    data = {
        "provider": "arenavision",
        "action": "list0",
        "title": "Arenavision"
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  if addon.getSetting('show_livetvsx') == "true":
    listitem = xbmcgui.ListItem(label='LiveTV.sx')
    listitem.setInfo('video', {'title': 'LiveTV.sx', 'mediatype': 'video'})
    data = {
        "provider": "livetvsx",
        "action": "list0",
        "title": "LiveTV.sx"
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  if addon.getSetting('show_platinsport') == "true":
    listitem = xbmcgui.ListItem(label='Platinsport')
    listitem.setInfo('video', {'title': 'Platinsport', 'mediatype': 'video'})
    data = {
        "provider": "platinsport",
        "action": "list0",
        "title": "PlatinSport"
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  #if addon.getSetting('show_reddit_boxing') == "true":
  #  listitem = xbmcgui.ListItem(label='Reddit Boxing')
  #  listitem.setInfo('video', {'title': 'Reddit Boxing', 'mediatype': 'video'})
  #  data = {
  #      "provider": "reddit",
  #      "action": "list1",
  #      "title": "Reddit Boxing",
  #      "sub": "boxingstreams",
  #      "sep": " vs"
  #      }
  #  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  #if addon.getSetting('show_reddit_mma') == "true":
  #  listitem = xbmcgui.ListItem(label='Reddit MMA')
  #  listitem.setInfo('video', {'title': 'Reddit MMA', 'mediatype': 'video'})
  #  data = {
  #      "provider": "reddit",
  #      "action": "list1",
  #      "title": "Reddit MMA",
  #      "sub": "MMAStreams",
  #      "sep": " vs"
  #      }
  #  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  #if addon.getSetting('show_reddit_motorsports') == "true":
  #  listitem = xbmcgui.ListItem(label='Reddit MotorSports')
  #  listitem.setInfo('video', {'title': 'Reddit MotorSports', 'mediatype': 'video'})
  #  data = {
  #      "provider": "reddit",
  #      "action": "list1",
  #      "title": "Reddit MotorSports",
  #      "sub": "motorsportsstreams",
  #      "sep": " utc"
  #      }
  #  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  #if addon.getSetting('show_reddit_nba') == "true":
  #  listitem = xbmcgui.ListItem(label='Reddit NBA')
  #  listitem.setInfo('video', {'title': 'Reddit NBA', 'mediatype': 'video'})
  #  data = {
  #      "provider": "reddit",
  #      "action": "list1",
  #      "title": "Reddit NBA",
  #      "sub": "nbastreams",
  #      "sep": " @"
  #      }
  #  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  #if addon.getSetting('show_reddit_nfl') == "true":
  #  listitem = xbmcgui.ListItem(label='Reddit NFL')
  #  listitem.setInfo('video', {'title': 'Reddit NFL', 'mediatype': 'video'})
  #  data = {
  #      "provider": "reddit",
  #      "action": "list1",
  #      "title": "Reddit NFL",
  #      "sub": "nflstreams",
  #      "sep": " @"
  #      }
  #  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  #if addon.getSetting('show_reddit_soccer') == "true":
  #  listitem = xbmcgui.ListItem(label='Reddit Soccer')
  #  listitem.setInfo('video', {'title': 'Reddit Soccer', 'mediatype': 'video'})
  #  #data = {
  #  #    "provider": "reddit",
  #  #    "action": "list0",
  #  #    "title": "Reddit Soccer",
  #  #    "subs": [
  #  #      {
  #  #        "provider": "reddit",
  #  #        "action": "list1",
  #  #        "title": "/r/soccerstreams_other",
  #  #        "sub": "soccerstreams_other",
  #  #        "sep": " vs"
  #  #        },
  #  #      {
  #  #        "provider": "reddit",
  #  #        "action": "list1",
  #  #        "title": "/r/soccerstreams_pl",
  #  #        "sub": "soccerstreams_pl",
  #  #        "sep": " vs"
  #  #        }
  #  #      ]
  #  #    }
  #  data = {
  #      "provider": "reddit",
  #      "action": "list1",
  #      "title": "Reddit Soccer",
  #      "sub": "redditsoccer",
  #      "sep": " vs"
  #      }
  #  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

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

    elif params['provider'] == 'livefootballol':
      if params['action'] == 'list0':
        try:
          livefootballol.build_list0(_pid, _handle, addon, params['title'])
        except Exception as e:
          xbmc.log("type error: " + str(e), xbmc.LOGERROR)
      elif params['action'] == 'list1':
        livefootballol.build_list1(_pid, _handle, addon, params['title'], params['url'])

    elif params['provider'] == 'arenavision':
      if params['action'] == 'list0':
        try:
          arenavision.build_list0(_pid, _handle, addon, params['title'])
        except Exception as e:
          xbmc.log("type error: " + str(e), xbmc.LOGERROR)
      elif params['action'] == 'list1':
        arenavision.build_list1(_pid, _handle, addon, params['title'], params['url'])

    elif params['provider'] == 'livetvsx':
      if params['action'] == 'list0':
        livetvsx.build_list0(_pid, _handle, addon, params['title'])
      elif params['action'] == 'list1':
        livetvsx.build_list1(_pid, _handle, addon, params['title'], params['url'])
      elif params['action'] == 'list2':
        livetvsx.build_list2(_pid, _handle, addon, params['title'], params['url'])

    elif params['provider'] == 'platinsport':
      if params['action'] == 'list0':
        platinsport.build_list0(_pid, _handle, addon, params['title'])
      elif params['action'] == 'list1':
        platinsport.build_list1(_pid, _handle, addon, params['title'], params['url'])

    elif params['provider'] == 'reddit':
      if params['action'] == 'list0':
        reddit.build_list0(_pid, _handle, addon, params['title'], params['subs'])
      elif params['action'] == 'list1':
        reddit.build_list1(_pid, _handle, addon, params['title'], params['sub'], params['sep'])
      elif params['action'] == 'list2':
        reddit.build_list2(_pid, _handle, addon, params['title'], params['url'])
  else:
    list_categories()

if __name__ == '__main__':
  router(sys.argv[2][1:])

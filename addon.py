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

# https://forum.kodi.tv/showthread.php?tid=324570

addon = xbmcaddon.Addon()

_pid = sys.argv[0]
_handle = int(sys.argv[1])
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36',
    }



def list_categories():
  xbmcplugin.setPluginCategory(_handle, 'ACE')
  xbmcplugin.setContent(_handle, 'videos')

  listitem = xbmcgui.ListItem(label='Refresh List')
  listitem.setInfo('video', {'title': 'Refresh List', 'mediatype': 'video'})
  xbmcplugin.addDirectoryItem(handle=_handle, url=_pid, listitem=listitem, isFolder=True)

  if addon.getSetting('show_arenavision') == "true":
    listitem = xbmcgui.ListItem(label='Arenavision')
    listitem.setInfo('video', {'title': 'Arenavision', 'mediatype': 'video'})
    data = {
        "provider": "arenavision",
        "action": "list0",
        "title": "Arenavision"
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

  if addon.getSetting('show_reddit_boxing') == "true":
    listitem = xbmcgui.ListItem(label='Reddit Boxing')
    listitem.setInfo('video', {'title': 'Reddit Boxing', 'mediatype': 'video'})
    data = {
        "provider": "reddit",
        "action": "list1",
        "title": "Reddit Boxing",
        "sub": "boxingstreams",
        "sep": " vs"
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_mma') == "true":
    listitem = xbmcgui.ListItem(label='Reddit MMA')
    listitem.setInfo('video', {'title': 'Reddit MMA', 'mediatype': 'video'})
    data = {
        "provider": "reddit",
        "action": "list1",
        "title": "Reddit MMA",
        "sub": "MMAStreams",
        "sep": " vs"
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_motorsports') == "true":
    listitem = xbmcgui.ListItem(label='Reddit MotorSports')
    listitem.setInfo('video', {'title': 'Reddit MotorSports', 'mediatype': 'video'})
    data = {
        "provider": "reddit",
        "action": "list1",
        "title": "Reddit MotorSports",
        "sub": "motorsportsstreams",
        "sep": " utc"
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_nba') == "true":
    listitem = xbmcgui.ListItem(label='Reddit NBA')
    listitem.setInfo('video', {'title': 'Reddit NBA', 'mediatype': 'video'})
    data = {
        "provider": "reddit",
        "action": "list1",
        "title": "Reddit NBA",
        "sub": "nbastreams",
        "sep": " @"
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_nfl') == "true":
    listitem = xbmcgui.ListItem(label='Reddit NFL')
    listitem.setInfo('video', {'title': 'Reddit NFL', 'mediatype': 'video'})
    data = {
        "provider": "reddit",
        "action": "list1",
        "title": "Reddit NFL",
        "sub": "nflstreams",
        "sep": " @"
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_soccer') == "true":
    listitem = xbmcgui.ListItem(label='Reddit Soccer')
    listitem.setInfo('video', {'title': 'Reddit Soccer', 'mediatype': 'video'})
    #data = {
    #    "provider": "reddit",
    #    "action": "list0",
    #    "title": "Reddit Soccer",
    #    "subs": [
    #      {
    #        "provider": "reddit",
    #        "action": "list1",
    #        "title": "/r/soccerstreams_other",
    #        "sub": "soccerstreams_other",
    #        "sep": " vs"
    #        },
    #      {
    #        "provider": "reddit",
    #        "action": "list1",
    #        "title": "/r/soccerstreams_pl",
    #        "sub": "soccerstreams_pl",
    #        "sep": " vs"
    #        }
    #      ]
    #    }
    data = {
        "provider": "reddit",
        "action": "list1",
        "title": "Reddit Soccer",
        "sub": "redditsoccer",
        "sep": " vs"
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  xbmcplugin.endOfDirectory(_handle)



def build_arenavision_list0(title):
  xbmcplugin.setPluginCategory(_handle, title)

  listitem = xbmcgui.ListItem(label='Refresh List')
  listitem.setInfo('video', {'title': 'Refresh List', 'mediatype': 'video'})
  data = {
      "provider": "arenavision",
      "action": "list0",
      "title": "Arenavision"
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  today = '{:%d/%m/%Y}'.format(datetime.utcnow())
  tomorrow = '{:%d/%m/%Y}'.format(datetime.utcnow() + timedelta(days=1))
  page = requests.get('http://arenavision.in/guide', cookies={'Cookie': 'beget=begetok; expires=' + ('{:%a, %d %b %Y %H:%M:%S GMT}'.format(datetime.utcnow() + timedelta(seconds=19360000))) + '; path=/'}, headers=headers).content
  tree = html.fromstring(page)
  pattern = re.compile(r'([0-9-]+)\W*([A-Z]+)', re.IGNORECASE)

  for item in tree.xpath('//tr[count(./td)>=6]'):
    av_date = item.xpath('./td[1]')[0].text.encode('utf-8').strip()
    if today != av_date and tomorrow !=av_date:
      continue
    av_time = item.xpath('./td[2]')[0].text.encode('utf-8').strip()
    av_sport = item.xpath('./td[3]')[0].text.encode('utf-8').strip()
    av_tournament = item.xpath('./td[4]')[0].text.encode('utf-8').strip()
    av_match = item.xpath('./td[5]')[0].text.encode('utf-8').strip()
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

  xbmcplugin.endOfDirectory(_handle)

def build_arenavision_list1(title, urls):
  xbmcplugin.setPluginCategory(_handle, title)

  listitem = xbmcgui.ListItem(label='Refresh List')
  listitem.setInfo('video', {'title': 'Refresh List', 'mediatype': 'video'})
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
    page = requests.get(t[1], cookies={'Cookie': 'beget=begetok; expires=' + ('{:%a, %d %b %Y %H:%M:%S GMT}'.format(datetime.utcnow() + timedelta(seconds=19360000))) + '; path=/'}, headers=headers).content
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



def build_platinsport_list0(title):
  xbmcplugin.setPluginCategory(_handle, title)

  listitem = xbmcgui.ListItem(label='Refresh list')
  listitem.setInfo('video', {'title': 'Refresh list', 'mediatype': 'video'})
  data = {
      "provider": "platinsport",
      "action": "list0",
      "title": "PlatinSport"
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  page = requests.get('http://www.platinsport.com/', headers=headers).content
  tree = html.fromstring(page)

  for item in tree.xpath('//article[@class="item-list"]'):
    date = item.xpath('./h2[@class="post-box-title"]/a')[0].text.encode('utf-8').strip()
    for row in tree.xpath('.//tr'):
      title = date[0:10] + ' ' + row.xpath('.//td[2]/strong')[0].text.encode('utf-8').strip()
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
  xbmcplugin.endOfDirectory(_handle)

def build_platinsport_list1(title, url):
  xbmcplugin.setPluginCategory(_handle, title)

  listitem = xbmcgui.ListItem(label='Refresh List')
  listitem.setInfo('video', {'title': 'Refresh List', 'mediatype': 'video'})
  data = {
      "provider": "platinsport",
      "action": "list1",
      "title" : title,
      "url" : url
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  pattern = re.compile(r'acestream:\/\/([0-z]{40})', re.IGNORECASE)
  page = requests.get(url, headers=headers).content
  for m in re.finditer(pattern, page):
    listitem = xbmcgui.ListItem(label=title)
    listitem.setInfo('video', {'title': title, 'mediatype': 'video'})
    listitem.setProperty('IsPlayable', 'true')
    data = {
        "action": "play",
        "video" : 'http://{0}:{1}/ace/manifest.m3u8?id={2}'.format(addon.getSetting('ace_host'), addon.getSetting('ace_port'), m.group(1))
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=False)

  xbmcplugin.endOfDirectory(_handle)



def build_reddit_list0(title, subs):
  xbmcplugin.setPluginCategory(_handle, title)
  for data in subs:
    listitem = xbmcgui.ListItem(label=data['title'])
    listitem.setInfo('video', {'title': data['title'], 'mediatype': 'video'})
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?data={1}'.format(_pid, urllib.quote(json.dumps(data))), listitem=listitem, isFolder=True)

  xbmcplugin.endOfDirectory(_handle)

def build_reddit_list1(title, sub, sep):
  xbmcplugin.setPluginCategory(_handle, title)

  listitem = xbmcgui.ListItem(label='Refresh List')
  listitem.setInfo('video', {'title': 'Refresh List', 'mediatype': 'video'})
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
    page = requests.get('https://www.reddit.com/r/{0}.json{1}'.format(sub, plus), headers=headers).content
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

def build_reddit_list2(title, url):
  xbmcplugin.setPluginCategory(_handle, title)

  listitem = xbmcgui.ListItem(label='Refresh List')
  listitem.setInfo('video', {'title': 'Refresh List', 'mediatype': 'video'})
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
    page = requests.get(url[:-1] + ".json" + plus, headers=headers).content
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

    elif params['provider'] == 'arenavision':
      if params['action'] == 'list0':
        try:
          build_arenavision_list0(params['title'])
        except Exception as e:
          xbmc.log("type error: " + str(e), xbmc.LOGERROR)
      elif params['action'] == 'list1':
        build_arenavision_list1(params['title'], params['url'])

    elif params['provider'] == 'platinsport':
      if params['action'] == 'list0':
        build_platinsport_list0(params['title'])
      elif params['action'] == 'list1':
        build_platinsport_list1(params['title'], params['url'])

    elif params['provider'] == 'reddit':
      if params['action'] == 'list0':
        build_reddit_list0(params['title'], params['subs'])
      elif params['action'] == 'list1':
        build_reddit_list1(params['title'], params['sub'], params['sep'])
      elif params['action'] == 'list2':
        build_reddit_list2(params['title'], params['url'])
  else:
    list_categories()

if __name__ == '__main__':
  router(sys.argv[2][1:])

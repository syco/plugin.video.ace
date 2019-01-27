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

  if addon.getSetting('show_arenavision') == "true":
    listitem = xbmcgui.ListItem(label='Arenavision')
    listitem.setInfo('video', {'title': 'Arenavision', 'mediatype': 'video'})
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=listing&title=Arenavision&provider=arenavision'.format(_pid), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_boxing') == "true":
    listitem = xbmcgui.ListItem(label='Reddit Boxing')
    listitem.setInfo('video', {'title': 'Reddit Boxing', 'mediatype': 'video'})
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=listing&title=Reddit%20Boxing&provider=reddit&sub=boxingstreams&sep=%20vs'.format(_pid), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_mma') == "true":
    listitem = xbmcgui.ListItem(label='Reddit MMA')
    listitem.setInfo('video', {'title': 'Reddit MMA', 'mediatype': 'video'})
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=listing&title=Reddit%20MMA&provider=reddit&sub=MMAStreams&sep=%20vs'.format(_pid), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_motorsports') == "true":
    listitem = xbmcgui.ListItem(label='Reddit MotorSports')
    listitem.setInfo('video', {'title': 'Reddit MotorSports', 'mediatype': 'video'})
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=listing&title=Reddit%20MotorSports&provider=reddit&sub=motorsportsstreams&sep=%20utc'.format(_pid), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_nba') == "true":
    listitem = xbmcgui.ListItem(label='Reddit NBA')
    listitem.setInfo('video', {'title': 'Reddit NBA', 'mediatype': 'video'})
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=listing&title=Reddit%20NBA&provider=reddit&sub=nbastreams&sep=%20@'.format(_pid), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_nfl') == "true":
    listitem = xbmcgui.ListItem(label='Reddit NFL')
    listitem.setInfo('video', {'title': 'Reddit NFL', 'mediatype': 'video'})
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=listing&title=Reddit%20NFL&provider=reddit&sub=nflstreams&sep=%20@'.format(_pid), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_soccer') == "true":
    listitem = xbmcgui.ListItem(label='Reddit Soccer')
    listitem.setInfo('video', {'title': 'Reddit Soccer', 'mediatype': 'video'})
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=listing&title=Reddit%20Soccer&provider=reddit&sub=soccerstreams_other&sep=%20vs'.format(_pid), listitem=listitem, isFolder=True)

  xbmcplugin.endOfDirectory(_handle)


def list_matches_arenavision(title):
  xbmcplugin.setPluginCategory(_handle, title)
  today = '{:%d/%m/%Y}'.format(datetime.utcnow())
  tomorrow = '{:%d/%m/%Y}'.format(datetime.utcnow() + timedelta(days=1))
  page = requests.get('http://arenavision.in/guide', cookies={'Cookie': 'beget=begetok; expires=' + ('{:%a, %d %b %Y %H:%M:%S GMT}'.format(datetime.utcnow() + timedelta(seconds=19360000))) + '; path=/'}, headers=headers).content
  tree = html.fromstring(page)
  pattern = re.compile(r'([0-9-]+)\s*\[([A-Z]+)\]', re.IGNORECASE)

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
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=sublisting&provider=arenavision&url={1}&title={2}'.format(_pid, urllib.quote('|'.join(urls)), urllib.quote(title)), listitem=listitem, isFolder=True)
  xbmcplugin.endOfDirectory(_handle)


def list_matches_reddit(title, sub, sep):
  xbmcplugin.setPluginCategory(_handle, title)
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
        xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=sublisting&provider=reddit&url={1}&title={2}'.format(_pid, urllib.quote(url2), urllib.quote(title)), listitem=listitem, isFolder=True)
    after = js["data"]["after"]
    if after is None:
      break
    else:
      plus = "?after=" + after
  xbmcplugin.endOfDirectory(_handle)


def list_links_arenavision(title, url):
  xbmcplugin.setPluginCategory(_handle, title)
  pattern = re.compile(r'acestream:\/\/([0-z]{40})', re.IGNORECASE)
  for r in url.split('|'):
    t = r.split('!')
    page = requests.get(t[1], cookies={'Cookie': 'beget=begetok; expires=' + ('{:%a, %d %b %Y %H:%M:%S GMT}'.format(datetime.utcnow() + timedelta(seconds=19360000))) + '; path=/'}, headers=headers).content
    for m in re.finditer(pattern, page):
      listitem = xbmcgui.ListItem(label=t[0])
      listitem.setInfo('video', {'title': t[0], 'mediatype': 'video'})
      listitem.setProperty('IsPlayable', 'true')
      xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=play&video={1}'.format(_pid, 'http://{0}:{1}/ace/manifest.m3u8?id={2}'.format(addon.getSetting('ace_host'), addon.getSetting('ace_port'), m.group(1))), listitem=listitem, isFolder=False)
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

def list_links_reddit(title, url):
  xbmcplugin.setPluginCategory(_handle, title)
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
        xbmcplugin.addDirectoryItem(handle=_handle, url='http://{0}:{1}/ace/manifest.m3u8?id={2}'.format(addon.getSetting('ace_host'), addon.getSetting('ace_port'), m.group(2)), listitem=listitem, isFolder=False)
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
  params = dict(parse_qsl(paramstring))
  if params:
    if params['action'] == 'listing':
      if params['provider'] == 'arenavision':
        list_matches_arenavision(params['title'])
      elif params['provider'] == 'reddit':
        list_matches_reddit(params['title'], params['sub'], params['sep'])

    elif params['action'] == 'sublisting':
      if params['provider'] == 'arenavision':
        list_links_arenavision(params['title'], params['url'])
      elif params['provider'] == 'reddit':
        list_links_reddit(params['title'], params['url'])

    elif params['action'] == 'play':
      play_video(params['video'])
  else:
    list_categories()

if __name__ == '__main__':
  router(sys.argv[2][1:])

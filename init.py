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

  if addon.getSetting('show_arenavision'):
    listitem = xbmcgui.ListItem(label='Arenavision')
    listitem.setInfo('video', {'title': 'Arenavision', 'mediatype': 'video'})
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=listing&title=Arenavision&category=arenavision&sub=%20&sep=%20'.format(_pid), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_boxing'):
    listitem = xbmcgui.ListItem(label='Reddit Boxing')
    listitem.setInfo('video', {'title': 'Reddit Boxing', 'mediatype': 'video'})
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=listing&title=Reddit%20Boxing&category=reddit&sub=boxingstreams&sep=%20vs'.format(_pid), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_mma'):
    listitem = xbmcgui.ListItem(label='Reddit MMA')
    listitem.setInfo('video', {'title': 'Reddit MMA', 'mediatype': 'video'})
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=listing&title=Reddit%20MMA&category=reddit&sub=MMAStreams&sep=%20vs'.format(_pid), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_motorsports'):
    listitem = xbmcgui.ListItem(label='Reddit MotorSports')
    listitem.setInfo('video', {'title': 'Reddit MotorSports', 'mediatype': 'video'})
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=listing&title=Reddit%20MotorSports&category=reddit&sub=motorsportsstreams&sep=%20utc'.format(_pid), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_nba'):
    listitem = xbmcgui.ListItem(label='Reddit NBA')
    listitem.setInfo('video', {'title': 'Reddit NBA', 'mediatype': 'video'})
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=listing&title=Reddit%20NBA&category=reddit&sub=nbastreams&sep=%20@'.format(_pid), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_nfl'):
    listitem = xbmcgui.ListItem(label='Reddit NFL')
    listitem.setInfo('video', {'title': 'Reddit NFL', 'mediatype': 'video'})
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=listing&title=Reddit%20NFL&category=reddit&sub=nflstreams&sep=%20@'.format(_pid), listitem=listitem, isFolder=True)

  if addon.getSetting('show_reddit_soccer'):
    listitem = xbmcgui.ListItem(label='Reddit Soccer')
    listitem.setInfo('video', {'title': 'Reddit Soccer', 'mediatype': 'video'})
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=listing&title=Reddit%20Soccer&category=reddit&sub=soccerstreams_other&sep=%20vs'.format(_pid), listitem=listitem, isFolder=True)

  xbmcplugin.endOfDirectory(_handle)


def list_matches(title, category, sub, sep):
  xbmcplugin.setPluginCategory(_handle, title)
  if category == 'arenavision':
    today = '{:%d/%m/%Y}'.format(datetime.utcnow())
    tomorrow = '{:%d/%m/%Y}'.format(datetime.utcnow() + timedelta(days=1))
    page = requests.get('http://arenavision.in/guide', cookies={'Cookie': 'beget=begetok; expires=' + ('{:%a, %d %b %Y %H:%M:%S GMT}'.format(datetime.utcnow() + timedelta(seconds=19360000))) + '; path=/'}, headers=headers).content
    tree = html.fromstring(page)

    for item in tree.xpath('//tr[count(./td)>=6]'):
      av_date = item.xpath('./td[1]')[0].text.decode('UTF-8')
      if today != av_date and tomorrow !=av_date:
        continue
      av_time = item.xpath('./td[2]')[0].text.decode('UTF-8')
      av_sport = item.xpath('./td[3]')[0].text.decode('UTF-8')
      av_tournament = item.xpath('./td[4]')[0].text.decode('UTF-8')
      av_match = item.xpath('./td[5]')[0].text.decode('UTF-8')
      av_langs = '' 
      urls = []
      for t1 in item.xpath('./td[6]'):
        tokens = t1.text.split(' ')
        av_langs = av_langs + ' ' + tokens[1]
        for c in tokens[0].split('-'):
          c = c.strip()
          if c[0] == 'W':
            urls.append(tokens[1] + ' ' + c + '!' + (tree.xpath('//a[text()="World Cup ' + c[1:] + '"]')[0]).get('href'))
          else:
            urls.append(tokens[1] + ' ' + c + '!' + (tree.xpath('//a[text()="ArenaVision ' + c + '"]')[0]).get('href'))
      title = av_date + ' ' + av_time + ' | ' + av_sport + ' | ' + av_tournament + ' | ' + av_match + ' |' + av_langs
      listitem = xbmcgui.ListItem(label=title)
      listitem.setInfo('video', {'title': title, 'mediatype': 'video'})
      xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=sublisting&category=arenavision&sub={1}&title={2}'.format(_pid, urllib.quote('|'.join(urls)), urllib.quote(title)), listitem=listitem, isFolder=True)

  elif category == 'reddit':
    plus = ""
    while True:
      page = requests.get('https://www.reddit.com/r/{0}.json{1}'.format(sub, plus), headers=headers).content
      js = json.loads(page)
      for t3 in js["data"]["children"]:
        title = t3["data"]["title"]
        if title.lower().find(sep) != -1:
          title2 = "{0}, by {1}".format(title, t3["data"]["author"]).decode('UTF-8')
          url2 = t3["data"]["url"].decode('UTF-8')
          listitem = xbmcgui.ListItem(label=title)
          listitem.setInfo('video', {'title': title, 'mediatype': 'video'})
          xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=sublisting&category=reddit&sub={1}&title={2}'.format(_pid, urllib.quote(url2), urllib.quote(title)), listitem=listitem, isFolder=True)
      after = js["data"]["after"]
      if after is None:
        break
      else:
        plus = "?after=" + after

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

def list_links(title, category, url):
  xbmcplugin.setPluginCategory(_handle, title)
  if category == 'arenavision':
    pattern = re.compile(r'acestream:\/\/([0-z]{40})', re.IGNORECASE)
    for r in url.split('|'):
      t = r.split('!')
      page = requests.get(t[1], cookies={'Cookie': 'beget=begetok; expires=' + ('{:%a, %d %b %Y %H:%M:%S GMT}'.format(datetime.utcnow() + timedelta(seconds=19360000))) + '; path=/'}, headers=headers).content
      for m in re.finditer(pattern, page):
        listitem = xbmcgui.ListItem(label=t[0])
        listitem.setInfo('video', {'title': t[0], 'mediatype': 'video'})
        listitem.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?action=play&video={1}'.format(_pid, 'http://{0}:{1}/ace/manifest.m3u8?id={2}'.format(addon.getSetting('ace_host'), addon.getSetting('ace_port'), m.group(1))), listitem=listitem, isFolder=False)

  elif category == 'reddit':
    pattern = re.compile(r'((?:\[[^\[\]]+\]\s+)*)acestream:\/\/([0-z]{40})((?:\s+\[[^\[\]]+\])*)', re.IGNORECASE)
    plus = ""
    while True:
      page = requests.get(url[:-1] + ".json" + plus, headers=headers).content
      js = json.loads(page)
      arr = findAllData(js, "data")
      for t3 in arr:
        for m in re.finditer(pattern, t3["body"]):
          acedesc = "{0}{1} by {2}".format(m.group(1), m.group(3), t3["author"])
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
      list_matches(params['title'], params['category'], params['sub'], params['sep'])
    elif params['action'] == 'sublisting':
      list_links(params['title'], params['category'], params['sub'])
    elif params['action'] == 'play':
      play_video(params['video'])
  else:
    list_categories()

if __name__ == '__main__':
  router(sys.argv[2][1:])

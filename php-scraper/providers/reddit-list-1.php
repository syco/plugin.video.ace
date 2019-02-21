<?php
function doYourStuff() {
  $return = [];
  $others = [];
  $html = getHtml($url);
  if ($html[0]) {
    $matches = [];
    preg_match_all('/((?:\[[^\[\]]+\]\s+)*)acestream:\/\/([0-z]{40})((?:\s+\[[^\[\]]+\])*)/', $html[1], $matches);
    for ($i = 0; $i < count($matches[0]); $i ++) {
      $ace = $matches[2][$i];
      $extra = "";
      if (isset($return[$ace])) {
        continue;
      }
      if (!empty($matches[1][$i])) {
        $extra = trim($matches[1][$i]);
      } else if (!empty($matches[3][$i])) {
        $extra = trim($matches[3][$i]);
      }
      if(empty($extra)) {
        $extra = "no info";
      }
      if (preg_match('/\[(ar|arabic|croatian|es|esp|fr|french|ger|german|kazakh|pl|polish|por|portugal|portuguese|pt|ru|russian|spanish|turkish|ukrainian|vietnamese)\]/i', $extra)) {
        $others[] = ['title' => $extra, 'ace' => $ace];
      } else {
        $return[] = ['title' => $extra, 'ace' => $ace];
      }
    }
  }
  return array_merge($return, $others);
}

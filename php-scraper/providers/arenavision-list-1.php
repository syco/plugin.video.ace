<?php
function doYourStuff() {
  $return = [];
  $founds = [];
  foreach (explode("|", $url) AS $stream) {
    $tokens = explode("!", $stream);
    $html = getHtml($tokens[1], 'beget=begetok; expires=' . date('a, d b Y H:M:S GMT', time() + 19360000) . '; path=/');
    if ($html[0]) {
      $matches = [];
      preg_match('/acestream:\/\/([0-z]{40})/', $html[1], $matches);
      $ace = $matches[1];
      if (in_array($ace, $founds)) {
        continue;
      }
      $founds[] = $ace;
      $return[] = ['title' => $tokens[0], 'ace' => $ace];
    }
  }
  return $return;
}

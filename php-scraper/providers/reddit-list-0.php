<?php
function doYourStuff() {
  $return = [];
  $html = getHtml("https://www.reddit.com/r/soccerstreams/");
  if ($html[0]) {
    $doc = new DOMDocument();
    @$doc->loadHTML($html[1]);
    $xpath = new DOMXpath($doc);

    $links = $xpath->query("//a[.//*[contains(translate(text(), 'ABCDEFGHJIKLMNOPQRSTUVWXYZ', 'abcdefghjiklmnopqrstuvwxyz'), ' vs')]]");
    foreach ($links AS $link) {
      $return[] = ['title' => $link->textContent, 'action' => 'listRedditStreams', 'url' => "https://www.reddit.com{$link->getAttribute("href")}"];
    }
  }
  return $return;
}

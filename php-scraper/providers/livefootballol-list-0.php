<?php
function doYourStuff() {
  $return = [];

  $links = ['https://www.livefootballol.me/channels/'];
  for ($i = 2; $i <= 20; $i++) {
    $links[] = "https://www.livefootballol.me/channels/page-{$i}.html";
  }

  foreach ($links as $link) {
    $html = getHtml($link, null, false);
    if ($html[0]) {
      $doc = new DOMDocument();
      @$doc->loadHTML($html[1]);
      $xpath = new DOMXpath($doc);

      foreach ($xpath->query('//table[@class="uk-table uk-table-striped"]/*/tr/td/a') as $obj) {
        $obj->textContent;
      }
    }
  }




  $today = date('d/m/Y');
  $tomorrow = date('d/m/Y', time() + 86400);
  $html = getHtml('http://arenavision.in/guide', 'beget=begetok; expires=' . date('a, d b Y H:M:S GMT', time() + 19360000) . '; path=/');
  if ($html[0]) {
    $doc = new DOMDocument();
    @$doc->loadHTML($html[1]);
    $xpath = new DOMXpath($doc);

    $links = $xpath->query("//tr[count(./td)>=6]");
    foreach ($links AS $link) {
      $av_date = $xpath->query('./td[1]', $link)[0]->textContent;
      if ($today !== $av_date and $tomorrow !== $av_date) {
        continue;
      }
      $av_time = $xpath->query('./td[2]', $link)[0]->textContent;
      $av_sport = $xpath->query('./td[3]', $link)[0]->textContent;
      $av_tournament = $xpath->query('./td[4]', $link)[0]->textContent;
      $av_match = $xpath->query('./td[5]', $link)[0]->textContent;
      $av_langs = '';
      $urls = [];
      foreach (preg_split('/[\r\n]+/', $xpath->query('./td[6]', $link)[0]->textContent) AS $t1) {
        $tokens = preg_split('/[\s+]/', trim($t1));
        $av_langs .= ' ' . trim($tokens[1]);
        foreach (explode('-', $tokens[0]) AS $c) {
          $c = trim($c);
          if (substr($c, 0, 1) == 'W') {
            $urls[] = trim($tokens[1]) . '!' . $xpath->query('//a[text()="World Cup ' . substr($c, 1) . '"]')[0]->getAttribute('href');
          } else {
            $urls[] = trim($tokens[1]) . '!' . $xpath->query('//a[text()="ArenaVision ' . $c . '"]')[0]->getAttribute('href');
          }
        }
      }
      if (!empty($urls)) {
        $title = "$av_date $av_time | $av_sport | $av_tournament | $av_match |$av_langs";
        $return[] = ['title' => $title, 'action' => 'listArenavisionStreams', 'url' => implode('|', $urls)];
      }
    }
  }
  return $return;
}

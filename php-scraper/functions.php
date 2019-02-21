<?php

function getHtml($url, $cookie = null, $mobile = true) {
  $ch = curl_init();
  curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);
  curl_setopt($ch, CURLOPT_COOKIE, $cookie);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
  curl_setopt($ch, CURLOPT_TIMEOUT, 60);
  curl_setopt($ch, CURLOPT_URL, $url);
  if ($mobile) {
    curl_setopt($ch, CURLOPT_USERAGENT, "");
  } else {
    curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0");
  }

  if (curl_error($ch)) {
    $error_msg = curl_error($ch);
    return [FALSE, "ERROR: $error_msg\n\n"];
  }
  $html = curl_exec($ch);
  curl_close($ch);
  return [TRUE, $html];
}

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
    curl_setopt($ch, CURLOPT_USERAGENT, "");
  }

  if (curl_error($ch)) {
    $error_msg = curl_error($ch);
    return [FALSE, "ERROR: $error_msg\n\n"];
  }
  $html = curl_exec($ch);
  curl_close($ch);
  return [TRUE, $html];
}

<?php

error_reporting(E_ALL);

header('Content-Type: application/json');
require_once 'functions.php';

$action = filter_input(INPUT_GET, 'action');

if (file_exists("providers/{$action}.php")) {
  require_once "providers/{$action}.php";
  echo json_encode(doYourStuff());
} else {
  echo json_encode(
    [
      ['title' => 'Arenavision', 'action' => 'arenavision-list-0'],
      ['title' => 'Free Live Football Streaming', 'action' => 'livefootballol-list-0'],
      ['title' => 'LiveTV.sx', 'action' => 'livetvsx-list-0'],
      ['title' => 'Platin Sport', 'action' => 'platinsport-list-0'],
    ]
  );
}

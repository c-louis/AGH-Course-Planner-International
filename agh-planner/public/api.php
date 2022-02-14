<?php

if (isset($_GET['id'])) {
	$id = $_GET['id'];
	$rq = file_get_contents('https://sylabusy.agh.edu.pl/en/document/'.$id.'.jsonHtml');
	echo $rq;
} else {
	echo 'Invalid Request';
}


?>
<?php
	$login = '';
	$pass = '';
	if (!empty($_POST['login']) && !empty($_POST['pass'])) 
	{
		$login = trim($_POST['login']);
		$pass = trim($_POST['pass']);

		if(($login=="patrick")&&($pass=="password"))
		{
			$authenticated=1;	
			//echo 'YES';
			header("Location: ./hourra/welcome.html");
		}		
		else 
		{
			$authenticated=0;
			echo '<center><h1>Authentication Failed</h1></center>';
		}
	}
?>
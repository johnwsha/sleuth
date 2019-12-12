<?php

				$hour=$_GET['hour'];
				$minute=$_GET['minute'];
				$meridian=$_GET['meridian'];

?>

<html>
   <head>
      <title>HTML Meta Tag</title>
      <meta http-equiv = "refresh" content = "2; url = pickaparty.html">
   </head>
   <body>
      <p></p>
   </body>

Hour : <B><?php echo $hour; ?></B>
Minute : <B><?php=$hour?></B>
Meridian : <B><?php=$meridian?></B>

</html>

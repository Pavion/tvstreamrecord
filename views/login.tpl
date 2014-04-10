<!DOCTYPE html>
<html>
    <head>
        <title>tvstreamrecord</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="css/login.css" />
    </head>
    <body>
        <div id="loginWindow">
            <div id="myLogo">
                <a href=""><img alt="" src="images/tvstreamrecordlogo.png" /></a>
            </div>
            <form action="/login" method="post">
                <div>
                    <center>
                    Password<br />
                    <input type="password" id="pw" name="pw"><br />
                    <input type="checkbox" value="1" name="store_pw">Remember me<br />
                    <input type="submit" value="Login">
                    </center>
                </div>
            </form>
        </div>
    </body>
</html>

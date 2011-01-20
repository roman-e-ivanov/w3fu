<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:include href="common/head.html.xsl" />
	<w3fu:include href="common/footer.html.xsl" />
	<w3fu:include href="common/nav.html.xsl" />

	<w3fu:template match="/">
		<html>
			<head>
			<title>Регистрация</title>
			<meta name="keywords">
				<w3fu:attribute name="content">
        			
        		</w3fu:attribute>
			</meta>

			<meta name="description">
				<w3fu:attribute name="content">
					
				</w3fu:attribute>
			</meta>
			<w3fu:call-template name="w3fu:header" />
			</head>
			
			<body>
				
				<div class="l-header">
					<p>Заголовок<br /><br /></p>

					
				</div>
				
				
				<div class="l-main">
				 	
					<div class="l-main-sidebar">
						<w3fu:apply-templates select="*/nav" />
						<w3fu:call-template name="w3fu:statnav" />
					</div>

					<div class="l-main-content">
						<form method="post" action="/register" class="validate">
							<p>Регистрации</p>
							<p>Логин:
							<input type="text" name="password" class="text_login val-required"
								maxlength="255" value="12345678" /></p>
							<p>Пароль:
							<input type="text" name="password" class="text_login val-required"
								maxlength="255" value="12345678" /></p>
							
							<p><input type="submit" class="button" value="ОК" /></p>
							
							
						</form>
					</div>

				</div>

				<div class="l-footer">
					<w3fu:call-template name="w3fu:footer" />
					
					
				</div>
			</body>
		</html>
		
	</w3fu:template>

</w3fu:stylesheet>
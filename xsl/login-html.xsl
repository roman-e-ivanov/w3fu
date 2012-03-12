<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:include href="common/head.html.xsl" />
	<w3fu:include href="common/top.html.xsl" />
	<w3fu:include href="common/footer.html.xsl" />
	<w3fu:include href="common/nav.html.xsl" />
	<w3fu:include href="common/forms.html.xsl" />
	
	<w3fu:template match="/">
		<html>
			<head>
			<title>Вход на сайт</title>
			<meta name="keywords" content="войти, вход, залогиниться" />
    		<meta name="description" content="Вход на сайт" />
			<w3fu:call-template name="w3fu:links" />
			</head>
			
			<body>
				<w3fu:call-template name="w3fu:statnav" />
			
				<div class="container_16">
				<w3fu:call-template name="w3fu:top" />
				
					<div class="grid_3 l-main"><br/></div>	
					<div class="grid_10">						
						
						<form method="post" action="/login" class="login">												
							<w3fu:call-template name="w3fu:edit-login" />
							<w3fu:call-template name="w3fu:val-login-msg" />
							<w3fu:call-template name="w3fu:login-label" />
							<w3fu:call-template name="w3fu:edit-password" />
							<w3fu:call-template name="w3fu:val-password-msg" />
							<w3fu:call-template name="w3fu:password-label" />
							<input type="submit" class="button-enter-login" value="Войти" />
							<a href="/register">Зарегистрироваться</a>
							<w3fu:call-template name="w3fu:error-auth" />
						</form>
					</div>
					<div class="grid_3 l-main"><br/></div>
					<div class="clear"></div>

					<w3fu:call-template name="w3fu:footer" />
				
				</div>
			</body>
		</html>
		
	</w3fu:template>

</w3fu:stylesheet>
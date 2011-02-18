<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:include href="common/head.html.xsl" />
	<w3fu:include href="common/footer.html.xsl" />
	<w3fu:include href="common/nav.html.xsl" />
	<w3fu:include href="common/errors.html.xsl" />
	<w3fu:include href="common/user.html.xsl" />
	
	<w3fu:template match="/">
		<html>
			<head>
			<title>Вход на сайт</title>
			<w3fu:call-template name="w3fu:keywords">
				<w3fu:with-param name="keywords" select="'войти, вход, залогиниться'" />
			</w3fu:call-template>
			
			<w3fu:call-template name="w3fu:description">
				<w3fu:with-param name="description" select="'Вход на сайт'" />
			</w3fu:call-template>

			<w3fu:call-template name="w3fu:links" />
			</head>
			
			<body>
				<w3fu:call-template name="w3fu:statnav" />
			
				<div class="container_16">
				<div class="grid_12 l-header">
					<p>Заголовок</p>
				</div>
				<div class="grid_4 l-header">
					<w3fu:call-template name="w3fu:user-login" />
				</div>
				
				<div class="clear"></div>
				 	
					<!--<div class="l-main-sidebar">
						<w3fu:apply-templates select="*/nav" />
					</div> -->

					<div class="grid_16 l-main">
						<form method="post" action="/login" class="validate">
							<p>Вход</p>
							<p>Логин:
															
								<input type="text" name="login" maxlength="32">
									<w3fu:attribute name="value">
										<w3fu:value-of select="login/form/values/login" />
									</w3fu:attribute>
									
									<w3fu:attribute name="class">									
										<w3fu:text>val-required val-login </w3fu:text>						
										<w3fu:call-template name="w3fu:login-status-class">
											<w3fu:with-param name="status" select="login/form/errors/login" />
										</w3fu:call-template>
									</w3fu:attribute>
								</input>
								<w3fu:call-template name="w3fu:login-status-msg">
									<w3fu:with-param name="status" select="login/form/errors/login" />
								</w3fu:call-template>
							</p> 
							<p>Пароль:
								<input type="text" name="password" maxlength="32">
									<w3fu:attribute name="value">
										<w3fu:value-of select="login/form/values/password" />
									</w3fu:attribute>
									<w3fu:attribute name="class">
										<w3fu:call-template name="w3fu:password-status-class">
											<w3fu:with-param name="status" select="login/form/errors/password" />
										</w3fu:call-template>
									</w3fu:attribute>
								</input>
								<w3fu:call-template name="w3fu:login-status-msg">
									<w3fu:with-param name="status" select="login/form/errors/password" />
								</w3fu:call-template>
							</p>
							<p><input type="submit" class="button" value="ОК" /></p>
							 <w3fu:apply-templates select="login/error" />
						</form>
					</div>
					<div class="clear"></div>

				<div class="grid_16 l-footer">
					<w3fu:call-template name="w3fu:footer" />
				</div>
				<div class="clear"></div>
				<w3fu:call-template name="w3fu:user-not-login" />
				</div>
			</body>
		</html>
		
	</w3fu:template>

</w3fu:stylesheet>
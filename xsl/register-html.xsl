<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:include href="common/head.html.xsl" />
	<w3fu:include href="common/top.html.xsl" />
	<w3fu:include href="blocks/b-development-menu/b-development-menu.html.xsl" />
	<w3fu:include href="blocks/b-form-register/b-form-register.html.xsl" />
	<w3fu:include href="blocks/b-page-footer/b-page-footer.html.xsl" />
	
	<w3fu:template match="/">
		<html>
			<head>
			<title>Вход на сайт</title>
			<meta name="keywords" content="войти, вход, зарегистрироваться" />
    		<meta name="description" content="Регистрация на сайте" />
			<w3fu:call-template name="w3fu:links" />
			<link rel="stylesheet" href="/s/pages/register/register.html.css" type="text/css" />
			<script type="text/javascript" src="/s/pages/register/register.html.js" />
			</head>
			
			<body>
				<w3fu:call-template name="w3fu:b-development-menu" />
			
				<div class="container_16">
					<w3fu:call-template name="w3fu:top" />
				
					<div class="grid_3 l-main"><br/></div>	
					<div class="grid_10">						
						
						<w3fu:call-template name="w3fu:b-form-register" />
					</div>
					<div class="grid_3 l-main"><br/></div>
					<div class="clear"></div>

					<w3fu:call-template name="w3fu:b-page-footer" />

				</div>
			</body>
		</html>
		
	</w3fu:template>

</w3fu:stylesheet>
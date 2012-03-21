<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:include href="common/head.html.xsl" />
	<w3fu:include href="blocks/b-development-menu/b-development-menu.html.xsl" />
	<w3fu:include href="common/top.html.xsl" />
	<w3fu:include href="blocks/b-page-footer/b-page-footer.html.xsl" />
	
	<w3fu:template match="/">
		<html>
			<head>
			<title>Вход на сайт</title>
			<meta name="keywords" content="войти, вход, залогиниться" />
    		<meta name="description" content="Вход на сайт" />
			<w3fu:call-template name="w3fu:links" />
			</head>
			
			<body>
				<w3fu:call-template name="w3fu:b-development-menu" />
			
				<div class="container_16">
					<w3fu:call-template name="w3fu:top" />
				
					

				
					<w3fu:call-template name="w3fu:b-page-footer" />
				</div>
			</body>
		</html>
		
	</w3fu:template>

</w3fu:stylesheet>
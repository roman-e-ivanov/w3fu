<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:include href="../../blocks/b-page-head/b-page-head.html.xsl" />
	<w3fu:include href="../../blocks/b-development-menu/b-development-menu.html.xsl" />
	<w3fu:include href="../../blocks/b-page-footer/b-page-footer.html.xsl" />
	<w3fu:include href="../../blocks/b-page-top/b-page-top.html.xsl" />
	
	<w3fu:template match="/">
		<html>
			<head>
				<title>Поиск компании</title>
				<meta name="keywords" content="" />
    			<meta name="description" content="" />
				<w3fu:call-template name="w3fu:links" />
				<link rel="stylesheet" href="/s/pages/firms-public/firms-public.html.css" type="text/css" />
				<script type="text/javascript" src="/s/pages/firms-public/firms-public.html.js" />
			</head>
			
			<body>
				<w3fu:call-template name="w3fu:b-development-menu" />
				<div class="container_16">
					<w3fu:call-template name="w3fu:b-page-top" />
				
					<div class="grid_10 l-main">
						123
					</div>
						
					<div class="grid_6 l-main">
						123
					</div>
					
					<div class="clear"></div>
					<w3fu:call-template name="w3fu:b-page-footer" />				
				</div>
			</body>
		</html>	
	</w3fu:template>
</w3fu:stylesheet>
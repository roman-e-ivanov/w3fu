<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:include href="../../blocks/b-page-head/b-page-head.html.xsl" />
	<w3fu:include href="../../blocks/b-development-menu/b-development-menu.html.xsl" />
	<w3fu:include href="../../blocks/b-page-footer/b-page-footer.html.xsl" />
	<w3fu:include href="../../blocks/b-page-top/b-page-top.html.xsl" />
	<w3fu:include href="../../blocks/b-form-firm/b-form-firm.html.xsl" />
		
	<w3fu:template match="/">
		<html>
			<head>
				<title>Информация о компании</title>
				<meta name="keywords" content="" />
    			<meta name="description" content="" />
				<w3fu:call-template name="w3fu:links" />
				<link rel="stylesheet" href="/s/pages/firms-admin/firms-admin.html.css" type="text/css" />
				<script type="text/javascript" src="/s/pages/firms-admin/firms-admin.html.js" />
			</head>
			
			<body>
				<w3fu:call-template name="w3fu:b-development-menu" />
				<div class="container_16">
					<w3fu:call-template name="w3fu:b-page-top" />
				
					<div class="grid_10">
						<w3fu:call-template name="w3fu:b-form-firm" >
							<w3fu:with-param name="mode" select="1" />
						</w3fu:call-template>
					</div>
						
					<div class="grid_6 l-main">
						
					</div>
					
					<div class="clear"></div>
					<w3fu:call-template name="w3fu:b-page-footer" />				
				</div>
			</body>
		</html>	
	</w3fu:template>
</w3fu:stylesheet>
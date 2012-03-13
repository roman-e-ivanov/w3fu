<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:include href="common/head.html.xsl" />
	<w3fu:include href="common/footer.html.xsl" />
	<w3fu:include href="common/nav.html.xsl" />
 	<w3fu:include href="common/top.html.xsl" />
 	<w3fu:include href="common/forms.html.xsl" />

	<w3fu:template match="/">
		<html>
			<head>
			<title>Страница разработчика</title>
			<w3fu:call-template name="w3fu:links" />
			</head>
			
			<body>
			<w3fu:call-template name="w3fu:statnav" />
				<div class="container_16">
					<w3fu:call-template name="w3fu:top" />
			
					<div class="grid_4 l-main">Блок 1<br /><br /><br /><br /><br /></div>
					<div class="grid_4 l-main">Блок 2<br /><br /><br /><br /><br /></div>
					<div class="grid_4 l-main">Блок 3<br /><br /><br /><br /><br /></div>
					<div class="grid_4 l-main">Блок 4<br /><br /><br /><br /><br /></div>
					<div class="clear"></div>
				 	
				 	<w3fu:call-template name="w3fu:footer" />									
				</div>
			</body>
		</html>
		
	</w3fu:template>

</w3fu:stylesheet>
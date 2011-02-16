<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:include href="common/head.html.xsl" />
	<w3fu:include href="common/footer.html.xsl" />
	<w3fu:include href="common/nav.html.xsl" />
 	<w3fu:include href="common/datepicker.html.xsl" />
 	<w3fu:include href="common/user.html.xsl" />

	<w3fu:template match="/">
		<html>
			<head>
			<title>Главная страница</title>
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
				
			<!-- <div class="grid_4 l-main-sidebar">
					<w3fu:apply-templates select="*/nav" />
					
				</div>
			-->
					<div class="grid_4 l-main">Блок 1<br /><br /><br /><br /><br /></div>
					<div class="grid_4 l-main">Блок 2<br /><br /><br /><br /><br /></div>
					<div class="grid_4 l-main">Блок 3<br /><br /><br /><br /><br /></div>
					<div class="grid_4 l-main">Блок 4<br /><br /><br /><br /><br /></div>
					<div class="clear"></div>
				 

				<div class="l-footer grid_16">
					<w3fu:call-template name="w3fu:footer" />									
				</div>
				<div class="clear"></div>

					<w3fu:call-template name="w3fu:user-not-login" />
				</div>
			</body>
		</html>
		
	</w3fu:template>

</w3fu:stylesheet>
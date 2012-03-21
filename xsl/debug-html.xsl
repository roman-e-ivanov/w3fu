<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:include href="common/head.html.xsl" />
	<w3fu:include href="blocks/b-page-footer/b-page-footer.html.xsl" />
	<w3fu:include href="blocks/b-development-menu/b-development-menu.html.xsl" />
 	<w3fu:include href="common/top.html.xsl" />
 	<w3fu:include href="common/datepicker.html.xsl" />

	<w3fu:template match="/">
		<html>
			<head>
			<title>Страница разработчика</title>
			<w3fu:call-template name="w3fu:links" />
			<script type="text/javascript" src="/s/pages/debug/debug.html.js" />
			<link rel="stylesheet" href="/s/pages/debug/debug.html.css" type="text/css" />
			</head>
			
			<body>
			<w3fu:call-template name="w3fu:b-development-menu" />
				<div class="container_16">
					<w3fu:call-template name="w3fu:top" />
			
					<div class="grid_4 l-main b-debug-noxslt">
						<div class="b-debug-noxslt__head">Отображение без шаблона</div>
						<div class="b-debug-noxslt__body">
							<ul class="b-debug-noxslt__list">
								<li class="b-debug-noxslt__item"><a class="b-debug-noxslt__enable">Включить</a></li>
								<li iclass="b-debug-noxslt__item"><a class="b-debug-noxslt__disable">Выключить</a></li>
							</ul>
						</div>
					</div>
					<div class="grid_4 l-main"></div>
					
					<div class="grid_4 l-main"></div>
					
					<div class="grid_4 l-main">
					<form method="post" action="/login" class="region">
					<input type="text" name="pattern" maxlength="32" class="def" id="f4"/>
						<input type="submit" class="button-enter-login" value="Войти" />
						
					</form>
					</div>
					<div class="clear"></div>
				 	
				 	<w3fu:call-template name="w3fu:b-page-footer" />										
				</div>
			</body>
		</html>
		
	</w3fu:template>

</w3fu:stylesheet>
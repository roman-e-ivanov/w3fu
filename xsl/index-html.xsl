<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:include href="common/head.html.xsl" />
	<w3fu:include href="common/footer.html.xsl" />
	<w3fu:include href="common/nav.html.xsl" />
 	<w3fu:include href="common/providers-js.html.xsl" />
 	<w3fu:include href="common/datepicker.html.xsl" />

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
			<w3fu:call-template name="w3fu:links" />
			</head>
			
			<body>
			<w3fu:call-template name="w3fu:statnav" />
			
				<div class="container_16">
				
				<div class="grid_16 l-header">
					<p>Заголовок<br /><br /></p>
					
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
				<div class="popup1">
						<form><p>
						<input type="text" name="" class="text_login datepicker-day"
								maxlength="2" size="2" />-
							<input type="text" name="" class="text_login datepicker-month"
								maxlength="2" size="2" />-
							<input type="text" name="" class="text_login datepicker-year"
								maxlength="4" size="4" />
								<input type="button" class="dropdown-button" value=" C " />
							</p>
							</form>		
						<div class="dropdown-content">
							<w3fu:call-template name="w3fu:datepicker" />
						</div>
					</div>
					<w3fu:call-template name="w3fu:providers-js" />
				</div>
			<!--	<script type="text/javascript" src="s/js/modulargrid.js"></script> -->
			</body>
		</html>
		
	</w3fu:template>

</w3fu:stylesheet>
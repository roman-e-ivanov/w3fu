<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:include href="common/head.html.xsl" />
	<w3fu:include href="common/footer.html.xsl" />
	<w3fu:include href="common/nav.html.xsl" />
<!-- 	<w3fu:include href="common/errors.html.xsl" /> -->
	<w3fu:include href="common/user.html.xsl" />
	<w3fu:include href="common/forms.html.xsl" />
	<w3fu:include href="common/datepicker.html.xsl" />
	
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
				<div class="grid_12 l-header">
					<p>Заголовок</p>
				</div>
				<div class="grid_4 l-header">
				 	<w3fu:call-template name="w3fu:user-login" />
				</div>
				
				<div class="clear"></div>
				
					<div class="grid_8">
					<a class="f2">Создать компанию</a>
					<div class="f2popup">
						<div class="fast-firm">
							<form method="post" action="/admin/firms" class="firm-create">							
								<w3fu:call-template name="w3fu:edit-firm" />
								<input type="submit" class="button-enter-create" value="Создать" />
							</form>
							
						</div>
					</div>
					
					<br /><br /><br /><br />
					<form method="post" action="/login" class="region">
					<input type="text" name="pattern" maxlength="32" class="def" id="f4"/>
						<input type="submit" class="button-enter-login" value="Войти" />
						
					</form>
					<div id="f4popup"></div>
					
					
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
					</div>
						
					<div class="grid_8">
					<a class="f3">Создать компанию</a>
					<div class="f3popup">
						<div class="fast-firm">
							<form method="post" action="/admin/firms" class="firm-create">							
								<w3fu:call-template name="w3fu:edit-firm" />
								<input type="submit" class="button-enter-create" value="Создать" />
							</form>
						</div>
					</div>
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
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
			<title>Тестовая страница</title>
			<w3fu:call-template name="w3fu:keywords">
				<w3fu:with-param name="keywords" select="'войти, вход, залогиниться'" />
			</w3fu:call-template>
			
			<w3fu:call-template name="w3fu:description">
				<w3fu:with-param name="description" select="'Вход на сайт'" />
			</w3fu:call-template>

			<w3fu:call-template name="w3fu:links" />
			</head>
			
			<body>
				
				<div class="l-header">
					<p>Заголовок<br /><br /></p>
					<w3fu:call-template name="w3fu:providers-js" />
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
							<p>
								<select disabled="disabled"><option>20</option></select>
								<select disabled="disabled"><option>декабря</option></select>
								<select disabled="disabled"><option>2010</option></select>
							</p>
							</form>		
						<div class="dropdown-content">
							<w3fu:call-template name="w3fu:datepicker" />
						</div>
					</div>
					<div class="popup2">
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
				
				
				<div class="l-main">
				 	
					<div class="l-main-sidebar">
						<w3fu:apply-templates select="*/nav" />
						<w3fu:call-template name="w3fu:statnav" />
					</div>

					<div class="l-main-content">
						<form method="post" action="/register" class="validate">
							<p>Форма 1</p>
							<p>E-mail:
							<input type="text" name="email" class="text_login val-email val-required"
								maxlength="255" /> (*)</p>
							<p>E-mail:
							<input type="text" name="email" class="text_login val-email"
								maxlength="255" /></p>
							<p>Целое число:
							<input type="text" name="email" class="text_login val-integer val-required"
								maxlength="255" /> (*)</p>
							<p>Целое число:
							<input type="text" name="email" class="text_login val-integer"
								maxlength="255" /></p>
							<p>Я на все согласен:
							<input type="checkbox" name="" class="val-required val-toggle" /> (*)</p>
							<p><input type="submit" class="button" value="ОК" />
							<input type="reset" class="button" value="Очистить" /></p>
							<p><input type="button" class="b-ajax" value="AJAX" /></p>
							
						</form><br />
						<form method="post" action="/register" class="validate">
							<p>Форма 2</p>
							<p>E-mail:
							<input type="text" name="email" class="text_login val-email val-required"
								maxlength="255" /> (*)</p>
							<p>E-mail:
							<input type="text" name="email" class="text_login val-email"
								maxlength="255" /></p>
							<p>Целое число:
							<input type="text" name="email" class="text_login val-integer val-required"
								maxlength="255" /> (*)</p>
							<p>Целое число:
							<input type="text" name="email" class="text_login val-integer"
								maxlength="255" /></p>
							<p>Я на все согласен:
							<input type="checkbox" name="" class="val-required val-toggle" /> (*)</p>
							<p><input type="submit" class="button" value="ОК" />
							<input type="reset" class="button" value="Очистить"/></p>
						</form>
					</div>

				</div>

				<div class="l-footer">
					<w3fu:call-template name="w3fu:footer" />
					
					
				</div>
			</body>
		</html>
		
	</w3fu:template>

</w3fu:stylesheet>
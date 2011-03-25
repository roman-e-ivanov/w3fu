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
				<w3fu:call-template name="w3fu:statnav" />
				<div class="container_16">
				<div class="grid_12 l-header">
					<p>Заголовок</p>
				</div>
				<div class="grid_4 l-header">
					<w3fu:call-template name="w3fu:user-login" />
				</div>
				<div class="clear"></div>
				<div class="grid_12 l-main">
			 		<table class="timetable">
						<tr>
							<th></th>
							<th colspan="7">Столики двухместные</th></tr>
						<tr class="week">
							<th></th>
							<th>Пн</th><th>Вт</th><th>Cp</th><th>Чт</th><th>Пт</th><th>Сб</th><th>Вс</th>
						</tr>
						<tr class="dates">
							<th></th>
							<th class='date'>0</th><th class='date'>1</th><th class='date'>2</th><th class='date'>3</th><th class='date'>4</th><th class='date'>5</th><th class='date'>6</th>
						</tr>
						
						<tr>
							<th>00:00</th>
							<td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
							
						</tr>
						<tr>	
							<th>00:20</th>
							<td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
							
						</tr>
						
					</table> 
				
				</div>
				<div class="grid_4 l-main">2</div>
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
					
				<div class="l-main">

					<div class="l-main-content">
							
					</div>

				</div>

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
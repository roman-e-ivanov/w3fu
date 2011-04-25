<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform"
	xmlns:time="http://w3fu/time">

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
			 	 <w3fu:apply-templates select="document('conf/example.xml')/planxml" />
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
					
				<div class="l-footer grid_16">
					<w3fu:call-template name="w3fu:footer" />									
				</div>
				<div class="clear"></div>

					<w3fu:call-template name="w3fu:user-not-login" />
				</div>
			</body>
		</html>
		
	</w3fu:template>
	
	<w3fu:template match="planxml">
		<w3fu:apply-templates select="day" /> 
	</w3fu:template>
	
	<w3fu:template name="w3fu:timetable-days-names">
		<w3fu:param name="day" />
			<w3fu:choose>
				<w3fu:when test="$day = 0">Пн.</w3fu:when>
				<w3fu:when test="$day = 1">Вт.</w3fu:when>
				<w3fu:when test="$day = 2">Ср.</w3fu:when>
				<w3fu:when test="$day = 3">Чт.</w3fu:when>
				<w3fu:when test="$day = 4">Пт.</w3fu:when>
				<w3fu:when test="$day = 5">Сб.</w3fu:when>
				<w3fu:when test="$day = 6">Вс.</w3fu:when>
			</w3fu:choose>
	</w3fu:template>
	
	<w3fu:template name="w3fu:timetable-cell-type">
		<w3fu:param name="type" />
			<w3fu:choose>
				<w3fu:when test="$type = 0">timetable-cell-off</w3fu:when>
				<w3fu:when test="$type = 1">timetable-cell-free</w3fu:when>
				<w3fu:when test="$type = 2">timetable-cell-busy</w3fu:when>		
			</w3fu:choose>
	</w3fu:template>
 
	<w3fu:template match="day">
		<table class="timetable">
			<w3fu:variable name = "a" select="start" /> 		
				<tr>
					<th colspan="2">id=<w3fu:value-of select="../id" /></th>
				</tr>
				<tr>
					<th colspan="2">
						<w3fu:call-template name="w3fu:timetable-days-names">
							<w3fu:with-param name="day" select="time:gmtime(6,number($a))" />
						</w3fu:call-template>
					</th>
				</tr>
				<tr>
					<th colspan="2">
						<w3fu:value-of select="time:gmtime(2,number($a))" />.<w3fu:value-of select="time:gmtime(1,number($a))" />.<w3fu:value-of select="time:gmtime(0,number($a))" />
					</th>
				</tr>		
			<w3fu:apply-templates select="cell" /> 		
		</table>
	</w3fu:template>
 	
	<w3fu:template match="cell">
		<w3fu:variable name = "cell-start" select="start" />
		<tr>
			<th>
				<w3fu:value-of select="time:gmtime(3,number($cell-start))" />:<w3fu:value-of select="time:gmtime(4,number($cell-start))" />
			</th>
			<td>
				<w3fu:attribute name="class">									
					<w3fu:call-template name="w3fu:timetable-cell-type">
						<w3fu:with-param name="type" select="type" />
					</w3fu:call-template>
				</w3fu:attribute>
				<a href=""><w3fu:value-of select="type" /></a>
			</td>																	
		</tr>
	</w3fu:template>

</w3fu:stylesheet>
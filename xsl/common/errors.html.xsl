<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:template name="w3fu:login-status-class">
		<w3fu:param name="status" select="''"/>
			<w3fu:choose>
				<w3fu:when test="$status='argabsent'">login-argabsent</w3fu:when>
				<w3fu:otherwise>login-ok</w3fu:otherwise>
			</w3fu:choose>
	</w3fu:template>
	
	<w3fu:template name="w3fu:password-status-class">
		<w3fu:param name="status" select="''"/>
			<w3fu:choose>
				<w3fu:when test="$status='argabsent'">val-required val-password password-argabsent</w3fu:when>
				<w3fu:otherwise>val-required val-password password-ok</w3fu:otherwise>
			</w3fu:choose>
	</w3fu:template>
	
	
	<w3fu:template name="w3fu:login-status-msg">
		<w3fu:param name="status" select="''"/>
			<w3fu:choose>
				<w3fu:when test="$status='argabsent'">Поле не заполнено</w3fu:when>
				<w3fu:otherwise></w3fu:otherwise>
			</w3fu:choose>
	</w3fu:template>
	
	
	<w3fu:template match="error">
		<w3fu:apply-templates select="auth" />
	</w3fu:template>
	
	<w3fu:template match="auth">
		Неверный логин и/или пароль
	</w3fu:template>
	
		
</w3fu:stylesheet>
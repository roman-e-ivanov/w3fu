<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:template match="error">
		<w3fu:apply-templates select="auth" />
	</w3fu:template>
	
	<w3fu:template match="auth">
		Неверный логин и/или пароль
	</w3fu:template>
	
		
</w3fu:stylesheet>
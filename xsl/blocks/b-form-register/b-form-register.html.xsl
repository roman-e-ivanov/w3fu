<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:include href="../b-edit-email/b-edit-email.html.xsl" />
	<w3fu:include href="../b-form-error-msg/b-form-error-msg.html.xsl" />	
	
	<w3fu:template name="w3fu:b-form-register">
		<form method="post" action="/register" class="b-form-register">												
			<w3fu:call-template name="w3fu:b-form-error-msg" />
			<w3fu:call-template name="w3fu:b-edit-email" >
				<w3fu:with-param name="name" select="'email'" />
			</w3fu:call-template>
			<input type="submit" class="i-button" value="OK" />
			<a class="i-link" href="/login">Войти</a>
		</form>
	</w3fu:template>
</w3fu:stylesheet>
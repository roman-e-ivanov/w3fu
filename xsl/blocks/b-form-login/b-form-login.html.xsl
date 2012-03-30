<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:include href="../b-edit-email/b-edit-email.html.xsl" />
	<w3fu:include href="../b-edit-password/b-edit-password.html.xsl" />
	<w3fu:include href="../b-form-error-msg/b-form-error-msg.html.xsl" />	
	
	<w3fu:template name="w3fu:b-form-login">
		<form method="post" action="/login" class="b-form-login">												
			<w3fu:call-template name="w3fu:b-form-error-msg" />
			<w3fu:call-template name="w3fu:b-edit-email">
				<w3fu:with-param name="name" select="'email'" />
			</w3fu:call-template>
			<w3fu:call-template name="w3fu:b-edit-password" >
				<w3fu:with-param name="name" select="'password'" />
			</w3fu:call-template>
			<input type="submit" class="i-button" value="Войти" />
			<a class="i-link" href="/register">Зарегистрироваться</a>
		</form>
	</w3fu:template>
</w3fu:stylesheet>
<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:include href="../b-edit-login/b-edit-login.html.xsl" />
	
	<w3fu:template name="w3fu:b-form-login">
		<form method="post" action="/login" class="b-form-login__form">												
			<w3fu:call-template name="w3fu:b-edit-login" />
		</form>
	</w3fu:template>
</w3fu:stylesheet>
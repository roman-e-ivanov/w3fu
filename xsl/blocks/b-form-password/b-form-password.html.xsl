<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:include href="../b-edit-password/b-edit-password.html.xsl" />
	
	<w3fu:template name="w3fu:b-form-password">
		<form method="post" action="" class="b-form-password">												
			<w3fu:call-template name="w3fu:b-edit-password" >
				<w3fu:with-param name="name" select="'password'" />
			</w3fu:call-template>
			<input type="submit" class="i-button" value="OK" />
		</form>
	</w3fu:template>
</w3fu:stylesheet>
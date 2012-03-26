<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:include href="../b-edit-firm-name/b-edit-firm-name.html.xsl" />
	<w3fu:include href="../b-form-error-msg/b-form-error-msg.html.xsl" />	
	
	<w3fu:template name="w3fu:b-form-firm">
		<form method="post" action="" class="b-form-firm">												
			<w3fu:call-template name="w3fu:b-form-error-msg" />
			<w3fu:call-template name="w3fu:b-edit-firm-name" />
			<input type="submit" class="i-button" value="OK" />
		</form>
	</w3fu:template>
</w3fu:stylesheet>
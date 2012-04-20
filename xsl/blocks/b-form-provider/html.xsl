<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:include href="../b-edit-provider-name/html.xsl" />
	<w3fu:include href="../b-form-error-msg/html.xsl" />	
	
	<w3fu:template name="w3fu:b-form-provider">
		<w3fu:param name="mode" />
		<form method="post" action="" class="b-form-provider">												
			<w3fu:call-template name="w3fu:b-form-error-msg" />
			<w3fu:call-template name="w3fu:b-edit-provider-name">
				<w3fu:with-param name="name" select="'name'" />
				<w3fu:with-param name="value" select="/*/provider/doc/@name" />
			</w3fu:call-template>
			
			<w3fu:if test="$mode=1">
				<input type="hidden" name="method" value="put" /> 
			</w3fu:if>
			
			<input type="submit" class="i-button">
				<w3fu:attribute name="value">
					<w3fu:if test="$mode=0">Создать</w3fu:if>
					<w3fu:if test="$mode=1">Сохранить</w3fu:if>
				</w3fu:attribute>
			</input>
		</form>
		<w3fu:if test="$mode=1">
			<form method="post" action="">				
				<input type="hidden" name="method" value="delete" /> 
				<input type="submit" class="i-button" value="Удалить" />
			</form>
		</w3fu:if>
	</w3fu:template>
</w3fu:stylesheet>
<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:b-edit-provider-name">
		<w3fu:param name="name" />
		<w3fu:param name="value" />
		<div class="b-edit-provider-name__name">Название компании</div>
		
		<input type="text" maxlength="100">
			
			<w3fu:attribute name="name">
				<w3fu:value-of select="$name" />
			</w3fu:attribute>
			
			<w3fu:attribute name="value">
			 	<w3fu:value-of select="/*/form/source/@*[local-name(.)=$name]"/>
			 	<w3fu:value-of select="$value" />
			</w3fu:attribute>
									
			<w3fu:attribute name="class">									
				<w3fu:text>i-edit b-edit-provider-name</w3fu:text>									
			</w3fu:attribute>
		</input>
		<div class="b-edit-provider-name__label">1-100 символов</div>
	</w3fu:template>
</w3fu:stylesheet>
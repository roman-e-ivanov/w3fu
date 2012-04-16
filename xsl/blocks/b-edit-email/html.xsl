<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:b-edit-email">
		<w3fu:param name="name" />
		<div class="b-edit-email__name">Почта</div>
		
		<input type="text" maxlength="254">
			
			<w3fu:attribute name="name">
				<w3fu:value-of select="$name" />
			</w3fu:attribute>
			
			<w3fu:attribute name="value">
			 	<w3fu:value-of select="/*/form/source/@*[local-name(.)=$name]"/>
			</w3fu:attribute>
									
			<w3fu:attribute name="class">									
				<w3fu:text>i-edit b-edit-email</w3fu:text>									
			</w3fu:attribute>
		
		</input>
		<div class="b-edit-email__label">Пример: name@example.com</div>
	</w3fu:template>
</w3fu:stylesheet>
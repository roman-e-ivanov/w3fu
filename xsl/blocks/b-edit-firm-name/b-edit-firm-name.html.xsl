<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:b-edit-firm-name">
		<div class="b-edit-firm-name__name">Название компании</div>
		
		<input type="text" name="name" maxlength="100">
			
			<w3fu:attribute name="value">
				<w3fu:value-of select="*/form/source/@name" />
			</w3fu:attribute>
									
			<w3fu:attribute name="class">									
				<w3fu:if test="not(*/form/errors/name)">
					<w3fu:text>i-edit b-edit-firm-name</w3fu:text>
				</w3fu:if>
										
				<w3fu:if test="*/form/errors/name">
					<w3fu:text>i-edit b-edit-firm-name</w3fu:text>
				</w3fu:if>										
			</w3fu:attribute>
		</input>
		<div class="b-edit-firm-name__label">1-100 символов</div>
	</w3fu:template>
</w3fu:stylesheet>
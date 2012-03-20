<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:b-edit-email">
		<div class="b-edit-email__name">Почта</div>
		
		<input type="text" name="email" maxlength="64">
			
			<w3fu:attribute name="value">
				<w3fu:value-of select="*/form/source/@email" />
			</w3fu:attribute>
									
			<w3fu:attribute name="class">									
				<w3fu:if test="not(*/form/errors/login)">
					<w3fu:text>i-edit b-edit-email</w3fu:text>
				</w3fu:if>
										
				<w3fu:if test="*/form/errors/login">
					<w3fu:text>i-edit b-edit-email</w3fu:text>
				</w3fu:if>										
			</w3fu:attribute>
		</input>
		<div class="b-edit-email__label">Пример: name@example.com</div>
	</w3fu:template>
</w3fu:stylesheet>
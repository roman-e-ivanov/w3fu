<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:b-edit-login">
		<div class="b-edit-login__name">Логин</div>
		
		<input type="text" name="login" maxlength="32">
			
			<w3fu:attribute name="value">
				<w3fu:value-of select="*/form/source/@login" />
			</w3fu:attribute>
									
			<w3fu:attribute name="class">									
				<w3fu:if test="not(*/form/errors/login)">
					<w3fu:text>i-edit b-edit-login</w3fu:text>
				</w3fu:if>
										
				<w3fu:if test="*/form/errors/login">
					<w3fu:text>i-edit b-edit-login</w3fu:text>
				</w3fu:if>										
			</w3fu:attribute>
		</input>
		<div class="b-edit-login__label">4-32 символа: буквы, цифры, ( - ) , ( _ ) , ( . )</div>
	</w3fu:template>
</w3fu:stylesheet>
<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:b-edit-password">
		<div class="top-label">
			<div class="b-edit-password__name">Пароль</div>
			<div class="b-edit-password__toggle-display">показать</div>
			<div class="b-edit-password__toggle-hide">скрыть</div>
		</div>
		
		<input type="text" value="" class="i-edit b-edit-password__display-monitor" maxlength="32" />
		
		<input type="password" name="password" maxlength="32" >
		
		<w3fu:attribute name="class">
				<w3fu:if test="not(*/form/errors/password)">
					<w3fu:text>i-edit b-edit-password__display-element</w3fu:text>	
				</w3fu:if>
				
				<w3fu:if test="*/form/errors/password">
					<w3fu:text>i-edit b-edit-password__display-element</w3fu:text>	
				</w3fu:if>			
			</w3fu:attribute>
		</input>
		<div class="b-edit-password__label">4-32 символа: буквы, цифры, ( - ) , ( _ ) , ( . )</div>
	</w3fu:template>
</w3fu:stylesheet>
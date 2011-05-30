<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:edit-login">
		 <div class="top-label">
			<div class="title">Логин</div>
			<div>
				<w3fu:attribute name="class">									
				<w3fu:if test="not(login/form/errors/login/argsizeerror)">
					<w3fu:text>tip val-login-tip</w3fu:text>
				</w3fu:if>
										
				<w3fu:if test="login/form/errors/login/argsizeerror">
					<w3fu:text>tip-error val-login-tip</w3fu:text>
				</w3fu:if>										
				</w3fu:attribute> 
				<!-- 4-32 символа: буквы, цифры, ( - ) , ( _ ) , ( . )-->
			</div>
		</div>
		<input type="text" name="login" maxlength="32">
			
			<w3fu:attribute name="value">
				<w3fu:value-of select="login/form/source/@login" />
			</w3fu:attribute>
									
			<w3fu:attribute name="class">									
				<w3fu:if test="not(login/form/errors/login)">
					<w3fu:text>val-required val-login def </w3fu:text>
				</w3fu:if>
										
				<w3fu:if test="login/form/errors/login">
					<w3fu:text>val-required val-login err </w3fu:text>
				</w3fu:if>										
			</w3fu:attribute>
		</input>
		<div class="bottom-label">4-32 символа: буквы, цифры, ( - ) , ( _ ) , ( . )</div>
		
	</w3fu:template> 
	
	<w3fu:template name="w3fu:edit-password">	
		<div class="top-label">
			<div class="title">Пароль <span class="display-toggle nodisplay">(показать)</span></div>
			<div>
		 		<w3fu:attribute name="class">
				<w3fu:if test="not(login/form/errors/password/argsizeerror)">
					<w3fu:text>tip val-password-tip</w3fu:text>	
				</w3fu:if>
				
				<w3fu:if test="login/form/errors/password/argsizeerror">
					<w3fu:text>tip-error val-password-tip</w3fu:text>	
				</w3fu:if>			
				</w3fu:attribute>
				<!-- 4-32 символа: любые, кроме пробела -->
			</div>
		</div>
		<input type="text" value="" class="val-required val-password def display-monitor" style="display: none;" />
		<input type="password" name="password" maxlength="32">
			
			<w3fu:attribute name="class">
				<w3fu:if test="not(login/form/errors/password/argabsent)">
					<w3fu:text>val-required val-password def display-element </w3fu:text>	
				</w3fu:if>
				
				<w3fu:if test="login/form/errors/password/argabsent">
					<w3fu:text>val-required val-password err display-element </w3fu:text>	
				</w3fu:if>			
			</w3fu:attribute>
		</input>
		<div class="bottom-label">
			4-32 символа: любые, кроме пробела
		</div>
	</w3fu:template>

</w3fu:stylesheet>
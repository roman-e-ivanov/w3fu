<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:user-not-login">	
	<w3fu:if test="not(*/user)">		
		<div class="fast-login">
		<a href="/login" class="display">Войти</a><span class="dropdown-button nodisplay">Войти</span>		
		<div class="dropdown-content">
			<div class="fast-login-container">
				<form method="post" action="/login" class="fast-login">
					<w3fu:call-template name="w3fu:edit-login" />
					<w3fu:call-template name="w3fu:login-label" /> 
					<w3fu:call-template name="w3fu:edit-password" />
					<w3fu:call-template name="w3fu:password-label" /> 
					<input type="submit" class="button-enter-login" value="Войти" />
					<a href="/register">Зарегистрироваться</a>
				</form>
			</div>
		</div>
		</div>		
	</w3fu:if>
	</w3fu:template> 
		
	<w3fu:template name="w3fu:user-login">	
		<w3fu:if test="*/user">
			<w3fu:value-of select="*/user/@login" />
				<form method="post" action="/login" class="exit-form">				
					<input type="hidden" name="method" value="delete" /> 
					<input type="submit" class="exit-button" value="Выход" />
				</form>
		</w3fu:if>
	</w3fu:template>
	
	<w3fu:template match="providers/provider">
		<div >
			<w3fu:value-of select="." />
		</div>
	</w3fu:template>

</w3fu:stylesheet>
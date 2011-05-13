<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:user-not-login">
	
	<w3fu:if test="not(*/session)">	
	
		<div class="fast-login">
		<a href="/login" class="display">Войти</a><span class="dropdown-button nodisplay">Войти</span>		
		<div class="dropdown-content">
			<form method="post" action="/login" class="fast-login">
				<p class="fast-login">Логин</p><input type="text" name="login" maxlength="32" class="val-required val-login fast-login-def" /> 
				<p class="fast-login">Пароль <span class="display-toggle">676767</span></p><input type="password" name="password" maxlength="32" class="val-required val-password fast-login-def display-element" />
				<p class="display"><span>&#160;</span><span class="display-monitor nodisplay"></span></p>
				<p><input type="submit" class="button" value="ОК" /></p>
			</form>
			<a href="/register">Зарегестрироваться</a>
	<!-- 		<w3fu:apply-templates select="document('../conf/providers.xml')/*" /> -->
			</div>
		</div>
		
	</w3fu:if>
	</w3fu:template> 
	
	<w3fu:template name="w3fu:user-login">	
	
	<w3fu:if test="*/session">
		
			<w3fu:value-of select="*/session/@user-name" />
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
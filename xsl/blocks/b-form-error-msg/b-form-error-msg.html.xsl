<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:b-form-error-msg">
		<w3fu:if test="count(*/form/errors/*) > 0">
			<div class="b-form-error-msg">Следующие поля содержат ошибки:
				<ul class="b-form-error-msg__list">
					<w3fu:if test="*/form/errors/email">
						<li>Почта</li>
					</w3fu:if>
				
					<w3fu:if test="*/form/errors/password">
						<li>Пароль</li>
					</w3fu:if>
				</ul>
			</div>	
		</w3fu:if>
		
		<w3fu:if test="*/user-auth-error">
			<div class="b-form-error-msg">
				Ошибка аутентификации.<br /> Неправильный логин и/или пароль.
			</div>
		</w3fu:if>
		
		<w3fu:if test="*/user-exists-erro">
			<div class="b-form-error-msg">
				Ошибка регистрации. <br /> Пользователь с таким логином уже существует.
			</div>
		</w3fu:if>
		<user-auth-error/>	
	</w3fu:template>
</w3fu:stylesheet>
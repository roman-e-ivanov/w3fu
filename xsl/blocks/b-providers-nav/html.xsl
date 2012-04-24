<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:b-providers-nav">
		<div class="b-providers-nav">
			<ul class="b-providers-nav__list">
				<li class="b-providers-nav__line">
					<a class="link" href="/home/providers/list">Компании</a>
				</li>	
			
		<!-- 	<w3fu:if test="*/providers/i"> -->
				<li class="b-providers-nav__line">
					<a class="i-link" href="/home/providers">Создать компанию</a>
				</li>
		<!--	</w3fu:if> -->
			
			<w3fu:if test="*/provider">
			 		<li class="b-providers-nav__line">
						<a class="i-link">
							<w3fu:attribute name="href">
								<w3fu:value-of select="*/provider/nav/@workers" />
							</w3fu:attribute>
							<w3fu:text>Воркеры</w3fu:text>
						</a>
					</li>
						
					<li class="b-providers-nav__line">
						<a class="i-link">
							<w3fu:attribute name="href">
								<w3fu:value-of select="*/provider/nav/@services" />
							</w3fu:attribute>
							<w3fu:text>Сервисы</w3fu:text>
						</a>	
					</li> 
				</w3fu:if>
			</ul>
		</div>
	</w3fu:template>
</w3fu:stylesheet>
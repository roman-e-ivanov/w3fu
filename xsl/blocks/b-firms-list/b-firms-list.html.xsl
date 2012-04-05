<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:b-firms-list">
		<div class="b-firms-list">
			<ul class="b-firms-list__list">
				<w3fu:for-each	select="*/firms/i"> 
					<li class="b-firms-list__line">
						<a class="i-link b-firms-list__link">
							<w3fu:attribute name="href">
								<w3fu:value-of select="@path" />
							</w3fu:attribute>
							<w3fu:value-of select="firm/@name" />
						</a>
					</li>
				</w3fu:for-each>
			</ul>
		</div>
	</w3fu:template>
</w3fu:stylesheet>
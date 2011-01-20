<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:template match="nav">
		<div class="c-nav">
			<ul class="c-nav-list">
				<w3fu:apply-templates select="url" />
			</ul>
		</div>
	</w3fu:template>

	<w3fu:template match="url">

		<w3fu:param name="a" select="." />

		<!--
			<w3fu:variable name = "a"><w3fu:value-of select="."/></w3fu:variable>
		-->
		<li class="с-nav-line">
			<a title="">

				<w3fu:attribute name="href">
					<w3fu:value-of select="$a" />
				</w3fu:attribute>

				<w3fu:value-of select="$a" />

			</a>
		</li>

	</w3fu:template>
	
	<w3fu:template name="w3fu:statnav">

		<div class="c-nav">
			<ul class="c-nav-list">

				<li class="с-nav-line">
					<a title="" href="/">/</a>
				</li>

				<li class="с-nav-line">
					<a title="" href="/test">/test</a>
				</li>
				
			<li class="с-nav-line">
					<a title="" href="/login">/login</a>
				</li>
			<li class="с-nav-line">
					<a title="" href="/register">/register</a>
				</li>
			</ul>
		</div>


	</w3fu:template>

</w3fu:stylesheet>
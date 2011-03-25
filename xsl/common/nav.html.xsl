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
					<a title="" href="/plans/1?from=1298884200&amp;to=1398884200">/plans/1</a>
				</li>
			<!--<li class="с-nav-line">
					<a title="" href="/register">/register</a>
				</li>-->
			</ul>
		
		
			<ul class="c-nav-list">

				<li class="с-nav-line">
					<a title="" href="/?no-xslt">/?no-xslt</a>
				</li>

				<li class="с-nav-line">
					<a title="" href="/test?no-xslt">/test?no-xslt</a>
				</li>
				
			<li class="с-nav-line">
					<a title="" href="/login?no-xslt">/login?no-xslt</a>
				</li>
			
			<li class="с-nav-line">
					<a title="" href="/plans/1?from=1298884200&amp;to=1398884200&amp;no-xslt">/plans/1?no-xslt</a>
				</li>
					
			<!--<li class="с-nav-line">
					<a title="" href="/register?no-xslt">/register?no-xslt</a>
				</li>-->
			</ul>
		</div>

	</w3fu:template>

</w3fu:stylesheet>
<?xml version="1.0"?>
<!--
This XML file defines mapping rules for converting an Excel worksheet or TSV file to an XML document

Conceptually speaking, the Excel worksheet or TSV file is parsed first into an intermediate XML
document that contains field names as tags and field values as texts. This intermediate XML document
is then transformed into final XML document through XSLT transformation.

You could define multiple templates here, each catering for different schema.

Please note that because XML tag must start with a letter or underscore and contains only
letters, digits, hyphens, underscores and periods, any violating characters should be replaced
with underscores.
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
                xmlns:my="some.uri" exclude-result-prefixes="my">

<my:typemap>
  <entry key="bcf">vcf</entry>
</my:typemap>
  
<xsl:output method="xml" indent="yes"/>
<xsl:template match="/ResultSet/SampleSet"><!-->Should match <key_in_config>+'Set'<-->
  <SAMPLE_SET>
    <xsl:for-each select="Sample"><!-->Should select from <key_in_config><-->
      <SAMPLE>
        <SAMPLE_ID><xsl:value-of select="Sample_ID"/></SAMPLE_ID>
        <GENOTYPE_ID><xsl:value-of select="Geno_ID"/></GENOTYPE_ID>
      </SAMPLE>
    </xsl:for-each>
  </SAMPLE_SET>
</xsl:template>

<xsl:template match="/ResultSet/FileSet">
  <FILE_GROUP_SET>
    <xsl:for-each select="File">
      <xsl:variable name="filetype" select="Filetype"/>
      <FILE_GROUP>
        <FILE><xsl:value-of select="Filename"/></FILE>
        <FILE_TYPE><xsl:value-of select="document('')/*/my:typemap/entry[@key=$filetype]"/></FILE_TYPE>
      </FILE_GROUP>
    </xsl:for-each>
  </FILE_GROUP_SET>
</xsl:template>

</xsl:stylesheet>

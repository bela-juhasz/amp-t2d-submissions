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
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="xml" indent="yes"/>

<!--> Analysis <-->
<xsl:template match="AnalysisSet">
  <ANALYSIS_SET noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.analysis.xsd">
    <xsl:for-each select="Analysis">
      <ANALYSIS>
        <xsl:attribute name="alias">
          <xsl:value-of select="Analysis_alias"/>
        </xsl:attribute>
        <xsl:attribute name="center_name">
          <xsl:value-of select="Center_name"/>
        </xsl:attribute>
        <xsl:attribute name="broker_name">
          <xsl:value-of select="string('AMP T2D')"/>
        </xsl:attribute>
        <xsl:attribute name="analysis_center">
          <xsl:value-of select="Analysis_center"/>
        </xsl:attribute>
        <xsl:attribute name="analysis_date">
          <xsl:value-of select="Analysis_date"/>
        </xsl:attribute>
        <xsl:variable name="analysis_alias">
          <xsl:value-of select="Analysis_alias"/>
        </xsl:variable>
        <TITLE><xsl:value-of select="Title"/></TITLE>
        <DESCRIPTION><xsl:value-of select="Description"/></DESCRIPTION>
        <RUN_REF>
          <xsl:attribute name="refname">
            <xsl:value-of select="Run_Accession_s_"/>
          </xsl:attribute>
          <xsl:attribute name="refcenter">
            <xsl:value-of select="Center_name"/>
          </xsl:attribute>
        </RUN_REF>
        <ANALYSIS_TYPE>
          <SEQUENCE_VARIATION>
            <EXPERIMENT_TYPE><xsl:value-of select="Experiment_type"/></EXPERIMENT_TYPE>
            <PLATFORM><xsl:value-of select="Platform"/></PLATFORM>
            <IMPUTATION><xsl:value-of select="Imputation"/></IMPUTATION>
          </SEQUENCE_VARIATION>
        </ANALYSIS_TYPE>
        <FILES>
          <xsl:for-each select="/ResultSet/FileSet/File[Analysis_alias=$analysis_alias]">
            <File>
              <xsl:attribute name="filename">
                <xsl:value-of select="Filename"/>
              </xsl:attribute>
              <xsl:attribute name="filetype">
                <xsl:value-of select="Filetype"/>
              </xsl:attribute>
              <xsl:attribute name="checksum_method">
                <xsl:value-of select="string('MD5')"/>
              </xsl:attribute>
              <xsl:attribute name="checksum">
                <xsl:value-of select="Encrypted_checksum"/>
              </xsl:attribute>
              <xsl:attribute name="unencrypted_checksum">
                <xsl:value-of select="Unencrypted_checksum"/>
              </xsl:attribute>
            </File>
          </xsl:for-each>
        </FILES>
        <ANALYSIS_LINKS>
          <ANALYSIS_LINK>
            <XREF_LINK>
              <DB><xsl:value-of select="substring-before(External_link, ':')"/></DB>
              <ID><xsl:value-of select="substring-after(External_ink, ':')"/></ID>
            </XREF_LINK>
          </ANALYSIS_LINK>
        </ANALYSIS_LINKS>
        <ANALYSIS_ATTRIBUTES>
          <ANALYSIS_ATTRIBUTE>
            <TAG>pipeline_description</TAG>
            <VALUE><xsl:value-of select="Pipeline_Description"/></VALUE>
          </ANALYSIS_ATTRIBUTE>
          <ANALYSIS_ATTRIBUTE>
            <TAG>imputation</TAG>
            <VALUE><xsl:value-of select="Imputation"/></VALUE>
          </ANALYSIS_ATTRIBUTE>
          <ANALYSIS_ATTRIBUTE>
            <TAG>software</TAG>
            <VALUE><xsl:value-of select="Software"/></VALUE>
          </ANALYSIS_ATTRIBUTE>
        </ANALYSIS_ATTRIBUTES>
      </ANALYSIS>
    </xsl:for-each>
  </ANALYSIS_SET>
</xsl:template>

<xsl:template match="FileSet"/>

</xsl:stylesheet>

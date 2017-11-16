<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="xml" indent="yes"/>
<xsl:template match="/SampleSet">
  <SAMPLE_SET noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.sample.xsd">
    <xsl:for-each select="Sample">
      <SAMPLE>
        <xsl:attribute name="center_name">
            <xsl:value-of select="Center_name"/>
        </xsl:attribute>
        <DESCRIPTION><xsl:value-of select="Description"/></DESCRIPTION>
        <SAMPLE_NAME>
            <TAXON_ID>9606</TAXON_ID>
            <SCIENTIFIC_NAME>homo sapiens</SCIENTIFIC_NAME>
            <COMMON_NAME>human</COMMON_NAME>
        </SAMPLE_NAME>
        <SAMPLE_ATTRIBUTES>
            <SAMPLE_ATTRIBUTE>
                <TAG>subject_id</TAG>
                <VALUE><xsl:value-of select="Subject_ID"/></VALUE>
            </SAMPLE_ATTRIBUTE>
            <SAMPLE_ATTRIBUTE>
                <TAG>sample_id</TAG>
                <VALUE><xsl:value-of select="Sample_ID"/></VALUE>
            </SAMPLE_ATTRIBUTE>
            <SAMPLE_ATTRIBUTE>
                <TAG>cell_type</TAG>
                <VALUE><xsl:value-of select="Cell_Type"/></VALUE>
            </SAMPLE_ATTRIBUTE>
            <SAMPLE_ATTRIBUTE>
                <TAG>gender</TAG>
                <VALUE><xsl:value-of select="Gender"/></VALUE>
            </SAMPLE_ATTRIBUTE>
            <SAMPLE_ATTRIBUTE>
                <TAG>T2D</TAG>
                <VALUE><xsl:value-of select="T2D"/></VALUE>
            </SAMPLE_ATTRIBUTE>
            <SAMPLE_ATTRIBUTE>
                <TAG>year_of_birth</TAG>
                <VALUE><xsl:value-of select="Year_of_Birth"/></VALUE>
            </SAMPLE_ATTRIBUTE>
        </SAMPLE_ATTRIBUTES>
      </SAMPLE>
    </xsl:for-each>
  </SAMPLE_SET>
</xsl:template>

<xsl:template match="/AnalysisSet">
  <ANALYSIS_SET noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.analysis.xsd">
    <xsl:for-each select="Analysis">
      <ANALYSIS>
        <xsl:attribute name="analysis_center">
            <xsl:value-of select="Center_name"/>
        </xsl:attribute>
        <xsl:attribute name="analysis_date">
            <xsl:value-of select="Analysis_date"/>
        </xsl:attribute>
        <TITLE><xsl:value-of select="Title"/></TITLE>
        <DESCRIPTION><xsl:value-of select="Description"/></DESCRIPTION>
        <EXPERIMENT_REF><xsl:value-of select="Experiment_type"/></EXPERIMENT_REF>
        <RUN_REF><xsl:value-of select="Run_Accession_s_"/></RUN_REF>
        <ANALYSIS_LINKS><xsl:value-of select="External_link"/></ANALYSIS_LINKS>
      </ANALYSIS>
    </xsl:for-each>
  </ANALYSIS_SET>
</xsl:template>

</xsl:stylesheet>

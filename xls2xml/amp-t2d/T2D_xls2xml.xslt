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
<xsl:template match="/AnalysisSet">
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
          <FILE></FILE>
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

<!--> Experiment <-->
<!--xsl:template match="/AnalysisSet">
  <EXPERITMENT_SET noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.experiment.xsd">
    <EXPERIMENT>
      <xsl:attribute name="center_name">
        <xsl:value-of select="Center_name"/>
      </xsl:attribute>
      <TITLE><xsl:value-of select="Title"/></TITLE>
      <STUDY_REF>
        <xsl:attribute name="refname">
          <xsl:value-of select="Project_name"/>
        </xsl:attribute>
      </STUDY_REF>
    </EXPERIMENT>
  </EXPERITMENT_SET>
</xsl:template-->

<!--> Sample <-->
<xsl:template match="/SampleSet"><!-->Should match <key_in_config>+'Set'<-->
  <SAMPLE_SET noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.sample.xsd">
    <xsl:for-each select="Sample"><!-->Should select from <key_in_config><-->
      <SAMPLE>
        <xsl:attribute name="alias">
          <xsl:value-of select="Sample_ID"/>
        </xsl:attribute>
        <xsl:attribute name="center_name">
          <xsl:value-of select="Center_name"/>
        </xsl:attribute>
        <SAMPLE_NAME display_name="Human">
          <TAXON_ID>9606</TAXON_ID>
          <SCIENTIFIC_NAME>homo sapiens</SCIENTIFIC_NAME>
          <COMMON_NAME>human</COMMON_NAME>
        </SAMPLE_NAME>
        <DESCRIPTION><xsl:value-of select="Description"/></DESCRIPTION>
        <SAMPLE_ATTRIBUTES>
          <SAMPLE_ATTRIBUTE>
            <TAG>subject_id</TAG>
            <VALUE><xsl:value-of select="Subject_ID"/></VALUE>
          </SAMPLE_ATTRIBUTE>
          <SAMPLE_ATTRIBUTE>
            <TAG>phenotype</TAG>
            <VALUE><xsl:value-of select="Phenotype"/></VALUE>
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
            <TAG>T2D_status</TAG>
            <VALUE><xsl:value-of select="T2D"/></VALUE>
          </SAMPLE_ATTRIBUTE>
          <SAMPLE_ATTRIBUTE>
            <TAG>year_of_birth</TAG>
            <VALUE><xsl:value-of select="Year_of_Birth"/></VALUE>
          </SAMPLE_ATTRIBUTE>
          <SAMPLE_ATTRIBUTE>
            <TAG>ethnicity</TAG>
            <VALUE><xsl:value-of select="Ethnicity"/></VALUE>
          </SAMPLE_ATTRIBUTE>
          <SAMPLE_ATTRIBUTE>
            <TAG>ethnicity_description</TAG>
            <VALUE><xsl:value-of select="Ethnicity_Description"/></VALUE>
          </SAMPLE_ATTRIBUTE>
          <SAMPLE_ATTRIBUTE>
            <TAG>case_control</TAG>
            <VALUE><xsl:value-of select="Case_Control"/></VALUE>
          </SAMPLE_ATTRIBUTE>
          <SAMPLE_ATTRIBUTE>
            <TAG>of_spanish_origin</TAG>
            <VALUE><xsl:value-of select="Hispanic_or_Latino__of_Spanish_origin"/></VALUE>
          </SAMPLE_ATTRIBUTE>
          <SAMPLE_ATTRIBUTE>
            <TAG>age</TAG>
            <VALUE><xsl:value-of select="Age"/></VALUE>
          </SAMPLE_ATTRIBUTE>
          <SAMPLE_ATTRIBUTE>
            <TAG>year_of_first_visit</TAG>
            <VALUE><xsl:value-of select="Year_of_first_visit"/></VALUE>
          </SAMPLE_ATTRIBUTE>
          <SAMPLE_ATTRIBUTE>
            <TAG>cell_type</TAG>
            <VALUE><xsl:value-of select="Cell_Type"/></VALUE>
          </SAMPLE_ATTRIBUTE>
          <SAMPLE_ATTRIBUTE>
            <TAG>maternal_alias</TAG>
            <VALUE><xsl:value-of select="Maternal_id"/></VALUE>
          </SAMPLE_ATTRIBUTE>
          <SAMPLE_ATTRIBUTE>
            <TAG>paternal_alias</TAG>
            <VALUE><xsl:value-of select="Paternal_id"/></VALUE>
          </SAMPLE_ATTRIBUTE>
        </SAMPLE_ATTRIBUTES>
      </SAMPLE>
    </xsl:for-each>
  </SAMPLE_SET>
</xsl:template>

<!--> Study <-->
<xsl:template match="/ProjectSet">
  <STUDY_SET noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.study.xsd">
    <xsl:for-each select="Project">
      <STUDY>
        <xsl:attribute name="alias">
          <xsl:value-of select="Project_Accronym"/>
        </xsl:attribute>
        <DESCRIPTOR>
          <STUDY_TITLE><xsl:value-of select="Project_Name"/></STUDY_TITLE>
          <STUDY_TYPE>
            <xsl:attribute name="existing_study_type">
              <xsl:value-of select="string('Other')"/>
            </xsl:attribute>
          </STUDY_TYPE>
          <STUDY_DESCRIPTION><xsl:value-of select="Project_Description"/></STUDY_DESCRIPTION>
        </DESCRIPTOR>
        <STUDY_LINKS>
          <STUDY_LINK>
            <URL_LINK>
              <LABEL>Project website</LABEL>
              <URL><xsl:value-of select="Project_website_link"/></URL>
            </URL_LINK>
          </STUDY_LINK>
          <STUDY_LINK>
            <URL_LINK>
              <LABEL>Data URL</LABEL>
              <URL><xsl:value-of select="Data_URL"/></URL>
            </URL_LINK>
          </STUDY_LINK>
          <STUDY_LINK>
            <XREF_LINK>
              <DB><xsl:value-of select="substring-before(External_Links, ':')"/></DB>
              <ID><xsl:value-of select="substring-after(External_Links, ':')"/></ID>
            </XREF_LINK>
          </STUDY_LINK>
          <STUDY_LINK>
            <XREF_LINK>
              <DB><xsl:value-of select="substring-before(Project_Publications, ':')"/></DB>
              <ID><xsl:value-of select="substring-after(Project_Publications, ':')"/></ID>
            </XREF_LINK>
          </STUDY_LINK>
        </STUDY_LINKS>
      </STUDY>
    </xsl:for-each>
  </STUDY_SET>
</xsl:template>

</xsl:stylesheet>

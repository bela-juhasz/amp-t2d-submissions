from StringIO import StringIO

from foghorn import foghorn_compression

def test_processing_genotypes():
    ios_output_gt_cvcf = StringIO()
    ios_missing_vars_gt = StringIO()
    with open('data/test_input.vcf', "r") as vcf:
        foghorn_compression.compress_genotypes(vcf, ios_output_gt_cvcf, ios_missing_vars_gt)
    ios_output_gt_cvcf.seek(0)
    ios_missing_vars_gt.seek(0)
    assert ios_output_gt_cvcf.read() == open('data/test_output_genotypes.cvcf').read()
    assert ios_missing_vars_gt.read() == open('data/missing_vars_genotypes.txt').read()
    ios_output_gt_cvcf.close()
    ios_missing_vars_gt.close()

def test_processing_dosage():
    ios_output_ds_cvcf = StringIO()
    with open('data/test_input.vcf', 'r') as vcf:
        foghorn_compression.compress_dosages(vcf, ios_output_ds_cvcf)
    ios_output_ds_cvcf.seek(0)
    assert ios_output_ds_cvcf.read() == open('data/test_output_dosages.cvcf').read()
    ios_output_ds_cvcf.close()

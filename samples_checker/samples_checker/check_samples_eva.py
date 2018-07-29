from openpyxl import load_workbook
import os


def get_sample_names(eva_sample_sheet):
    sample_names = []
    num_rows = eva_sample_sheet.max_row
    num_cols = eva_sample_sheet.max_column

    for i in range(1, num_rows + 1):
        for j in range(1, num_cols + 1):
            if str(eva_sample_sheet.cell(i, j).value).strip().lower() == "sample name":
                first_sample_name_val = eva_sample_sheet.cell(i+1, j-3).value
                if first_sample_name_val is not None and not str(first_sample_name_val).strip() == "":
                    i += 1
                    j -= 3
                    while i <= num_rows:
                        sample_names.append(eva_sample_sheet.cell(i, j).value)
                        i += 1
                    return sample_names
                else:
                    first_sample_name_val = eva_sample_sheet.cell(i+1, j).value
                    if not str(first_sample_name_val).strip() == "":
                        i += 1
                        while i <= num_rows:
                            sample_names.append(eva_sample_sheet.cell(i, j).value)
                            i += 1
                        return sample_names
    raise Exception("Could not find sample names in the sheet: Sample")


eva_metadata_sheet = "/home/sundarvenkata/amp-t2d-submissions/samples_checker/tests/data/EVA_Submission.V1.0.5_LinMa_Nov_16_2017_garys.xlsx"
eva_metadata_sheet_copy = os.getcwd() + os.path.sep + \
                          ".".join(os.path.basename(eva_metadata_sheet).split(".")[:-1]) + "_with_sample_names_tab.xlsx"
metadata_wb = load_workbook(eva_metadata_sheet, data_only=True)
if "Sample" not in metadata_wb.sheetnames:
    raise Exception("Sample tab could not be found in the EVA metadata sheet: " + eva_metadata_sheet)
else:
    sample_names = get_sample_names(metadata_wb['Sample'])
    metadata_wb.save(eva_metadata_sheet_copy)
    metadata_wb.close()
    metadata_wb_copy = load_workbook(eva_metadata_sheet_copy)
    if "Sample_Names" not in metadata_wb_copy.sheetnames:
        sample_name_sheet = metadata_wb_copy.create_sheet("Sample_Names")
    else:
        sample_name_sheet = metadata_wb_copy["Sample_Names"]
    sample_name_sheet.cell(1, 1).value = "Sample Name"
    row_index = 2
    for sample_name in sample_names:
        sample_name_sheet.cell(row_index, 1).value = sample_name
        row_index += 1
    metadata_wb_copy.save(eva_metadata_sheet_copy)
    metadata_wb_copy.close()

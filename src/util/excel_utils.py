from util.io import grab_control_panel


def grab_column_vals(worksheet, columns):

    result = []
    if not isinstance(columns, list):
        columns = [columns]

    for colname in columns:
        vals = [cell.value for cell in worksheet[colname]]
        result.append(vals)

    return result


def extract_key_val(worksheet, cols):
    result = {}
    vals = grab_column_vals(worksheet, cols)
    for pair in zip(vals[0], vals[1]):
        if pair[0] is not None:
            val = "default" if pair[1] is None else pair[1].lower()
            result[pair[0].lower()] = val
    return result


def extract_control_panel_values():
    panel_dicts = {}
    wb = grab_control_panel()
    for worksheet_name in wb.sheetnames:
        sheet_dict = extract_key_val(wb[worksheet_name], ["C", "D"])
        panel_dicts[worksheet_name.lower()] = sheet_dict
    return panel_dicts

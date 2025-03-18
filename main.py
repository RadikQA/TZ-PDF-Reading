import fitz  # PyMuPDF
import json

# Data
pdf_path = "./pdf_data/test_task.pdf"

# Метод чтения
def read_and_format_pdf_info(pdf_path):

    doc = fitz.open(pdf_path)
    first_page = doc.load_page(0)

    text = first_page.get_text("text")

    lines = text.split('\n')

    keys_map = {
        "PN": "Part Number",
        "SN": "Serial Number",
        "DESCRIPTION": "Description",
        "LOCATION": "Location",
        "RECEIVER#": "Receiver Number",
        "EXP DATE": "Expiration Date",
        "CERT SOURCE": "Certification Source",
        "REC.DATE": "Received Date",
        "BATCH#": "Batch Number",
        "REMARK": "Remark",
        "CONDITION": "Condition",
        "UOM": "Unit of Measure",
        "PO": "Purchase Order",
        "MFG": "Manufacturer",
        "DOM": "Date of Manufacture",
        "LOT#": "Lot Number",
        "TAGGED BY": "Tagged By",
        "Qty": "Quantity"
    }

    data = {}
    for line in lines:
        for key in keys_map:
            if line.startswith(key + ":"):
                parts = line.split(": ")
                if len(parts) > 1:
                    value = parts[1].strip()
                    data[keys_map[key]] = value

    doc.close()

    formatted_data = json.dumps(data, ensure_ascii=False, indent=4)

    return formatted_data

# Запуск метода
formatted_info = read_and_format_pdf_info(pdf_path)
print(formatted_info)

# Механизм проверяющий другие входящие pdf-файлы на соответствие структуры эталона
def compare_pdf_structure(reference_pdf, test_pdf):

    reference_info = read_and_format_pdf_info(reference_pdf)

    test_info =read_and_format_pdf_info(test_pdf)

    if reference_info["metadata"] != test_info["metadata"]:
        print(f"Метаданные не совпадают для файла '{test_pdf}'.")
        return False

    if len(reference_info["pages"]) != len(test_info["pages"]):
        print(f"Количество страниц не совпадает для файла '{test_pdf}'.")
        return False

    for ref_page, test_page in zip(reference_info["pages"], test_info["pages"]):
        if ref_page["text"] != test_page["text"]:
            print(f"Текст на странице {ref_page['page_number']} не совпадает для файла '{test_pdf}'.")
            return False

    print(f"Файл '{test_pdf}' соответствует эталону.")
    return True
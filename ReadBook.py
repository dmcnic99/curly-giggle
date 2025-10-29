# read the DoubleSudoku202512.pdf file from ~/Dropbox/Puzzles
import os
from pypdf import PdfReader
import re

table_regex = r'(?s)\b(?:\w+\s+){2,}\w+\b(?:\s*[,;]\s*\b(?:\w+\s+){2,}\w+\b)*'


def read_double_sudoku_pdf(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    reader = PdfReader(file_path)
    text_content = []
    
    # for page in reader.pages:
    #     text_content.append(page.extract_text())
    # read the third page only and count the number of tables
    if len(reader.pages) < 3:
        raise ValueError("The PDF does not have enough pages.")
    third_page = reader.pages[2]
    text_content.append(third_page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False))

    # dfs = tabula.read_pdf(file_path, pages=3, multiple_tables=True)
    # print(f"Number of tables on page 3: {len(dfs)}")

    # Find all tables in page_text
    tables = re.findall(table_regex, third_page.extract_text(extraction_mode="layout"))
    # print(len(tables))
    # x = 9*9*2
    print(tables[1])
    rows = tables[1].split('\n')
    print(rows[1:19])
    
    return "\n".join(text_content)


if __name__ == "__main__":
    file_path = os.path.expanduser("~/Dropbox/Puzzles/DoubleSudoku202512.pdf")
    try:
        content = read_double_sudoku_pdf(file_path)
        # print(content)
    except FileNotFoundError as e:
        print(e)

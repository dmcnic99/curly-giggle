import argparse
import pdfplumber
import pandas as pd
from pathlib import Path


parser = argparse.ArgumentParser(description='Extract Double Sudoku puzzles from a PDF file and save them to a CSV file.')
# description = main.__doc__, formatter_class = argparse.RawTextHelpFormatter
parser.add_argument(
    '--book',
    required=True
)
args = parser.parse_args()
home = Path.home()
puzzle_dir = home / 'Dropbox' / 'Puzzles'

df = pd.DataFrame(columns=['Puzzle','Source'])
puzzle_number = 0
pdf = pdfplumber.open(puzzle_dir / f"{args.book}.pdf")
# get the pages with valid puzzles
pages = pdf.pages[2:191]
pages += pdf.pages[211:245]
pages += pdf.pages[266:285]
for page in pages:
    text = page.extract_text()
    # print(f"{text=}")
    tables = page.extract_tables()
    # print(f"{tables=}")
    if '\nEASY\n' in text or '\nMEDIUM\n' in text or '\nHARD\n' in text:
        for table in tables:
            # print(f"{table=}")
            puzzle = ''
            for row in table:
                # replace empty strings with '0'
                row = [cell if cell != '' else '0' for cell in row]
                # print(f"{row=}")
                puzzle += ''.join(row)
            # print(f"{puzzle=}")
            df.loc[puzzle_number] = [puzzle, '000'[:3 - len(str(puzzle_number+1))]+str(puzzle_number+1)]
            puzzle_number += 1
pdf.close()
# print(df)
df.to_csv(puzzle_dir / f'{args.book}.csv', index=False)


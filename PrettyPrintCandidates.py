with open('data/output/candidates.txt', 'r') as file:
    candidates = file.readlines()
rows = []
for candidate in candidates:
    # drop the first seven characters
    formatted_candidate = candidate[7:].strip()
    # print(formatted_candidate)
    # formatted_candidate looks like a list of lists. Convert it to an actual list of lists.
    candidate_list = eval(formatted_candidate)
    rows.append(candidate_list)

rows = [
    [
        ''.join(item) if isinstance(item, list) else item
        for item in row
    ]
    for row in rows
]

# print rows in a pretty format with borders around each item
from prettytable import PrettyTable
table = PrettyTable()
table.header=False
for i,row in enumerate(rows):
    table.add_row(row)
    if i==2 or i==5:
        table.add_divider()
print(table)
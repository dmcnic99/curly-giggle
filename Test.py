row = []
row.append([['2', '7'], ['5', '7', '8'], [], [], ['2', '5', '7'], [], ['5', '7', '8'], [], []])
row.append([[], ['5', '7', '8'], [], ['6', '9'], ['2', '5', '6', '7', '9'], ['2', '5', '9'], ['5', '7', '8', '9'], ['1', '5', '8'], ['1', '2', '5']])
row.append([['2', '7'], [], [], ['3', '9'], ['2', '3', '5', '7', '9'], [], ['5', '7', '9'], [], ['2', '5']])
row.append([[], [], ['1', '4', '8'], ['3', '4', '9'], ['3', '4', '8', '9'], [], ['4', '6', '8'], ['1', '6', '8'], ['1', '4']])
row.append([[], ['4', '7', '8'], ['1', '4', '7', '8'], [], ['4', '8'], [], ['4', '5', '8'], ['1', '5', '8'], []])
row.append([[], [], ['4', '8'], [], ['4', '8'], [], [], [], []])
row.append([[], [], ['4', '5'], [], ['4', '5', '9'], ['5', '9'], [], [], []])
row.append([[], ['4', '5', '7'], ['4', '5', '7'], ['4', '6'], ['2', '4', '5', '6'], ['2', '5'], [], [], []])
row.append([[], [], [], [], [], [], ['4', '5', '6'], ['5', '6'], ['4', '5']])

for r in row:
    pair = [x for x in row if len(x) == 2]
    if len(pair)==2 and pair[0]==pair[1]:
        # for each item in pair[0], drop it from each item in col
        for val in pair[0]:
            for i in range(len(r)):
                if r[i] != pair[0]:
                    if val in r[i]:
                        r[i].remove(val)
                        print(r)
# count the number of items in col with length == 1
# count = sum(1 for x in col if len(x) == 1)
# print("Count of items with length 1:", count)

def CreateColumns(row_list):
    return [[row[i] for row in row_list] for i in range(9)]
columns = CreateColumns(row)

puzzle_change = False

for n,col in enumerate(columns):
    two_candidates = [x for x in col if len(x) == 2]
    # find identical iteams in two_candidates
    pair = [x for x in two_candidates if two_candidates.count(x) == 2]
    if len(pair)==2 and pair[0]==pair[1]:
        pair_ndx = [[n,i] for i,x in enumerate(col) if x==pair[0]]
        # for each item in pair[0], drop it from each item in col
        for val in pair[0]:
            for i in range(len(col)):
                if col[i] != pair[0]:
                    if val in col[i]:
                        col[i].remove(val)
                        puzzle_change = True
                        columns[n] = col
                        print(f"c{n}:{col}")
    if puzzle_change:
        break

puzzle_change = False

# now figure out if the pairs are in the same square
if pair_ndx[0][1]//3 == pair_ndx[1][1]//3:
    square_row = pair_ndx[0][0]//3
    square_col = pair_ndx[0][1]//3
    print(f"Square found at {square_row},{square_col}")
    # now drop the values from other items in the square
    for i in range(square_row*3, square_row*3+3):
        for j in range(square_col*3, square_col*3+3):
            if [i,j] != pair_ndx[0] and [i,j] != pair_ndx[1]:
                for val in pair[0]:
                    if val in columns[i][j]:
                        columns[i][j].remove(val)
                        puzzle_change = True
                        print(f"square {i},{j}:{columns[i][j]}")
            if puzzle_change:
                break

# for col in columns:
#     print(col)

puzzle_change = False

for n,col in enumerate(columns):
    two_candidates = [x for x in col if len(x) == 2]
    # find identical iteams in two_candidates
    pair = [x for x in two_candidates if two_candidates.count(x) == 2]
    if len(pair)==2 and pair[0]==pair[1]:
        pair_ndx = [[n,i] for i,x in enumerate(col) if x==pair[0]]
        print(pair_ndx)
        # for each item in pair[0], drop it from each item in col
        for val in pair[0]:
            for i in range(len(col)):
                if col[i] != pair[0]:
                    if val in col[i]:
                        col[i].remove(val)
                        puzzle_change = True
                        columns[n] = col
                        print(f"c{n}:{col}")
    if puzzle_change:
        break

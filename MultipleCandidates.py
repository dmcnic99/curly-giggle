candidates = [[],['2','6'],['2','6'],[],['8','9'],[],['8','9'],[],[]]
# find the unique values in candidates
unique_candidates = []
for c in candidates:
    if len(c) == 2:
        if c not in unique_candidates:
            unique_candidates.append(c)
print("Unique candidates:", unique_candidates)
# for each unique candidate, print the index positions in candidates
for uc in unique_candidates:
    positions = [i for i, x in enumerate(candidates) if x == uc]
    if len(positions) == 2:
        print(f"Candidate {uc} found at positions {positions}")

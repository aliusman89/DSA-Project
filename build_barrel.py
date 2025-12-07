import os
import csv

INVERTED = "D:/DSA-Project/search_engine/backend/app/indexing/output/inverted_index.csv"
BARRELS_DIR = "D:/DSA-Project/search_engine/backend/app/indexing/barrels/"
NUM_BARRELS = 20   

os.makedirs(BARRELS_DIR, exist_ok=True)

# Pre-open all barrel files for fast writing
barrel_files = {}
writers = {}

for i in range(NUM_BARRELS):
    f = open(f"{BARRELS_DIR}barrel_{i}.csv", "w", newline="", encoding="utf-8")
    barrel_files[i] = f
    writers[i] = csv.writer(f)
    writers[i].writerow(["wordID", "docIDs"])

with open(INVERTED, "r", encoding="utf-8") as f:
    next(f)  

    for line in f:
        if not line.strip():
            continue

        word_id, docs = line.strip().split(",", 1)
        wid = int(word_id)

        barrel_id = wid % NUM_BARRELS
        writers[barrel_id].writerow([wid, docs])
# ClosING all files at once
for f in barrel_files.values():
    f.close()

print("barrels created successfully")

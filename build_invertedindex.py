import os, json, gzip, re, csv
from collections import defaultdict

JSON_PATH = "D:/DATA/"
LEXICON = "D:/DSA-Project/search_engine/backend/app/indexing/output/lexicon.csv"
OUTPUT = "D:/DSA-Project/search_engine/backend/app/indexing/output/inverted_index.csv"

def tokenize(t):
    return re.findall(r"[a-z0-9]+", t.lower())

lex = {}
with open(LEXICON, encoding="utf-8") as f:
    next(f)
    for line in f:
        w, i = line.strip().split(",")
        lex[w] = int(i)

index = defaultdict(set)
doc_id = 1

for file in os.listdir(JSON_PATH):
    path = os.path.join(JSON_PATH, file)
    f = gzip.open(path, "rt", encoding="utf-8") if file.endswith(".gz") else open(path, encoding="utf-8")
    data = json.load(f)

    text = ""
    for sec in data.get("abstract", []):
        text += sec.get("text", "") + " "
    for sec in data.get("body_text", []):
        text += sec.get("text", "") + " "

    for token in tokenize(text):
        if token in lex:
            index[lex[token]].add(doc_id)

    doc_id += 1

with open(OUTPUT, "w", newline="", encoding="utf-8") as out:
    writer = csv.writer(out)
    writer.writerow(["wordID", "docIDs"])
    for wid, docs in index.items():
        writer.writerow([wid, " ".join(map(str, docs))])

print("Inverted index created")

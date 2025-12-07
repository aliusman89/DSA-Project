import os, json, gzip, re, csv

JSON_PATH = "D:/DATA/"
LEXICON = "D:/DSA-Project/search_engine/backend/app/indexing/output/lexicon.csv"
OUTPUT = "D:/DSA-Project/search_engine/backend/app/indexing/output/forward_index.csv"

def tokenize(t):
    return re.findall(r"[a-z0-9]+", t.lower())

# load lexicon
lex = {}
with open(LEXICON, encoding="utf-8") as f:
    next(f)
    for line in f:
        w, i = line.strip().split(",")
        lex[w] = int(i)

with open(OUTPUT, "w", newline="", encoding="utf-8") as out:
    writer = csv.writer(out)
    writer.writerow(["docID", "wordIDs"])

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

        ids = [str(lex[t]) for t in tokenize(text) if t in lex]
        writer.writerow([doc_id, " ".join(ids)])

        doc_id += 1

print("Forward index created")

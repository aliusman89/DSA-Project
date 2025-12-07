import os, json, gzip, re

JSON_PATH = "D:/DATA"
OUTPUT = "D:/DSA-Project/search_engine/backend/app/indexing/output/lexicon.csv"

def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())

lexicon = {}
word_id = 1

def process_file(path):
    global word_id
    if path.endswith(".gz"):
        f = gzip.open(path, "rt", encoding="utf-8")
    else:
        f = open(path, "r", encoding="utf-8")

    data = json.load(f)

    text = ""
    if "abstract" in data:
        for x in data["abstract"]:
            text += x.get("text", "") + " "
    if "body_text" in data:
        for x in data["body_text"]:
            text += x.get("text", "") + " "

    for token in tokenize(text):
        if token not in lexicon:
            lexicon[token] = word_id
            word_id += 1

for file in os.listdir(JSON_PATH):
    process_file(os.path.join(JSON_PATH, file))

with open(OUTPUT, "w", encoding="utf-8") as out:
    out.write("word,wordID\n")
    for w, i in lexicon.items():
        out.write(f"{w},{i}\n")

print("Lexicon created")

#include <iostream>
#include <fstream>
#include <filesystem>
#include <map>
#include <vector>
#include <sstream>
#include <algorithm>

using namespace std;
namespace fs = std::filesystem;

string DOCS_PATH = "D:/Dataset/Cleaned1/";
string OUTPUT_PATH = "D:/DSA-Project/search_engine/backend/app/indexing/output/";
string LEXICON_PATH = "D:/DSA-Project/search_engine/backend/app/indexing/output/lexicon.csv";

vector<string> tokenize(const string &text) {
    vector<string> tokens;
    string word;

    for (char c : text) {
        if (isalnum(c)) word += tolower(c);
        else {
            if (!word.empty()) {
                tokens.push_back(word);
                word.clear();
            }
        }
    }
    if (!word.empty()) tokens.push_back(word);

    return tokens;
}

map<string, int> loadLexicon() {
    map<string, int> lex;
    ifstream in(LEXICON_PATH);
    string word, line;
    getline(in, line);

    while (getline(in, line)) {
        stringstream ss(line);
        string w, wid;
        getline(ss, w, ',');
        getline(ss, wid, ',');
        lex[w] = stoi(wid);
    }

    return lex;
}

int main() {
    map<string, int> lexicon = loadLexicon();
    map<int, vector<int>> forwardIndex;
    int docID = 1;

    for (const auto &file : fs::directory_iterator(DOCS_PATH)) {
        if (file.path().extension() == ".txt") {
            ifstream in(file.path());
            stringstream buffer;
            buffer << in.rdbuf();
            string text = buffer.str();
            vector<string> tokens = tokenize(text);

            vector<int> wordIDs;
            for (auto &t : tokens) {
                if (lexicon.count(t)) {
                    wordIDs.push_back(lexicon[t]);
                }
            }
            forwardIndex[docID++] = wordIDs;
        }
    }

    ofstream out(OUTPUT_PATH + "forward_index.csv");
    out << "docID,wordIDs\n";

    for (auto &p : forwardIndex) {
        out << p.first << ",";
        for (int id : p.second) out << id << " ";
        out << "\n";
    }

    cout << "forward_index.csv generated!" << endl;
    return 0;
}

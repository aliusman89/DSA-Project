#include <iostream>
#include <fstream>
#include <filesystem>
#include <map>
#include <vector>
#include <sstream>
#include <algorithm>

using namespace std;
namespace fs = std::filesystem;

string OUTPUT_PATH = "D:/DSA-Project/search_engine/backend/app/indexing/output/";
string DOCS_PATH = "D:/Dataset/Cleaned1/";

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

int main() {
    map<string, int> lexicon;
    int wordID = 1;

    for (const auto &file : fs::directory_iterator(DOCS_PATH)) {
        if (file.path().extension() == ".txt") {
            ifstream in(file.path());
            stringstream buffer;
            buffer << in.rdbuf();
            string text = buffer.str();
            vector<string> tokens = tokenize(text);

            for (auto &t : tokens) {
                if (lexicon.find(t) == lexicon.end()) {
                    lexicon[t] = wordID++;
                }
            }
        }
    }

    ofstream out(OUTPUT_PATH + "lexicon.csv");
    out << "word,wordID\n";
    for (auto &p : lexicon) {
        out << p.first << "," << p.second << "\n";
    }

    cout << "lexicon.csv generated!" << endl;
    return 0;
}

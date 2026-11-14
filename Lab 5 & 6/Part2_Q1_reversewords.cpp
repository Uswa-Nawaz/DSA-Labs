#include <iostream>
#include <string>
using namespace std;
 
// ---------- a stack of strings (linked-list based, same idea as your Q2 LinkedStack) ----------
struct SNode {
    string data;
    SNode* next;
    SNode(const string& s) : data(s), next(NULL) {}
};
 
class StringStack {
    SNode* top;                          // top of stack = head of list, so push/pop are O(1)
public:
    StringStack() : top(NULL) {}
    ~StringStack() { string tmp; while (pop(tmp)) {} }
    StringStack(const StringStack&) = delete;
    StringStack& operator=(const StringStack&) = delete;
 
    bool isEmpty() { return top == NULL; }
 
    void push(const string& s) {
        SNode* n = new SNode(s);
        n->next = top;
        top = n;
    }
    bool pop(string& out) {
        if (isEmpty()) return false;     // underflow
        SNode* tmp = top;
        out = tmp->data;
        top = top->next;
        delete tmp;
        return true;
    }
};
 
// ---------- the algorithm ----------
string reverseWords(const string& sentence) {
    StringStack st;
    string word = "";                    // the word we are currently building
 
    for (size_t i = 0; i < sentence.length(); i++) {
        char c = sentence[i];
        if (c == ' ') {
            if (word != "") {            // a space ends the word (ignore extra spaces)
                st.push(word);
                word = "";
            }
        } else {
            word += c;                   // still inside a word: keep collecting letters
        }
    }
    if (word != "") st.push(word);       // the LAST word has no space after it, so push it here
 
    string result = "";
    string w;
    while (st.pop(w)) {                  // last word pushed comes out first = reversed order
        if (result != "") result += " ";
        result += w;
    }
    return result;
}
 
int main() {
    string sentence = "I am from University of Engineering and Technology Lahore";
    cout << "Input:  " << sentence << "\n";
    cout << "Output: " << reverseWords(sentence) << "\n\n";
 
    cout << "Try your own sentence: ";
    getline(cin, sentence);
    cout << "Output: " << reverseWords(sentence) << "\n";
    return 0;
}
 
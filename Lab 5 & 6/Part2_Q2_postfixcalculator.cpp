// CS200L Lab 5 - Part 2, Q2: Postfix (RPN) calculator using a stack.
// Input tokens are separated by spaces/newlines:
//   integer  -> push it
//   + - * / % -> pop two, compute, push result
//   ?        -> print the whole stack (toString)
//   ^        -> pop the top element and print only that
//   !        -> exit
#include <iostream>
#include <string>
using namespace std;
 
struct Node {
    int data;
    Node* next;
    Node(int x) : data(x), next(NULL) {}
};
 
class LinkedStack {
    Node* top;                         // top of stack = head of list
    int count;                         // how many elements, so we can check "are there 2 operands?"
public:
    LinkedStack() : top(NULL), count(0) {}
    ~LinkedStack() { int tmp; while (pop(tmp)) {} }
    LinkedStack(const LinkedStack&) = delete;
    LinkedStack& operator=(const LinkedStack&) = delete;
 
    bool isEmpty() { return top == NULL; }
    int  size()    { return count; }
 
    void push(int x) {
        Node* n = new Node(x);
        n->next = top;
        top = n;
        count++;
    }
    bool pop(int& out) {
        if (isEmpty()) return false;   // underflow
        Node* tmp = top;
        out = tmp->data;
        top = top->next;
        delete tmp;
        count--;
        return true;
    }
 
    // Bottom ... top, e.g. "[ 3 4 7 ]". The list runs top->bottom, so we build the text backwards.
    string toString() {
        string s = " ]";
        for (Node* c = top; c != NULL; c = c->next)
            s = " " + to_string(c->data) + s;
        return "[" + s;
    }
};
 
// Is the token a valid integer? Accepts digits with an optional leading '-' (so "-42" yes, "-" alone no).
bool isInteger(const string& t) {
    size_t start = (t[0] == '-') ? 1 : 0;
    if (start == t.length()) return false;          // just "-" is the minus operator, not a number
    for (size_t i = start; i < t.length(); i++)
        if (t[i] < '0' || t[i] > '9') return false;
    return true;
}
 
bool isOperator(const string& t) {
    return t.length() == 1 &&
           (t[0] == '+' || t[0] == '-' || t[0] == '*' || t[0] == '/' || t[0] == '%');
}
 
int main() {
    LinkedStack st;
    string tok;
    cout << "Postfix calculator.  Integers, + - * / %,  ? (show stack),  ^ (pop & print),  ! (exit)\n";
 
    while (cin >> tok) {
        if (tok == "!") {
            break;
        }
        else if (tok == "?") {
            cout << st.toString() << "\n";
        }
        else if (tok == "^") {
            int v;
            if (st.pop(v)) cout << v << "\n";
            else cout << "Error: stack is empty\n";
        }
        else if (isInteger(tok)) {                  // check this BEFORE operators so "-42" isn't read as '-'
            st.push(stoi(tok));
        }
        else if (isOperator(tok)) {
            if (st.size() < 2) {                    // need two operands; leave the stack untouched
                cout << "Error: '" << tok << "' needs two operands\n";
                continue;
            }
            int b, a;
            st.pop(b);                              // FIRST pop is the RIGHT operand
            st.pop(a);                              // second pop is the LEFT operand
            char op = tok[0];
            if ((op == '/' || op == '%') && b == 0) {
                cout << "Error: division by zero\n";
                st.push(a);                         // put the operands back so nothing is lost
                st.push(b);
                continue;
            }
            int r = 0;
            if      (op == '+') r = a + b;
            else if (op == '-') r = a - b;
            else if (op == '*') r = a * b;
            else if (op == '/') r = a / b;
            else                r = a % b;
            st.push(r);
        }
        else {
            cout << "Error: invalid token '" << tok << "'\n";
        }
    }
    return 0;
}
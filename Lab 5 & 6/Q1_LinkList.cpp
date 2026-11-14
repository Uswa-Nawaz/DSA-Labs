//Part 1, Q1: Singly LinkList
#include <iostream>
using namespace std;

struct Node {
    int data;
    Node* next;
    Node(int x) : data(x), next(NULL) {}
};

class LinkList {
public:
    LinkList() { head = NULL; }
    ~LinkList();                               // frees every node
    bool isEmpty() { return head == NULL; }
    Node* getHead() { return head; }           // so main() can pass our list to the "Node* list" functions

    Node* insertNode(int index, int x);        // insert at given index (0-based)
    Node* insertAtHead(int x);
    Node* insertAtEnd(int x);
    bool  findNode(int x);
    bool  deleteNode(int x);                   // deletes ALL occurrences of x
    bool  deleteFromStart();
    bool  deleteFromEnd();
    void  displayList();

    // These work on any list passed in and return the head of a NEW list.
    Node* reverseList();                       // reverses THIS list, returns a new list
    Node* sortList(Node* list);
    Node* removeDuplicates(Node* list);
    Node* mergeLists(Node* list1, Node* list2);
    Node* interestLists(Node* list1, Node* list2);   // intersection (name as given in manual)

    // helpers
    static void printList(Node* list);
    static void freeList(Node* list);

private:
    Node* head;
    static bool contains(Node* list, int x);
    static void appendTo(Node*& h, Node*& t, int x);   // O(1) append using a tail pointer
};

// ---------- helpers ----------
bool LinkList::contains(Node* list, int x) {
    for (Node* c = list; c != NULL; c = c->next)
        if (c->data == x) return true;
    return false;
}

void LinkList::appendTo(Node*& h, Node*& t, int x) {
    Node* n = new Node(x);
    if (h == NULL) h = t = n;
    else { t->next = n; t = n; }
}

void LinkList::printList(Node* list) {
    if (list == NULL) { cout << "(empty)\n"; return; }
    for (Node* c = list; c != NULL; c = c->next)
        cout << c->data << (c->next ? " -> " : "");
    cout << " -> NULL\n";
}

void LinkList::freeList(Node* list) {
    while (list != NULL) {
        Node* tmp = list;
        list = list->next;
        delete tmp;
    }
}

LinkList::~LinkList() { freeList(head); head = NULL; }

// ---------- insertion ----------
Node* LinkList::insertAtHead(int x) {
    Node* n = new Node(x);
    n->next = head;
    head = n;
    return n;
}

Node* LinkList::insertAtEnd(int x) {
    Node* n = new Node(x);
    if (head == NULL) { head = n; return n; }
    Node* cur = head;
    while (cur->next != NULL) cur = cur->next;   // walk to last node: O(n)
    cur->next = n;
    return n;
}

Node* LinkList::insertNode(int index, int x) {
    if (index < 0) return NULL;
    if (index == 0) return insertAtHead(x);
    Node* prev = head;                           // we need the node BEFORE the position
    for (int i = 0; i < index - 1 && prev != NULL; i++) prev = prev->next;
    if (prev == NULL) return NULL;               // index is beyond the end of the list
    Node* n = new Node(x);
    n->next = prev->next;
    prev->next = n;
    return n;
}

// ---------- search / delete ----------
bool LinkList::findNode(int x) { return contains(head, x); }

bool LinkList::deleteNode(int x) {
    bool deleted = false;
    while (head != NULL && head->data == x) {    // case 1: matches at the head (maybe repeatedly)
        Node* tmp = head;
        head = head->next;
        delete tmp;
        deleted = true;
    }
    Node* cur = head;
    while (cur != NULL && cur->next != NULL) {   // case 2: matches later in the list
        if (cur->next->data == x) {
            Node* tmp = cur->next;
            cur->next = tmp->next;
            delete tmp;
            deleted = true;                      // don't advance: new cur->next may also match
        } else {
            cur = cur->next;
        }
    }
    return deleted;
}

bool LinkList::deleteFromStart() {
    if (head == NULL) return false;
    Node* tmp = head;
    head = head->next;
    delete tmp;
    return true;
}

bool LinkList::deleteFromEnd() {
    if (head == NULL) return false;
    if (head->next == NULL) { delete head; head = NULL; return true; }
    Node* cur = head;
    while (cur->next->next != NULL) cur = cur->next;   // stop at second-last node
    delete cur->next;
    cur->next = NULL;
    return true;
}

void LinkList::displayList() { printList(head); }

// ---------- list algorithms (each returns a NEW list) ----------
Node* LinkList::reverseList() {
    Node* result = NULL;
    for (Node* c = head; c != NULL; c = c->next) {
        Node* n = new Node(c->data);             // inserting each node at the front reverses the order
        n->next = result;
        result = n;
    }
    return result;
}

Node* LinkList::sortList(Node* list) {           // ascending, via sorted insertion: O(n^2)
    Node* result = NULL;
    for (Node* c = list; c != NULL; c = c->next) {
        Node* n = new Node(c->data);
        if (result == NULL || n->data < result->data) {
            n->next = result;
            result = n;
        } else {
            Node* p = result;
            while (p->next != NULL && p->next->data <= n->data) p = p->next;
            n->next = p->next;
            p->next = n;
        }
    }
    return result;
}

Node* LinkList::removeDuplicates(Node* list) {   // keeps first occurrence of each value
    Node *h = NULL, *t = NULL;
    for (Node* c = list; c != NULL; c = c->next)
        if (!contains(h, c->data)) appendTo(h, t, c->data);
    return h;
}

Node* LinkList::mergeLists(Node* list1, Node* list2) {   // list1's nodes followed by list2's
    Node *h = NULL, *t = NULL;
    for (Node* c = list1; c != NULL; c = c->next) appendTo(h, t, c->data);
    for (Node* c = list2; c != NULL; c = c->next) appendTo(h, t, c->data);
    return h;
}

Node* LinkList::interestLists(Node* list1, Node* list2) {  // values present in both (no repeats)
    Node *h = NULL, *t = NULL;
    for (Node* c = list1; c != NULL; c = c->next)
        if (contains(list2, c->data) && !contains(h, c->data)) appendTo(h, t, c->data);
    return h;
}

// ---------- test driver ----------
int main() {
    LinkList a;
    a.insertAtEnd(5); a.insertAtEnd(3); a.insertAtEnd(8); a.insertAtEnd(3); a.insertAtHead(1);
    cout << "List a:            "; a.displayList();

    a.insertNode(2, 99);
    cout << "insertNode(2,99):  "; a.displayList();
    cout << "insertNode(50,7) -> " << (a.insertNode(50, 7) == NULL ? "NULL (bad index)" : "inserted") << "\n";
    cout << "findNode(8): " << a.findNode(8) << "   findNode(42): " << a.findNode(42) << "\n";

    Node* rev = a.reverseList();
    cout << "reverseList():     "; LinkList::printList(rev);
    Node* sorted = a.sortList(a.getHead());
    cout << "sortList():        "; LinkList::printList(sorted);
    Node* nodup = a.removeDuplicates(a.getHead());
    cout << "removeDuplicates():"; LinkList::printList(nodup);

    LinkList b;
    b.insertAtEnd(3); b.insertAtEnd(10); b.insertAtEnd(1); b.insertAtEnd(3);
    cout << "List b:            "; b.displayList();
    Node* merged = a.mergeLists(a.getHead(), b.getHead());
    cout << "mergeLists(a,b):   "; LinkList::printList(merged);
    Node* inter = a.interestLists(a.getHead(), b.getHead());
    cout << "interestLists(a,b):"; LinkList::printList(inter);

    cout << "\ndeleteNode(3) -> " << a.deleteNode(3) << "  ";  a.displayList();
    cout << "deleteNode(42) -> " << a.deleteNode(42) << "\n";
    a.deleteFromStart(); cout << "deleteFromStart(): "; a.displayList();
    a.deleteFromEnd();   cout << "deleteFromEnd():   "; a.displayList();
    while (a.deleteFromEnd()) {}
    cout << "emptied: isEmpty=" << a.isEmpty() << "  deleteFromStart on empty -> " << a.deleteFromStart() << "\n";

    LinkList::freeList(rev); LinkList::freeList(sorted); LinkList::freeList(nodup);
    LinkList::freeList(merged); LinkList::freeList(inter);
    return 0;
}

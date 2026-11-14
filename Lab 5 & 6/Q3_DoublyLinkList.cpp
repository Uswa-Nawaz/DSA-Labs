// CS200L Lab 5 - Part 1, Q3: Doubly LinkList (Data, Next, Prev) + complexity comparison
#include <iostream>
using namespace std;

struct DNode {
    int data;
    DNode* next;
    DNode* prev;
    DNode(int x) : data(x), next(NULL), prev(NULL) {}
};

class DoublyLinkList {
public:
    DoublyLinkList() { head = tail = NULL; }
    ~DoublyLinkList() { freeList(head); head = tail = NULL; }
    bool   isEmpty() { return head == NULL; }
    DNode* getHead() { return head; }

    DNode* insertNode(int index, int x);
    DNode* insertAtHead(int x);
    DNode* insertAtEnd(int x);
    bool   findNode(int x);
    bool   deleteNode(int x);                 // all occurrences
    bool   deleteFromStart();
    bool   deleteFromEnd();
    void   displayList();                     // forward
    void   displayReverse();                  // backward (only possible because of prev)

    DNode* reverseList();                     // returns a NEW reversed list
    DNode* sortList(DNode* list);
    DNode* removeDuplicates(DNode* list);
    DNode* mergeLists(DNode* list1, DNode* list2);
    DNode* interestLists(DNode* list1, DNode* list2);

    static void printList(DNode* list);
    static void freeList(DNode* list);

private:
    DNode* head;
    DNode* tail;                              // tail pointer: this is what makes the end O(1)
    static bool contains(DNode* list, int x);
    static void appendTo(DNode*& h, DNode*& t, int x);
    void unlink(DNode* n);                    // remove a node we already have a pointer to: O(1)
};

// ---------- helpers ----------
bool DoublyLinkList::contains(DNode* list, int x) {
    for (DNode* c = list; c != NULL; c = c->next)
        if (c->data == x) return true;
    return false;
}

void DoublyLinkList::appendTo(DNode*& h, DNode*& t, int x) {
    DNode* n = new DNode(x);
    if (h == NULL) h = t = n;
    else { t->next = n; n->prev = t; t = n; }
}

void DoublyLinkList::printList(DNode* list) {
    if (list == NULL) { cout << "(empty)\n"; return; }
    cout << "NULL <-> ";
    for (DNode* c = list; c != NULL; c = c->next)
        cout << c->data << " <-> ";
    cout << "NULL\n";
}

void DoublyLinkList::freeList(DNode* list) {
    while (list != NULL) {
        DNode* tmp = list;
        list = list->next;
        delete tmp;
    }
}

void DoublyLinkList::unlink(DNode* n) {
    // no walking needed: n->prev tells us who is behind it
    if (n->prev) n->prev->next = n->next; else head = n->next;
    if (n->next) n->next->prev = n->prev; else tail = n->prev;
    delete n;
}

// ---------- insertion ----------
DNode* DoublyLinkList::insertAtHead(int x) {
    DNode* n = new DNode(x);
    n->next = head;
    if (head) head->prev = n; else tail = n;
    head = n;
    return n;
}

DNode* DoublyLinkList::insertAtEnd(int x) {   // O(1): no walking, thanks to tail
    DNode* n = new DNode(x);
    n->prev = tail;
    if (tail) tail->next = n; else head = n;
    tail = n;
    return n;
}

DNode* DoublyLinkList::insertNode(int index, int x) {
    if (index < 0) return NULL;
    if (index == 0) return insertAtHead(x);
    DNode* cur = head;                        // find the node currently AT index
    for (int i = 0; i < index && cur != NULL; i++) cur = cur->next;
    if (cur == NULL) {                        // cur fell off the end: valid only if index == size
        int size = 0;
        for (DNode* c = head; c != NULL; c = c->next) size++;
        if (index == size) return insertAtEnd(x);
        return NULL;
    }
    DNode* n = new DNode(x);                  // insert BEFORE cur
    n->prev = cur->prev;
    n->next = cur;
    cur->prev->next = n;
    cur->prev = n;
    return n;
}

// ---------- search / delete ----------
bool DoublyLinkList::findNode(int x) { return contains(head, x); }

bool DoublyLinkList::deleteNode(int x) {
    bool deleted = false;
    DNode* cur = head;
    while (cur != NULL) {
        DNode* nxt = cur->next;               // save before cur may be deleted
        if (cur->data == x) { unlink(cur); deleted = true; }
        cur = nxt;
    }
    return deleted;
}

bool DoublyLinkList::deleteFromStart() {
    if (head == NULL) return false;
    unlink(head);
    return true;
}

bool DoublyLinkList::deleteFromEnd() {        // O(1): tail->prev gives the new last node
    if (tail == NULL) return false;
    unlink(tail);
    return true;
}

void DoublyLinkList::displayList() { printList(head); }

void DoublyLinkList::displayReverse() {
    if (tail == NULL) { cout << "(empty)\n"; return; }
    cout << "NULL <-> ";
    for (DNode* c = tail; c != NULL; c = c->prev) cout << c->data << " <-> ";
    cout << "NULL\n";
}

// ---------- list algorithms (each returns a NEW list) ----------
DNode* DoublyLinkList::reverseList() {
    DNode *h = NULL, *t = NULL;
    for (DNode* c = tail; c != NULL; c = c->prev)   // walk backwards using prev, append in that order
        appendTo(h, t, c->data);
    return h;
}

DNode* DoublyLinkList::sortList(DNode* list) {
    DNode* result = NULL;
    for (DNode* c = list; c != NULL; c = c->next) {
        DNode* n = new DNode(c->data);
        if (result == NULL || n->data < result->data) {
            n->next = result;
            if (result) result->prev = n;
            result = n;
        } else {
            DNode* p = result;
            while (p->next != NULL && p->next->data <= n->data) p = p->next;
            n->next = p->next;
            n->prev = p;
            if (p->next) p->next->prev = n;
            p->next = n;
        }
    }
    return result;
}

DNode* DoublyLinkList::removeDuplicates(DNode* list) {
    DNode *h = NULL, *t = NULL;
    for (DNode* c = list; c != NULL; c = c->next)
        if (!contains(h, c->data)) appendTo(h, t, c->data);
    return h;
}

DNode* DoublyLinkList::mergeLists(DNode* list1, DNode* list2) {
    DNode *h = NULL, *t = NULL;
    for (DNode* c = list1; c != NULL; c = c->next) appendTo(h, t, c->data);
    for (DNode* c = list2; c != NULL; c = c->next) appendTo(h, t, c->data);
    return h;
}

DNode* DoublyLinkList::interestLists(DNode* list1, DNode* list2) {
    DNode *h = NULL, *t = NULL;
    for (DNode* c = list1; c != NULL; c = c->next)
        if (contains(list2, c->data) && !contains(h, c->data)) appendTo(h, t, c->data);
    return h;
}

/* =====================================================================
   TIME COMPLEXITY: LinkList (singly, head only) vs DoublyLinkList (head + tail)
   n = number of nodes

   Operation                         Singly     Doubly
   ---------------------------------------------------------
   insertAtHead                      O(1)       O(1)
   insertAtEnd                       O(n)       O(1)   <- tail pointer
   insertNode(index)                 O(n)       O(n)   (still must walk to the index)
   findNode                          O(n)       O(n)
   deleteFromStart                   O(1)       O(1)
   deleteFromEnd                     O(n)       O(1)   <- tail->prev, no walking
   deleteNode(x) (all occurrences)   O(n)       O(n)
   Delete a node you already hold    O(n)       O(1)   <- singly needs the previous node
   Traverse backwards                not possible  O(n)
   reverseList / sort / merge / ...  same as singly (dominated by traversal / comparisons)

   Cost: every doubly node stores an extra pointer (more memory), and every
   insert/delete must keep two links correct (more room for bugs).
   ===================================================================== */

// ---------- test driver ----------
int main() {
    DoublyLinkList a;
    a.insertAtEnd(5); a.insertAtEnd(3); a.insertAtEnd(8); a.insertAtEnd(3); a.insertAtHead(1);
    cout << "List a:            "; a.displayList();
    cout << "Backwards:         "; a.displayReverse();

    a.insertNode(2, 99);
    cout << "insertNode(2,99):  "; a.displayList();
    a.insertNode(6, 77);                      // index == size -> appends
    cout << "insertNode(6,77):  "; a.displayList();
    cout << "insertNode(50,7) -> " << (a.insertNode(50, 7) == NULL ? "NULL (bad index)" : "inserted") << "\n";
    cout << "findNode(8): " << a.findNode(8) << "   findNode(42): " << a.findNode(42) << "\n";

    DNode* rev = a.reverseList();
    cout << "reverseList():     "; DoublyLinkList::printList(rev);
    DNode* sorted = a.sortList(a.getHead());
    cout << "sortList():        "; DoublyLinkList::printList(sorted);
    DNode* nodup = a.removeDuplicates(a.getHead());
    cout << "removeDuplicates():"; DoublyLinkList::printList(nodup);

    DoublyLinkList b;
    b.insertAtEnd(3); b.insertAtEnd(10); b.insertAtEnd(1); b.insertAtEnd(3);
    DNode* merged = a.mergeLists(a.getHead(), b.getHead());
    cout << "mergeLists(a,b):   "; DoublyLinkList::printList(merged);
    DNode* inter = a.interestLists(a.getHead(), b.getHead());
    cout << "interestLists(a,b):"; DoublyLinkList::printList(inter);

    cout << "\ndeleteNode(3) -> " << a.deleteNode(3) << "  "; a.displayList();
    a.deleteFromStart(); cout << "deleteFromStart(): "; a.displayList();
    a.deleteFromEnd();   cout << "deleteFromEnd():   "; a.displayList();
    cout << "Backwards:         "; a.displayReverse();
    while (a.deleteFromEnd()) {}
    cout << "emptied: isEmpty=" << a.isEmpty() << "\n";

    DoublyLinkList::freeList(rev); DoublyLinkList::freeList(sorted); DoublyLinkList::freeList(nodup);
    DoublyLinkList::freeList(merged); DoublyLinkList::freeList(inter);
    return 0;
}

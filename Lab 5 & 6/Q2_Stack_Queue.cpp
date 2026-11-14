// CS200L Lab 5 - Part 1, Q2: Stack and Queue
//   (a) array based   (b) linked-list based
#include <iostream>
using namespace std;

// =====================================================
// (a) ARRAY-BASED
// =====================================================
class ArrayStack {
    int* arr;
    int capacity;
    int topIdx;                       // index of top element, -1 when empty
public:
    ArrayStack(int cap = 5) : capacity(cap), topIdx(-1) { arr = new int[cap]; }
    ~ArrayStack() { delete[] arr; }
    ArrayStack(const ArrayStack&) = delete;
    ArrayStack& operator=(const ArrayStack&) = delete;

    bool isEmpty() { return topIdx == -1; }
    bool isFull()  { return topIdx == capacity - 1; }

    bool push(int x) {
        if (isFull()) { cout << "Overflow: stack is full\n"; return false; }
        arr[++topIdx] = x;
        return true;
    }
    bool pop(int& out) {
        if (isEmpty()) { cout << "Underflow: stack is empty\n"; return false; }
        out = arr[topIdx--];
        return true;
    }
    bool peek(int& out) {
        if (isEmpty()) { cout << "Stack is empty\n"; return false; }
        out = arr[topIdx];
        return true;
    }
    void display() {                  // bottom ... top
        cout << "[ ";
        for (int i = 0; i <= topIdx; i++) cout << arr[i] << " ";
        cout << "] <- top\n";
    }
};

// Circular queue: indices wrap around so freed slots at the front get reused
class ArrayQueue {
    int* arr;
    int capacity;
    int frontIdx;
    int count;
public:
    ArrayQueue(int cap = 5) : capacity(cap), frontIdx(0), count(0) { arr = new int[cap]; }
    ~ArrayQueue() { delete[] arr; }
    ArrayQueue(const ArrayQueue&) = delete;
    ArrayQueue& operator=(const ArrayQueue&) = delete;

    bool isEmpty() { return count == 0; }
    bool isFull()  { return count == capacity; }

    bool enqueue(int x) {
        if (isFull()) { cout << "Overflow: queue is full\n"; return false; }
        arr[(frontIdx + count) % capacity] = x;   // next free slot after the last element
        count++;
        return true;
    }
    bool dequeue(int& out) {
        if (isEmpty()) { cout << "Underflow: queue is empty\n"; return false; }
        out = arr[frontIdx];
        frontIdx = (frontIdx + 1) % capacity;
        count--;
        return true;
    }
    bool peek(int& out) {
        if (isEmpty()) { cout << "Queue is empty\n"; return false; }
        out = arr[frontIdx];
        return true;
    }
    void display() {
        cout << "front -> ";
        for (int i = 0; i < count; i++) cout << arr[(frontIdx + i) % capacity] << " ";
        cout << "<- rear\n";
    }
};

// =====================================================
// (b) LINKED-LIST-BASED  (no fixed capacity)
// =====================================================
struct Node {
    int data;
    Node* next;
    Node(int x) : data(x), next(NULL) {}
};

class LinkedStack {
    Node* top;                        // top of stack = head of list, so push/pop are O(1)
public:
    LinkedStack() : top(NULL) {}
    ~LinkedStack() { int tmp; while (pop(tmp)) {} }
    LinkedStack(const LinkedStack&) = delete;
    LinkedStack& operator=(const LinkedStack&) = delete;

    bool isEmpty() { return top == NULL; }
    bool isFull()  { return false; }  // only runs out if the heap does

    bool push(int x) {
        Node* n = new Node(x);
        n->next = top;
        top = n;
        return true;
    }
    bool pop(int& out) {
        if (isEmpty()) return false;  // caller decides whether to report underflow
        Node* tmp = top;
        out = tmp->data;
        top = top->next;
        delete tmp;
        return true;
    }
    bool peek(int& out) {
        if (isEmpty()) return false;
        out = top->data;
        return true;
    }
    void display() {                  // top first
        cout << "top -> ";
        for (Node* c = top; c != NULL; c = c->next) cout << c->data << " ";
        cout << "\n";
    }
};

class LinkedQueue {
    Node* front;                      // dequeue from head
    Node* rear;                       // enqueue at tail (tail pointer keeps this O(1))
public:
    LinkedQueue() : front(NULL), rear(NULL) {}
    ~LinkedQueue() { int tmp; while (dequeue(tmp)) {} }
    LinkedQueue(const LinkedQueue&) = delete;
    LinkedQueue& operator=(const LinkedQueue&) = delete;

    bool isEmpty() { return front == NULL; }
    bool isFull()  { return false; }

    bool enqueue(int x) {
        Node* n = new Node(x);
        if (rear == NULL) front = rear = n;
        else { rear->next = n; rear = n; }
        return true;
    }
    bool dequeue(int& out) {
        if (isEmpty()) return false;
        Node* tmp = front;
        out = tmp->data;
        front = front->next;
        if (front == NULL) rear = NULL;          // queue became empty: reset rear too
        delete tmp;
        return true;
    }
    bool peek(int& out) {
        if (isEmpty()) return false;
        out = front->data;
        return true;
    }
    void display() {
        cout << "front -> ";
        for (Node* c = front; c != NULL; c = c->next) cout << c->data << " ";
        cout << "<- rear\n";
    }
};

// =====================================================
// Test driver
// =====================================================
int main() {
    int v;

    cout << "=== ArrayStack (capacity 3) ===\n";
    ArrayStack as(3);
    as.push(10); as.push(20); as.push(30);
    as.push(40);                                   // Overflow
    as.display();
    as.peek(v);  cout << "peek: " << v << "\n";
    as.pop(v);   cout << "pop: " << v << "\n";
    as.pop(v); as.pop(v);
    as.pop(v);                                     // Underflow

    cout << "\n=== ArrayQueue (capacity 3) ===\n";
    ArrayQueue aq(3);
    aq.enqueue(1); aq.enqueue(2); aq.enqueue(3);
    aq.enqueue(4);                                 // Overflow
    aq.dequeue(v); cout << "dequeue: " << v << "\n";
    aq.enqueue(4);                                 // works: circular wrap-around reuses the freed slot
    aq.display();
    aq.peek(v); cout << "peek: " << v << "  isFull: " << aq.isFull() << "\n";

    cout << "\n=== LinkedStack ===\n";
    LinkedStack ls;
    ls.push(1); ls.push(2); ls.push(3);
    ls.display();
    ls.pop(v); cout << "pop: " << v << "\n";
    ls.peek(v); cout << "peek: " << v << "\n";
    ls.display();

    cout << "\n=== LinkedQueue ===\n";
    LinkedQueue lq;
    lq.enqueue(7); lq.enqueue(8); lq.enqueue(9);
    lq.display();
    lq.dequeue(v); cout << "dequeue: " << v << "\n";
    lq.peek(v);    cout << "peek: " << v << "\n";
    lq.dequeue(v); lq.dequeue(v);
    cout << "isEmpty: " << lq.isEmpty() << "\n";
    if (!lq.dequeue(v)) cout << "Underflow: queue is empty\n";
    return 0;
}

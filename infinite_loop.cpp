// infinite_loop.cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int*> memoryAllocations;

    int a = 0;
    while (true) {
        a = a + 1;
    }
    return 0;
}

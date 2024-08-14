// memory_hog.cpp
#include <iostream>
#include <vector>

int main() {
    try {
        std::vector<int> large_vector(256 * 1024 * 1024); // Allocates 1GB of memory
    } catch (const std::bad_alloc&) {
        std::cerr << "Memory allocation failed!" << std::endl;
        return 1;
    }
    return 0;
}

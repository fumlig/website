#include <iostream>

int main(int argc, char* argv[])
{
    std::ios_base::sync_with_stdio(false);

    const int n = 1000000;

    for(int i = 0; i < n; i++)
    {
        int d;
        std::cin >> d;
        std::cout << d;
    }

    return 0;
}

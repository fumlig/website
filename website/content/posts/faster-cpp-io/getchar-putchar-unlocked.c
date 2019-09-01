#include <stdio.h>
#include <stdbool.h>

#define N 1000000
#define MAX_DIGITS 7 // 7 digits in 1 000 000

#ifdef _WIN32
#define GETCHAR() _getchar_nolock()
#define PUTCHAR(c) _putchar_nolock(c)
#elif __unix__
#define GETCHAR() getchar_unlocked()
#define PUTCHAR(c) putchar_unlocked(c)
#else
#define GETCHAR() getchar()
#define PUTCHAR(c) putchar(c)
#endif

int scanint() 
{
    int n = 0;
    bool negative = false;
    char c = GETCHAR();

    if(c == '-') 
    {
        negative = true;
        c = GETCHAR();
    }

    do 
    {
        n = n * 10 + c - '0';
        c = GETCHAR();
    } 
    while(c >= '0' && c <= '9');

    if(negative)
        n = -n;
  
    return n;
}

void printint(int n)
{
    if(n == 0)
    {
        PUTCHAR('0');
        return;
    }

    if(n < 0)
    {
        PUTCHAR('-');
        n = -n;
    }

    char buffer[MAX_DIGITS];
    int i = MAX_DIGITS - 1;

    while(n)
    {
        buffer[i--] = n % 10 + '0';
        n /= 10;
    }

    while(i != MAX_DIGITS - 1) 
    {
        PUTCHAR(buffer[++i]);
    }
}

int main(int argc, char* argv[])
{
    for(int i = 0; i < N; i++)
    {
        int d = scanint();
        printint(d);
    }

    return 0;
}

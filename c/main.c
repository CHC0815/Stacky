#include <stdio.h>
#include <unistd.h>

char buf[34];

void print(int num)
{
    int last = 0;
    int i = 0;
    int buf_size;
    while (num > 0)
    {
        last = num % 10;
        buf[30 - i] = last + '0'; // 48 ^= 0, 49 ^= 1, ...
        i++;
        num /= 10;
    }
    buf[32] = '\n';
    buf[33] = '\0';
    write(1, &buf, buf_size);
}

int main()
{
    print(69420);
}
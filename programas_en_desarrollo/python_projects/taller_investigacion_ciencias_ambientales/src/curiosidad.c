#include <stdio.h>

int fun() { return 1; }
int fun_2() { return 2; }
int fun_3() { return 3; }

void A(int (*(ptr)[])(), int len)
{
    for (int i = 0; i < len; i++)
    {
        printf("%d\n", ptr[i]());
    }
}

int main()
{
    int (*(ptr)[])() = {fun, fun_2, fun_3};
    A(&ptr, 3);
    return 0;
}
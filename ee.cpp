#include <iostream>
using namespace std;

int bme(int a, int e, int m)
{
    int r = 1;
    a = a % m;
    while (e)
    {
        if (e & 1)
            r = r * a % m;
        a = a * a % m;
        e >>= 1;
    }
    return r;
}

int eea(int a, int b, int &x, int &y)
{
    if (b == 0)
    {
        x = 1;
        y = 0;
        return a;
    }
    int x1, y1;
    int g = eea(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}

int modinv(int a, int m)
{
    int x, y;
    int g = eea(a, m, x, y);
    if (g != 1)
        return -1;
    x = x % m;
    if (x < 0)
        x += m;
    return x;
}

int findG(int p)
{
    for (int g = 2; g < p; g++)
    {
        bool used[p] = {false};
        int value = 1;
        for (int i = 1; i < p; i++)
        {
            value = (value * g) % p;
            if (used[value])
                break;
            used[value] = true;
        }
        bool ok = true;
        for (int i = 1; i < p; i++)
        {
            if (!used[i])
            {
                ok = false;
                break;
            }
        }
        if (ok)
            return g;
    }
    return -1;
}

int main()
{
    int p = 23, x = 6, m = 10, k = 7;

    int g = findG(p);
    cout << "primitive root g = " << g << endl;

    int y = bme(g, x, p);
    cout << "public key = (" << p << ", " << g << ", " << y << ")" << endl;

    int c1 = bme(g, k, p);
    int c2 = (m * bme(y, k, p)) % p;

    cout << "encryption:" << endl;
    cout << "c1 = " << c1 << endl;
    cout << "c2 = " << c2 << endl;

    int s = bme(c1, x, p);
    int s_inv = modinv(s, p);
    int decrypted = (c2 * s_inv) % p;

    cout << "decryption:" << endl;
    cout << "s = " << s << endl;
    cout << "s^-1 = " << s_inv << endl;
    cout << "decrypted message = " << decrypted << endl;

    cout << "result: ";
    if (m == decrypted)
        cout << "message is same" << endl;
    else
        cout << "message is not same" << endl;

    return 0;
}
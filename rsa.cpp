#include <bits/stdc++.h>
#define int long long
using namespace std;

int bme(int a, int e, int m)
{
    int r = 1;
    a = a % m;
    while (e)
    {
        if (e & 1)
        {
            r = r * a % m;
        }
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
    {
        return -1;
    }
    x = x % m;
    if (x < 0)
    {
        x += m;
    }
    return x;
}

bool isPrime(int n)
{
    if (n < 2)
        return false;
    for (int i = 2; i * i <= n; i++)
    {
        if (n % i == 0)
            return false;
    }
    return true;
}

signed main()
{
    int p = 11, q = 13, m = 42;

    if (!isPrime(p) || !isPrime(q))
    {
        cout << "p and q must be prime." << endl;
        return 0;
    }

    int n = p * q;
    int phi = (p - 1) * (q - 1);

    cout << "n = " << n << endl;
    cout << "phi = " << phi << endl;

    int e;
    for (int i = 2; i < phi; i++)
    {
        int x, y;
        if (eea(i, phi, x, y) == 1)
        {
            e = i;
            break;
        }
    }

    cout << "public exponent e = " << e << endl;

    int d = modinv(e, phi);
    if (d == -1)
    {
        cout << "no modular inverse exists." << endl;
        return 0;
    }

    cout << "private exponent d = " << d << endl;

    if (m >= n || m < 0)
    {
        cout << "message must satisfy 0 <= m < n." << endl;
        return 0;
    }

    int signature = bme(m, d, n);
    cout << "signature = " << signature << endl;

    int verifiedMessage = bme(signature, e, n);
    cout << "verified message = " << verifiedMessage << endl;

    if (m == verifiedMessage)
    {
        cout << "valid signature" << endl;
    }
    else
    {
        cout << "invalid signature" << endl;
    }

    return 0;
}
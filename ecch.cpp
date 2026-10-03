#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

struct Point
{
    ll x, y;
    bool infinity;
};

ll mod(ll a, ll m)
{
    a %= m;
    if (a < 0)
        a += m;
    return a;
}

ll egcd(ll a, ll b, ll &x, ll &y)
{
    if (b == 0)
    {
        x = 1;
        y = 0;
        return a;
    }
    ll x1, y1;
    ll g = egcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}

ll modinv(ll e, ll phi)
{
    ll x, y;
    ll g = egcd(e, phi, x, y);
    if (g != 1)
        return -1;
    return mod(x, phi);
}

bool isPointOnCurve(Point P, ll a, ll b, ll p)
{
    if (P.infinity)
        return true;
    ll left = mod(P.y * P.y, p);
    ll right = mod(P.x * P.x * P.x + a * P.x + b, p);
    return left == right;
}

Point add(Point P, Point Q, ll a, ll p)
{
    if (P.infinity)
        return Q;
    if (Q.infinity)
        return P;
    if (P.x == Q.x && mod(P.y + Q.y, p) == 0)
        return {0, 0, true};

    ll lambda;
    if (P.x == Q.x && P.y == Q.y)
    {
        if (P.y == 0)
            return {0, 0, true};
        ll numerator = mod(3 * P.x * P.x + a, p);
        ll denominator = mod(2 * P.y, p);
        lambda = mod(numerator * modinv(denominator, p), p);
    }
    else
    {
        ll numerator = mod(Q.y - P.y, p);
        ll denominator = mod(Q.x - P.x, p);
        lambda = mod(numerator * modinv(denominator, p), p);
    }

    ll x3 = mod(lambda * lambda - P.x - Q.x, p);
    ll y3 = mod(lambda * (P.x - x3) - P.y, p);
    return {x3, y3, false};
}

Point Negate(Point P, ll p)
{
    if (P.infinity)
        return P;
    return {P.x, mod(-P.y, p), false};
}

Point multiply(ll k, Point P, ll a, ll p)
{
    Point result = {0, 0, true};
    while (k > 0)
    {
        if (k & 1)
            result = add(result, P, a, p);
        P = add(P, P, a, p);
        k >>= 1;
    }
    return result;
}

int main()
{
    ll a = 2, b = 2, p = 17;

    Point G;
    bool found = false;
    for (ll x = 0; x < p && !found; x++)
    {
        for (ll y = 0; y < p; y++)
        {
            Point temp = {x, y, false};
            if (isPointOnCurve(temp, a, b, p))
            {
                G = temp;
                found = true;
                break;
            }
        }
    }

    if (!found)
    {
        cout << "no point found" << endl;
        return 0;
    }

    ll d = 7;
    Point Q = multiply(d, G, a, p);

    ll x1 = 3, y1 = 1, x2 = 3, y2 = 1;
    Point M1 = {x1, y1, false};
    Point M2 = {x2, y2, false};

    if (!isPointOnCurve(M1, a, b, p) ||
        !isPointOnCurve(M2, a, b, p))
    {
        cout << "invalid message point" << endl;
        return 0;
    }

    ll k1 = 5, k2 = 5;

    Point C11 = multiply(k1, G, a, p);
    Point C12 = add(M1, multiply(k1, Q, a, p), a, p);
    Point C21 = multiply(k2, G, a, p);
    Point C22 = add(M2, multiply(k2, Q, a, p), a, p);

    Point C1 = add(C11, C21, a, p);
    Point C2 = add(C12, C22, a, p);

    Point dC1 = multiply(d, C1, a, p);
    Point decryptedSum = add(C2, Negate(dC1, p), a, p);

    if (decryptedSum.infinity)
        cout << "decrypted message = o" << endl;
    else
        cout << "decrypted message = "
             << decryptedSum.x << " " << decryptedSum.y << endl;

    return 0;
}
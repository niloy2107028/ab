#include <iostream>
#include <string>
using namespace std;

string encrypt(string text, int s)
{
    string result = "";
    for (char ch : text)
    {
        if (isupper(ch))
            result += char((ch - 'A' + s) % 26 + 'A');
        else if (islower(ch))
            result += char((ch - 'a' + s) % 26 + 'a');
        else
            result += ch;
    }
    return result;
}

string decrypt(string text, int s) { return encrypt(text, 26 - (s % 26)); }

int main()
{
    string text = "Hello World";
    int s = 3;

    cout << "encrypted: ";
    string enc = encrypt(text, s);
    cout << enc << endl;
    cout << "decrypted: " << decrypt(enc, s) << endl;
}
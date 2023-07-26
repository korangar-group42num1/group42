#include <iostream>
#include<string>
#include <openssl/evp.h>
#include<time.h>
#include<random>
#include<algorithm>

using namespace std;

#define N 19746783//2^32*1.177
string data_list[N];
string hash_list[N];
string sm3_hash(const string& message) {
    EVP_MD_CTX* ctx = EVP_MD_CTX_new();
    EVP_MD_CTX_init(ctx);

    if (EVP_DigestInit_ex(ctx, EVP_sm3(), nullptr) != 1) {
        cerr << "Error initializing SM3 digest" <<endl;
        EVP_MD_CTX_free(ctx);
        return "";
    }

    if (EVP_DigestUpdate(ctx, message.c_str(), message.length()) != 1) {
        cerr << "Error updating SM3 digest" << endl;
        EVP_MD_CTX_free(ctx);
        return "";
    }

    unsigned char hash[EVP_MAX_MD_SIZE];
    unsigned int hash_len;

    if (EVP_DigestFinal_ex(ctx, hash, &hash_len) != 1) {
        std::cerr << "Error finalizing SM3 digest" << std::endl;
        EVP_MD_CTX_free(ctx);
        return "";
    }

    EVP_MD_CTX_free(ctx);

    string result;
    for (unsigned int i = 0; i < hash_len; i++) {
        char hex[3];
        sprintf(hex, "%02x", hash[i]);
        result += hex;
    }

    return result;
}

string uniqueName(int length) {
    auto randchar = []() -> char
    {
        const char charset[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
        const size_t max_index = (sizeof(charset) - 1);
        return charset[rand() % max_index];
    };
    std::string str(length, 0);
    std::generate_n(str.begin(), length, randchar);
    return str;
}


int collision(int bit) {
    unsigned long long all = unsigned long long(1.177 * pow(2, bit / 2));
    unsigned long long i = 0;
    while(i<all) {
        string rand_i = uniqueName(50);
        string hash_i = sm3_hash(rand_i);
        data_list[i] = rand_i;
        hash_list[i] = hash_i;
        i++;
    }
    for (unsigned long long i=0; i < all; i++) {
        string data_i = data_list[i];
        string hash_i = hash_list[i];
        for (unsigned long long j = i + 1; j < all; j++) {
            string data_j = data_list[j];
            string hash_j = hash_list[j];
            for (int k = 0; k < bit / 4; k++) {
                if (hash_i[k] != hash_j[k]) {
                    break;
                }
                if (k == bit/4 - 1) {
                    cout << bit << " bits collision: " << endl;
                    cout<< data_i << " and " << data_j << endl;
                    cout << data_i << " SM3 Hash: " << hash_i << endl;
                    cout << data_j << " SM3 Hash: " << hash_j << endl;
                    cout << "collision : ";
                    for (int p = 0; p < bit / 4; p++) {
                        cout << hash_j[p];
                    }
                    cout << endl;
                    return 1;
                }
            }
        }

    }
    cout << bit<<" bits not found;" << endl;
    return 0;
}
int main() {
    srand(clock());
    clock_t start, end;
    double time_all=0;
    double count = 0;
    double count_success=0;
    int set = 0;
    //test-rate 
    //4-16 bits
    cout << sm3_hash("ABCDabcd");
    system("pause");
    for (int i = 0; i < 10; i++) {
        cout << "---------------------------- "<< i<< " ----------------------------" << endl;
        int j = 4;
        for (j; j <= 16; j += 4) {
            count++;
            start = clock();
            int sign = collision(j);
            end = clock();
            if (sign == 1) {
                count_success++;
            }
            time_all += ((double)(end - start)) / CLOCKS_PER_SEC;
            cout << "time:" << ((double)(end - start)) / CLOCKS_PER_SEC << " s" << endl << endl;
        }
        j = 4;
        set = i+1;
    }
    cout << "time of testing rate: " << time_all<<" s" << endl;
    cout << "the rate of the birthday attack of reduced SM3 ( "<<set<<" sets ): "<<100*count_success/count<< " %" << endl<<endl;

    //large bits collision
    cout << "---------------------------- large bits collision ----------------------------" << endl;
    int i = 20;
    time_all = 0;
    start = clock();
    while (i <= 32) {
        if (collision(i) == 1) {
            end = clock();
            time_all += ((double)(end - start)) / CLOCKS_PER_SEC;
            i += 4;
            cout << "time:" << ((double)(end - start)) / CLOCKS_PER_SEC << " s" << endl << endl;
            cout << endl;
        }
    }
    cout << "time of finding large bits collision:" << ((double)(end - start)) / CLOCKS_PER_SEC << " s" << endl << endl;
    return 0;
}
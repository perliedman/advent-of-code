/* gcc day14.c -o day14 -lcrypto */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#if defined(__APPLE__)
#  define COMMON_DIGEST_FOR_OPENSSL
#  include <CommonCrypto/CommonDigest.h>
#  define SHA1 CC_SHA1
#else
#  include <openssl/md5.h>
#endif

void digest2hex(unsigned char *digest, char *out) {
    for (int n = 0; n < 16; ++n) {
        snprintf(&(out[n*2]), 16*2, "%02x", (unsigned int)digest[n]);
    }
}

int findPattern(unsigned char *d, int length, int patLen, int print) {
    unsigned char nibble, last;
    int matchStart;
    int matchCount;

    for (int n = 0; n < length * 2; ++n) {
        nibble = d[n / 2] >> (n % 2 ? 0 : 4) & 0xF;
        if (print) printf("%d %01x\n", n, nibble);
        if (n && nibble == last) {
            matchCount++;
            if (matchCount == patLen) {
                return 1;
            }
        } else {
            if (matchCount > 1) {
                n = matchStart + 1;
                nibble = d[n / 2] >> (n % 2 ? 4 : 0);                
            }
            last = nibble;
            matchStart = n;
            matchCount = 1;
        }
    }

    return 0;
}

int main(int argc, char** argv) {
    int i = 0;
    int c = 0;
    char passwd[9];
    char k[256];
    MD5_CTX ctx;
    unsigned char digest[16];
    char buffer[33];

    while (c < 64) {
        int length = snprintf(k, 256, "%s%d", argv[1], i);

        MD5_Init(&ctx);
        MD5_Update(&ctx, k, length);
        MD5_Final(digest, &ctx);

        if (findPattern(digest, 16, 3, 0)) {
            for (int j = i + 1; j < i + 1000; j++) {
                length = snprintf(k, 256, "%s%d", argv[1], j);

                MD5_Init(&ctx);
                MD5_Update(&ctx, k, length);
                MD5_Final(digest, &ctx);

                if (findPattern(digest, 16, 5, 0)) {
                    printf("---------------\n");
                    digest2hex(digest, buffer);
                    printf("%d; %d: %s\n", i, j, buffer);
                    findPattern(digest, 16, 5, 1);

                    c++;
                    printf("%d: %d\n", c, i);
                    break;
                }
            }
        }

        i++;
    }

    printf("%d\n", i - 1);

    return 0;
}

// int main(int argc, char** argv) {
//     int i = 0;
//     int c = 0;
//     char passwd[9];
//     char k[256];
//     MD5_CTX ctx;
//     unsigned char digest[16];
//     char buffer[33];

//     int length = snprintf(k, 256, "abc200");

//     MD5_Init(&ctx);
//     MD5_Update(&ctx, k, length);
//     MD5_Final(digest, &ctx);

//     printf("%d\n", findPattern(digest, 16, 5));

//     return 0;
// }

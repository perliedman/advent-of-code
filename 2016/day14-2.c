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

int findPattern(unsigned char *d, int length, int patLen, int print, unsigned char *found) {
    unsigned char nibble, last;
    int matchStart = 0;
    int matchCount = 0;

    for (int n = 0; n < length * 2; ++n) {
        nibble = d[n / 2] >> (n % 2 ? 0 : 4) & 0xF;
        if (print) printf("%d %01x\n", n, nibble);
        if (n && nibble == last) {
            matchCount++;
            if (matchCount == patLen) {
                *found = last;
                return 1;
            }
        } else {
            if (matchCount > 1) {
                n = matchStart + 1;
                nibble = d[n / 2] >> (n % 2 ? 0 : 4);
            }
            last = nibble;
            matchStart = n;
            matchCount = 1;
        }
    }

    return 0;
}

int findFixedPattern(unsigned char *d, int length, int p, int patLen, int print) {
    unsigned char nibble;
    int matchCount = 0;

    for (int n = 0; n < length * 2; ++n) {
        nibble = d[n / 2] >> (n % 2 ? 0 : 4) & 0xF;
        if (print) printf("%d %01x\n", n, nibble);
        if (nibble == p) {
            matchCount++;
            if (matchCount == patLen) {
                return 1;
            }
        } else {
            matchCount = 0;
        }
    }

    return 0;
}

void hash(char *k, int length, unsigned char *digest, int rounds) {
    MD5_CTX ctx;
    char buffer[33];

    MD5_Init(&ctx);
    MD5_Update(&ctx, k, length);
    MD5_Final(digest, &ctx);
    digest2hex(digest, buffer);

    for (int i = 0; i < rounds; i++) {
        MD5_Init(&ctx);
        MD5_Update(&ctx, buffer, 32);
        MD5_Final(digest, &ctx);
        digest2hex(digest, buffer);
    }
}

int main(int argc, char** argv) {
    int i = 0;
    int c = 0;
    char k[256];
    MD5_CTX ctx;
    unsigned char *digest;
    char buffer[33];
    char buffer2[33];
    unsigned char pattern;

    unsigned char digests[1000*16];
    int maxHash = 0;

    while (c < 64) {
        int length = snprintf(k, 256, "%s%d", argv[1], i);

        digest = digests + (i % 1000) * 16;
        if (i >= maxHash) {
            hash(k, length, digest, 2016);
            maxHash = i;
        }

        if (findPattern(digest, 16, 3, 0, &pattern)) {
            digest2hex(digest, buffer);
            //printf("%d: %s\n", i, buffer);
            for (int j = i + 1; j < i + 1000; j++) {
                length = snprintf(k, 256, "%s%d", argv[1], j);

                digest = digests + (j % 1000) * 16;
                if (j >= maxHash) {
                    hash(k, length, digest, 2016);
                    maxHash = j;
                }

                if (findFixedPattern(digest, 16, pattern, 5, 0)) {
                    digest2hex(digest, buffer2);
                    //printf("%s; %d (%s); %d (%01x): %s\n", k, i, buffer, j, pattern, buffer2);
                    printf("%s %s\n", buffer, buffer2);
                    c++;
                    //printf("%d: %d\n", c, i);
                    break;
                }
                // if (j % 10 == 0) {
                //     printf("\t%d\n", j);
                // }
            }
            //printf("%d: failed match\n", i);
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

//     int length = snprintf(k, 256, "abc0");

//     hash(k, length, digest, 2016);
//     digest2hex(digest, buffer);

//     printf("%s\n", buffer);

//     return 0;
// }


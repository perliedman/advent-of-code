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

int main(int argc, char** argv) {
    int i = 0;
    int c = 0;
    char passwd[9];
    char k[256];
    MD5_CTX ctx;
    unsigned char digest[16];
    char buffer[33];

    while (c < 8) {
        int length = snprintf(k, 256, "%s%d", argv[1], i);

        MD5_Init(&ctx);
        MD5_Update(&ctx, k, length);
        MD5_Final(digest, &ctx);

        unsigned long l = *((unsigned long*)digest) & 0xF0FFFF;
        if (l == 0) {
            digest2hex(digest, buffer);
            printf("%d: %s => %s (%lx)\n", i, k, buffer, *((unsigned long*)digest));

            char b[2];
            sprintf(b, "%lx", (*((unsigned long*)digest) & 0xF0000) >> 16);
            passwd[c++] = b[0];
        }

        i++;
    }

    passwd[8] = 0;
    printf("%s\n", passwd);

    return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "dic_internals.h"

uint32_t bswap32(uint32_t x)
{
    return ((x << 24) & 0xff000000 ) |
        ((x <<  8) & 0x00ff0000 ) |
        ((x >>  8) & 0x0000ff00 ) |
        ((x >> 24) & 0x000000ff );
}

uint32_t bswap32p(uint32_t x)
{
    return ((x << 16) & 0xff000000 ) |
        ((x >> 16) & 0x0000ff00 ) |
        (x  & 0x00ff00ff );
}

uint32_t reverse(uint32_t x)
{
    x = ((x >> 1) & 0x55555555u) | ((x & 0x55555555u) << 1);
    x = ((x >> 2) & 0x33333333u) | ((x & 0x33333333u) << 2);
    x = ((x >> 4) & 0x0f0f0f0fu) | ((x & 0x0f0f0f0fu) << 4);
    x = ((x >> 8) & 0x00ff00ffu) | ((x & 0x00ff00ffu) << 8);
    x = ((x >> 16) & 0xffffu) | ((x & 0xffffu) << 16);
    return x;
}

unsigned char reverse_b(unsigned char b) {
    char rev = 0;
    int i = 0;
    rev |= ((b>>i) & 1)<<(7-i);
    i = 1;
    rev |= ((b>>i) & 1)<<(7-i);
    i = 2;
    rev |= ((b>>i) & 1)<<(7-i);
    rev |= b >> 3 & 0b00011111;
    return rev;
}

int main(int argc, char* argv[]) {
    FILE *f = fopen(argv[1], "rb");
    fseek(f, 0, SEEK_END);
    long fsize = ftell(f);
    printf("Size: %ld\n", fsize);
    rewind(f);

    char *buff = malloc(fsize);
    if (fread(buff, fsize, 1, f) != 1) {
        puts("Error");
        fclose(f);
        return 1;
    }

    fclose(f);

    uint32_t* p = (uint32_t*)buff;
    for (uint32_t i=0; i < 8; i++) {
        p[i] = bswap32(p[i]);
    }
    for (uint32_t i=8; i < fsize / 4; i++) {
		char* pc = (char*)(p+i);
        char temp = pc[0];
        pc[0] = pc[2];
        pc[2] = temp;
		pc[3] = reverse_b(pc[3]);
    }

    strncpy(buff, _COMPIL_KEYWORD_, sizeof( _COMPIL_KEYWORD_));

    FILE *g = fopen(argv[2], "wb");
    fwrite(buff, fsize, 1, g);
    fclose(g);
    puts("OK");

    return 0;
}

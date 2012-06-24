#include "lyricseek.h"

int main() {
	char *lyr = lyricseek_get("rammstein","", "Du Hast","lyrics", -1);
	if(lyr == NULL) {
		printf("Errori\n");
		return 1;
	}
	printf("%s\n", lyr);
	return 0;
}


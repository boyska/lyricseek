#include "lyricseek.h"

int main() {
	Py_Initialize();
/*    char *lyr = get_lyrics(get_data("senza sicura",NULL, "figli della patria","lyrics", 180));*/
	char *lyr = get_lyrics(get_data("rammstein",NULL, "Du Hast","lyrics", -1));
	if(lyr == NULL) {
		printf("Errori!\n");
		return 1;
	}
	printf("\n\n\n%s\n", lyr);
	Py_Finalize();
	return 0;
}


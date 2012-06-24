#include <Python.h>

#ifdef DEBUGGING
#include <stdio.h>
#define DEBUG(format, ...) fprintf(stderr, "%s[%s]:%d: ", basename(__FILE__), __FUNCTION__, __LINE__); fprintf(stderr, format, ## __VA_ARGS__); fputs("\n", stderr); fflush(stderr);
#else
#define DEBUG(format,...)
#endif


/* API */
char *lyricseek_get(char *artist, char* album, char* title, 
        char* request, int timeout);

/* internal functions */
static PyObject *get_data(char *artist, char* album, char* title, 
        char* request, int timeout);
static char *get_lyrics(PyObject* dict);


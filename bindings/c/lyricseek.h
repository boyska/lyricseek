#include <Python.h>

PyObject *get_data(char *artist, char* album, char* title, 
        char* request, int timeout);
char *get_lyrics(PyObject* dict);


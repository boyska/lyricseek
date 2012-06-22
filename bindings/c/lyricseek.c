#include "lyricseek.h"

static PyObject *get_module()
{
	PyObject* lyricseek;
	lyricseek = PyImport_ImportModule("lyricseek");
}
PyObject *get_data(char *artist, char* album, char* title, 
        char* request, int timeout)
{
	//(partially) wraps lyricseek.get()
	PyObject *request_tuple, *args;
	PyObject *lyricseek, *get;
	PyObject *data;

	request_tuple = Py_BuildValue("(s)", request);
	lyricseek = get_module();
	get = PyObject_GetAttr(lyricseek, Py_BuildValue("s", "get"));

	args = Py_BuildValue("(sss()(s)i)", artist, album, title, request, timeout);
	PyObject_Print(args, stdout, 0);
	data = PyObject_CallObject(get, args);
	if(data == NULL) {
		printf("Error: get() returned null\n");
		exit(1);
	}
	return data;
}

char *get_lyrics(PyObject* dict) {
	//extract the "lyrics" from the result dict and convert it to char*
	//returns NULL in case of error
	PyObject *lyrics;
	char *lyrics_string, *errors;
	int len;

	lyrics = PyDict_GetItemString(dict, "lyrics");
	if(lyrics == NULL) //not found
		return NULL;
	PyObject_Print(lyrics, stdout, 0);
	lyrics_string = PyString_AsString(lyrics);
	return lyrics_string;
}


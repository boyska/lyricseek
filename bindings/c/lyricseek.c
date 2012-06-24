#include "lyricseek.h"

static PyObject *get_module()
{
	PyObject* lyricseek;
	lyricseek = PyImport_ImportModule("lyricseek");
	return lyricseek;
}

/*
	(partially) wraps lyricseek.get()
	returns NULL on error
*/
static PyObject *get_data(char *artist, char* album, char* title, 
        char* request, int timeout)
{
	PyObject *request_tuple, *args;
	PyObject *lyricseek, *get;
	PyObject *data;

	request_tuple = Py_BuildValue("(s)", request);
	lyricseek = get_module();
	if(lyricseek == NULL) {
		return NULL;
	}
	get = PyObject_GetAttrString(lyricseek, "get");

	args = Py_BuildValue("(sss()(s)i)", artist, album, title, request, timeout);
	data = PyObject_CallObject(get, args);
	return data;
}

static char *get_lyrics(PyObject* dict) {
	//extract the "lyrics" from the result dict and convert it to char*
	//returns NULL in case of error
	PyObject *lyrics;
	char *lyrics_string, *errors;
	int len;

	lyrics = PyDict_GetItemString(dict, "lyrics");
	if(lyrics == NULL) //not found
		return NULL;
	lyrics_string = PyString_AsString(lyrics);
	return lyrics_string;
}

/* 
   Ready-to-use solution to use lyricseek in your C program
*/
char *lyricseek_get(char *artist, char* album, char* title, 
        char* request, int timeout)
{
	Py_Initialize();
	char *lyr = get_lyrics(get_data(artist, album, title, request, timeout));
	Py_Finalize();
	return lyr;
}



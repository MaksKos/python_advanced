#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <Python.h>

static PyObject *method_loads(PyObject *self, PyObject *args);
static PyObject *method_dumps(PyObject *self, PyObject *args);
// for dumps
int _check_dict(PyObject *dict, size_t *lenght);
int _make_string(PyObject *dict, char *json);
// for loads
int _parser(const char *string, PyObject *dict);
size_t _miss_whitespace(const char *string, size_t i);
size_t _get_key(const char *string, PyObject **key, size_t i);
size_t _get_value (const char *string, PyObject **value, size_t i);
size_t _get_str_len(const char *string, size_t i);
PyObject *_get_py_str(const char *string, size_t start, size_t end);
PyObject * _get_py_num(const char *string, size_t *i);

static PyMethodDef JsonMethods[] = {
    {"loads", method_loads, METH_VARARGS, "cjson load method: str"},
    {"dumps", method_dumps, METH_VARARGS, "cjson dump method: dict"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "cjson",
    "json C library",
    -1,
    JsonMethods
};

PyMODINIT_FUNC PyInit_cjson(void) {
    return PyModule_Create(&module);
};

static PyObject *method_loads(PyObject *self, PyObject *args) {
    
    const char *json_str = NULL;
    PyObject *dict = NULL;
    size_t str_len = 0;

    if(!PyArg_ParseTuple(args, "s", &json_str)) {
        PyErr_Format(PyExc_TypeError, "Expected object is not string");
        return NULL;
    }
    str_len = strlen(json_str);
    if (str_len < 2) {
        PyErr_Format(PyExc_TypeError, "Expected object is empty");
        return NULL;
    }
    if (json_str[0] != '{'  || json_str[str_len-1] != '}') {
        PyErr_Format(PyExc_TypeError, "Expected object isn't JSON");
        return NULL;
    }

    if (!(dict = PyDict_New())) {
        printf("ERROR: Failed to create Dict Object\n");
        return NULL;
    }

    if(!_parser(json_str, dict)){
        printf("ERROR: Failed to parsing\n");
        return NULL;
    }
    return dict;
};

static PyObject *method_dumps(PyObject *self, PyObject *args) {
    
    PyObject *json_dict = NULL;
    PyObject *dump = NULL;
    char *json_str = NULL;
    size_t lenght = 0;
    size_t dict_size = 0;

    if(!PyArg_ParseTuple(args, "O!", &PyDict_Type, &json_dict)){
        PyErr_Format(PyExc_TypeError, "Expected object is not dict type");
        return NULL;
    }
    if (json_dict == NULL)
    {
        printf("ERROR: Failed to create Dict Object\n");
        return NULL;
    }

    if(!_check_dict(json_dict, &lenght))
        return NULL;

    if(lenght == 0){
        return Py_BuildValue("s", "{}");
    }
    // allocate memory for key, value and symbols: 
    // ", "; ": "; "{"; "}"
    dict_size = PyDict_Size(json_dict);
    lenght += 4*dict_size;
    json_str = (char *)calloc(sizeof(char), lenght);

    if(!_make_string(json_dict, json_str)){
        printf("ERROR: Failed to create JSON\n");
        free(json_str);
        return NULL;
    }
    dump = Py_BuildValue("s", json_str);
    free(json_str);
    return dump;
};

int _check_dict(PyObject *dict, size_t *lenght){

    PyObject *key, *value;
    Py_ssize_t pos = 0;
    size_t len = 0;

    while (PyDict_Next(dict, &pos, &key, &value)) {

        if (!PyObject_IsInstance(key, &PyUnicode_Type)) {
            PyErr_Format(PyExc_TypeError, "dict's key isn't string");
            return 0;
        }
        if(
            !(PyObject_IsInstance(value, &PyUnicode_Type) ||
            PyObject_IsInstance(value, &PyFloat_Type) ||
            PyObject_IsInstance(value, &PyLong_Type))
            ) {
            PyErr_Format(PyExc_TypeError, "dict's val isn't <str>, <int> or <float>");
            return 0;
        }     
        len += strlen(PyUnicode_AsUTF8(PyObject_Repr(key)));
        len += strlen(PyUnicode_AsUTF8(PyObject_Repr(value)));

    }
    *lenght = len;
    return 1;
}

int _make_string(PyObject *dict, char *json){

    PyObject *key, *value;
    Py_ssize_t pos = 0;
    const char *key_str, *value_str;
    
    if (json == NULL || dict == NULL)
        return 0;
    
    strcat(json, "{");

    while (PyDict_Next(dict, &pos, &key, &value)) {

        key_str = PyUnicode_AsUTF8(key);
        value_str = PyUnicode_AsUTF8(PyObject_Repr(value));
        
        if (pos > 1)
            strcat(json, ", ");
        strcat(json, "\"");
        strcat(json, key_str);
        strcat(json, "\"");
        strcat(json, ": ");
        strcat(json, value_str);

    }
    strcat(json, "}");
    return 1;
}

int _parser(const char *string, PyObject *dict) {

    PyObject *key = NULL;
    PyObject *value = NULL;

    for (size_t i = 0; i < strlen(string);) {
        // delete whitespaces
        i = _miss_whitespace(string, i);
        // check separator
        if (string[i] == '}')
            break;
        if (string[i] == '{' || string[i] == ',') {

            // try to get key
            i = _get_key(string, &key, i+1);
            if (i == -1) {
                printf("ERROR: incorrect key\n");
                return 0;
            }
            i = _miss_whitespace(string, i);
            // try to get value
            if (string[i] == ':') {
            i = _get_value(string, &value, i+1);
                if (i == -1) {
                    printf("ERROR: incorrect value\n");
                    return 0;
                }
            }
            else {
                printf("ERROR: not JSON format (no value)\n");
                return 0;
            }
        }
        else {
            printf("ERROR: not JSON format (no key)\n");
            return 0;
        }
        // set item
        if (PyDict_SetItem(dict, key, value) < 0) {
            printf("ERROR: Failed to set item\n");
            return 0;
        }

    }
    return 1;
}

size_t _miss_whitespace(const char *string, size_t i) {
    
    while (isspace(string[i]))
        i++;
    return i;
}

size_t _get_key(const char *string, PyObject **key, size_t i) {

    size_t key_len, index;
    char *key_str;

    i = _miss_whitespace(string, i);
    if (string[i] != '"')
        return -1;
    i++; index = i; 

    i = _get_str_len(string,  i);
    if (i == -1)
        return -1;
    
    *key = _get_py_str(string, index, i);
    if (*key == NULL)
        return -1;
    return i;
}

size_t _get_value (const char *string, PyObject **value, size_t i) {
    
    size_t index;
    char *value_str;

    i = _miss_whitespace(string, i);
    if (string[i] == '"'){
        i++; index = i;

        i = _get_str_len(string,  i);
        if (i == -1)
            return -1;
    
        *value = _get_py_str(string, index, i);
        if (*value == NULL)
            return -1;
        return i;
    }
    if (isdigit(string[i])){
        *value = _get_py_num(string, &i);
        if (*value == NULL)
            return -1;
        return ++i;
    }

    return -1;
}

size_t _get_str_len(const char *string, size_t i){

    size_t len;

    while (i < strlen(string)) {

        len = strcspn(&string[i], "\"");

        if (len == strlen(&string[i])){
            printf("ERROR: Failed to get string\n");
            return -1;
        }
        if (string[i+len-1] != '\\'){
            i += len+1;
            break;
        }
        i += len+1;

    }
    return i;
}

PyObject *_get_py_str(const char *string, size_t start, size_t end){

    char *new_str;
    PyObject *py_str;

    new_str = (char *)calloc(sizeof(char), end-start-1);
    strncpy(new_str, &string[start], end-start-1);
    printf("Value: %s \n", new_str);

    // Build python string
    if (!(py_str = Py_BuildValue("s", new_str))) {
        printf("ERROR: Failed to build string value\n");
        return NULL;
    }      
    free(new_str);
    return py_str;
}

PyObject * _get_py_num(const char *string, size_t *i) {

    char *counter = NULL;
    double val_1;
    long int val_2;
    PyObject *value;

    val_1 = strtod(&string[*i], &counter);
    if (counter != NULL){
        //make float obj
    }

    val_2 = strtol(&string[*i], &counter, 10);
    if (counter == NULL){
        printf("ERROR: Failed to get number\n");
        return NULL;
    }

    if (!(value = Py_BuildValue("i", 10))) {
        printf("ERROR: Failed to build integer value\n");
        return NULL;
    }
    *i = 0;
    return value;
}
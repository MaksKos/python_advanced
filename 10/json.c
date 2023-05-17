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
int _parser(char *string, PyObject *dict);
char *_miss_whitespace(char *cursor);
char *_get_key(char **cursor, PyObject **key);
char *_get_value(char **cursor, PyObject **value);
int _get_str_len(char *cursor, size_t *lenght);
PyObject *_get_py_str(char **cursor, size_t len);
PyObject * _get_py_num(char **cursor);

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
    
    char *json_str = NULL;
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

    if(!_parser(json_str, dict)) {
        PyErr_Format(PyExc_TypeError, "Expected object isn't JSON");
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

        if (!PyUnicode_Check(key)) {
            PyErr_Format(PyExc_TypeError, "dict's key isn't string");
            return 0;
        }
        if(!(PyUnicode_Check(value) ||
            PyFloat_Check(value) ||
            PyLong_Check(value))
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
        if(PyUnicode_Check(value))
            value_str = PyUnicode_AsUTF8(value);
        else
            value_str = PyUnicode_AsUTF8(PyObject_Repr(value));
        
        if (pos > 1)
            strcat(json, ", ");
        strcat(json, "\"");
        strcat(json, key_str);
        strcat(json, "\"");
        strcat(json, ": ");
        if(PyUnicode_Check(value)){
            strcat(json, "\"");
            strcat(json, value_str);
            strcat(json, "\"");
        }
        else
            strcat(json, value_str);

    }
    strcat(json, "}");
    return 1;
}

int _parser(char *string, PyObject *dict) {

    PyObject *key = NULL;
    PyObject *value = NULL;
    char *cursor = string;

    while (cursor != string + strlen(string)) {
        // delete whitespaces
        cursor = _miss_whitespace(cursor);
        // check separator
        if (*cursor == '}')
            break;
        if (*cursor == '{' || *cursor == ',') {
            cursor++;
            // if empty JSON
            cursor = _miss_whitespace(cursor);
            if (*cursor == '}')
                break;
            // try to get key;
            if (_get_key(&cursor, &key) == NULL) {
                printf("ERROR: incorrect key\n");
                return 0;
            }
            cursor = _miss_whitespace(cursor);
            // try to get value
            if (*cursor == ':') {
                cursor++;
                if (_get_value(&cursor, &value) == NULL) {
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

char* _miss_whitespace(char *cursor) {  
    while (isspace(*cursor))
        cursor++;
    return cursor;
}

char* _get_key(char **cursor, PyObject **key) {

    size_t len;
    
    *cursor = _miss_whitespace(*cursor);
    if (**cursor != '"')
        return NULL;
    (*cursor)++;
    if (!_get_str_len(*cursor, &len))
        return NULL;
    *key = _get_py_str(cursor, len);
    if (*key == NULL)
        return NULL;
    (*cursor) += len+1;
    return *cursor;
}

char* _get_value (char **cursor, PyObject **value) {
    
    size_t len;

    *cursor = _miss_whitespace(*cursor);
    if (**cursor == '"'){
        (*cursor)++;
        if (!_get_str_len(*cursor, &len))
            return NULL;
        *value = _get_py_str(cursor, len);
        if (*value == NULL)
            return NULL;
        (*cursor) += len+1;
        return *cursor;
    }
    if (isdigit(**cursor)){
        *value = _get_py_num(cursor);
        if (*value == NULL)
            return NULL;
        return *cursor;
    }

    return NULL;
}

int _get_str_len(char *cursor, size_t *lenght){

    size_t len = 0, sum = 0;
    char *start = cursor;

    while (len  < strlen(cursor)) {
        
        len = strcspn(start, "\"");

        if (len == strlen(start)){
            printf("ERROR: Failed to get string\n");
            return 0;
        }
        if (start[len-1] != '\\'){
            sum += len;
            break;
        }
        len++;
        sum += len;
        start += len;
    }
    *lenght = sum;
    return 1;
}

PyObject *_get_py_str(char **cursor, size_t len){

    char *new_str;
    PyObject *py_str;

    new_str = (char *)calloc(sizeof(char), len);
    strncpy(new_str, *cursor, len);
    //printf("Value: %s \n", new_str);

    // Build python string
    if (!(py_str = Py_BuildValue("s", new_str))) {
        printf("ERROR: Failed to build string value\n");
        return NULL;
    }      
    free(new_str);
    return py_str;
}

PyObject * _get_py_num(char **cursor) {

    char *counter = NULL;
    double val_float;
    long int val_int;
    PyObject *value;

    val_int = strtol(*cursor, &counter, 0);
    if (counter == NULL){
        printf("ERROR: Failed to get number (int)\n");
        return NULL;
    }
    if (*counter != '.')
    {      
        if (!(value = Py_BuildValue("i", val_int))) {
            printf("ERROR: Failed to build integer value\n");
            return NULL;
        }

        *cursor = counter;
        return value;
    }
    
    val_float = strtod(*cursor, &counter);
    if (counter == NULL){
        printf("ERROR: Failed to get number (float)\n");
        return NULL;
    }
    if (*counter != '.')
    {      
        if (!(value = Py_BuildValue("d", val_float))) {
            printf("ERROR: Failed to build float value\n");
            return NULL;
        }
        *cursor = counter;
        return value;
    }
    printf("ERROR: no number");
    return NULL;
}

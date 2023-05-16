#include <stdio.h>
#include <string.h>
#include <Python.h>

static PyObject *method_loads(PyObject *self, PyObject *args);
static PyObject *method_dumps(PyObject *self, PyObject *args);
int _check_dict(PyObject *dict, size_t *lenght);

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
    //PyObject *key = NULL;
    //PyObject *value = NULL;

    if(!PyArg_ParseTuple(args, "s", &json_str))
        return NULL;

    if (!(dict = PyDict_New())) {
        printf("ERROR: Failed to create Dict Object\n");
        return NULL;
    }
    printf("In loads\n");
    return dict;
};

static PyObject *method_dumps(PyObject *self, PyObject *args) {
    
    PyObject *json_dict = NULL;
    char *json_str = NULL;
    size_t lenght = 0;
    Py_ssize_t dict_size = 0;

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
    // allocate memory for dict and ","; ":"; " " -> 3*sizeof(char) + "{" + "}"
    dict_size = PyDict_Size(json_dict);
    json_str = malloc(lenght + sizeof(char)*(2+3*dict_size));

    //printf("Iter: %d , key: %s, val: %s\n", pos, key_char, val_char);
        //strcat(json_str, key_char);
        //strcat(json_str, ": ");
        //strcat(json_str, val_char);


    //strcat(json_str, "}\0");
    //json_str = "succc";
    return PyObject_Repr(json_dict);
    //return Py_BuildValue("s", json_str);
};


int _check_dict(PyObject *dict, size_t *lenght){

    PyObject *key, *value;
    Py_ssize_t pos = 0;
    size_t len = 0;

    while (PyDict_Next(dict, &pos, &key, &value)) {

        if (!PyObject_IsInstance(key, &PyUnicode_Type)) {

            printf("ERROR: dict's key isn't string\n");
            return 0;
        }
        if(
            !(PyObject_IsInstance(value, &PyUnicode_Type) ||
            PyObject_IsInstance(value, &PyFloat_Type) ||
            PyObject_IsInstance(value, &PyLong_Type))
            ) {
            printf("ERROR: dict's val isn't <str>, <int> or <float>\n");
            return 0;
        }     
        len += strlen(PyUnicode_AsUTF8(PyObject_Repr(key)));
        len += strlen(PyUnicode_AsUTF8(PyObject_Repr(value)));

    }
    *lenght = len;
    return 1;
}

int _make_string(PyObject *dict, const char *string){
    return 1;
}
/*
        if(PyObject_IsInstance(value, &PyUnicode_Type)) {
            val_char = PyUnicode_AsUTF8(value);
        }
        else if(PyObject_IsInstance(value, &PyFloat_Type)) {
            represent = PyObject_Repr(value);
            val_char = PyUnicode_AsUTF8(represent);
        }
        else if(PyObject_IsInstance(value, &PyLong_Type)) {
            represent = PyObject_Repr(value);
            val_char = PyUnicode_AsUTF8(represent);
        }
        else{
            printf("ERROR: dict's val isn't <str>, <int> or <float>\n");
            return 0;
        }
*/
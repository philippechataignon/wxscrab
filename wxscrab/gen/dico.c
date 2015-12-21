#include <Python.h>
#include "structmember.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <ctype.h>
#include "dic_internals.h"
#include "dic.h"

typedef struct {
    PyObject_HEAD
    Dictionary dic;
} dico;

unsigned int
num_noeud_mot_rec(Dictionary dic, const char* mot, int n, unsigned int e)
{
    unsigned int p;

    if (mot[n]) {
        char c = (mot[n] & 0x1f) ;
        for(p = Dic_succ(dic,e); p && Dic_chr(dic,p)<=c ; p = Dic_next(dic,p)) {
            if ( c == Dic_chr(dic,p) ) {
                return num_noeud_mot_rec(dic, mot, n+1, p) ;
            }
        }
        return 0 ;
    } else {
        return e ;
    }
}

int
num_noeud_mot(Dictionary dic, const char* mot) {
    return num_noeud_mot_rec(dic,mot,0,Dic_root(dic)) ;
}
    
int
test_mot(Dictionary dic, const char* mot) {
    return Dic_word(dic,num_noeud_mot(dic,mot)) ;
}
    
static void
dico_dealloc(dico* self)
{
    self->ob_type->tp_free((PyObject*)self);
}

static PyObject *
dico_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    dico *self;
    self = (dico *)type->tp_alloc(type, 0);
    return (PyObject *)self;
}

static int
dico_init(dico *self, PyObject *args, PyObject *kwds)
{
    char* nomdic ;
    if (!PyArg_ParseTuple(args, "s", &nomdic)) {
        return -1;
    }
    if (Dic_load(&self->dic, nomdic)) {
        return -2;
    }
    return 0;
}

static PyObject *
dico_isMot(dico*self, PyObject *args)
{
    int e ;
    char *mot;
    if (!PyArg_ParseTuple(args, "s", &mot))
        return NULL;
    e = test_mot(self->dic,mot);
    return Py_BuildValue("i", e);
}

static PyMemberDef dico_members[] = {
    {NULL}  /* Sentinel */
};

static PyMethodDef dico_methods[] = {
    {"isMot",  (PyCFunction)dico_isMot, METH_VARARGS, "Teste existence d'un mot."},
    {NULL}  /* Sentinel */
};

static PyTypeObject dicoType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "dico.dico",             /*tp_name*/
    sizeof(dico),             /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)dico_dealloc, /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
    "dico objects",           /* tp_doc */
    0,                     /* tp_traverse */
    0,                     /* tp_clear */
    0,                     /* tp_richcompare */
    0,                     /* tp_weaklistoffset */
    0,                     /* tp_iter */
    0,                     /* tp_iternext */
    dico_methods,             /* tp_methods */
    dico_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)dico_init,      /* tp_init */
    0,                         /* tp_alloc */
    dico_new,                 /* tp_new */
};

static PyMethodDef module_methods[] = {
    {NULL}  /* Sentinel */
};

PyMODINIT_FUNC
initdico(void) 
{
    PyObject* m;

    if (PyType_Ready(&dicoType) < 0)
        return;

    m = Py_InitModule3("dico", module_methods,
                       "Module that creates an dictionnary type.");

    if (m == NULL)
      return;

    Py_INCREF(&dicoType);
    PyModule_AddObject(m, "dico", (PyObject *)&dicoType);
}

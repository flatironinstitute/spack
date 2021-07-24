from spack import *
import spack.pkg.builtin.py_ipykernel as builtin

class PyIpykernel(builtin.PyIpykernel):
    provides('jupyter-kernel')

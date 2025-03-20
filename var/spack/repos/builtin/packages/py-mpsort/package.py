# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMpsort(PythonPackage):
    """Massively Parallel Histogram Sort"""

    homepage = "https://github.com/rainwoodman/MP-sort"

    version(
        "0.1.17-59-gfb201bd",
        url="https://github.com/rainwoodman/MP-sort/archive/fb201bd5f3d6d4458d46dafce5301b2f1e188649.tar.gz",
        sha256="5db3e04e1232d015c99d97be8055c04f2d52a6f300c872d1d7af8e6eb739b64b",
    )

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-cython", type=("build", "run"))
    depends_on("mpi")
    depends_on("py-mpi4py", type=("build", "run"))

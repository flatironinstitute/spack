# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHealpy(PythonPackage):
    """healpy is a Python package to handle pixelated data on the sphere."""

    homepage = "https://healpy.readthedocs.io/"
    pypi = "healpy/healpy-1.13.0.tar.gz"

    license("GPL-2.0-or-later", checked_by="lgarrison")

    version("1.18.0", sha256="6a12fd8f804c8a6d193dc43d1dcdf636808830e1ccc0aa7c53d83e394bb15289")
    version("1.14.0", sha256="2720b5f96c314bdfdd20b6ffc0643ac8091faefcf8fd20a4083cedff85a66c5e")
    version("1.13.0", sha256="d0ae02791c2404002a09c643e9e50bc58e3d258f702c736dc1f39ce1e6526f73")
    version("1.7.4", sha256="3cca7ed7786ffcca70e2f39f58844667ffb8521180ac890d4da651b459f51442")

    variant("all", default=False, description="Install all optional dependencies")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")  # generated

    with when("@1.18.0:"):
        depends_on("python@3.10:", type=("build", "run"))
        depends_on("py-setuptools@60:", type="build")
        depends_on("py-setuptools-scm@8.0:", type="build")
        depends_on("py-cython@0.16:", type="build")
        depends_on("py-numpy@2.0.0rc1:", type="build")
        depends_on("pkgconfig", type="build")
        depends_on("py-numpy@1.19:", type="run")
        depends_on("py-astropy", type="run")

        depends_on("cfitsio", type=("build", "link", "run"))
        depends_on("healpix-cxx", type=("build", "link", "run"))
        # depends_on("libsharp", type=("build", "link", "run"))

        depends_on("py-matplotlib", type=("build", "run"), when="+all")
        depends_on("py-scipy", type=("build", "run"), when="+all")

    with when("@:1.14.0"):
        depends_on("py-setuptools@3.2:", type="build")
        depends_on("py-pkgconfig", type="build")
        depends_on("py-numpy@1.13:", type=("build", "run"))
        depends_on("py-scipy", type=("build", "run"))
        depends_on("py-astropy", type=("build", "run"))
        depends_on("py-matplotlib", type=("build", "run"))
        depends_on("py-six", type=("build", "run"))
        depends_on("cfitsio", type=("build", "run"))
        depends_on("healpix-cxx", type=("build", "run"))

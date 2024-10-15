# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArviz(PythonPackage):
    """ArviZ (pronounced "AR-vees") is a Python package for exploratory
    analysis of Bayesian models. Includes functions for posterior analysis,
    model checking, comparison and diagnostics."""

    homepage = "https://github.com/arviz-devs/arviz"
    pypi = "arviz/arviz-0.6.1.tar.gz"

    license("Apache-2.0")

    version("0.15.1", sha256="981cce0282bdf6f3b379255b95a440979f9a0ef0ae9dd88a54f763cf5b31484c")
    version("0.6.1", sha256="435edf8db49c41a8fa198f959e7581063006c49a4efdef4755bb778db6fd4f72")

    depends_on("py-setuptools", type="build")
    depends_on("py-matplotlib@3.0:", type=("build", "run"))
    depends_on("py-numpy@1.12:", type=("build", "run"))
    depends_on("py-scipy@0.19:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-pandas@0.23:", type=("build", "run"))
    depends_on("py-xarray@0.11:", type=("build", "run"))
    depends_on("py-netcdf4", type=("build", "run"))

    with when("@0.15.1"):
        depends_on("py-setuptools@60:", type="build")
        depends_on("py-matplotlib@3.2:", type=("build","run"))
        depends_on("py-numpy@1.20.0:", type=("build","run"))
        depends_on("py-scipy@1.8.0:", type=("build","run"))
        depends_on("py-pandas@1.3.0:", type=("build","run"))
        depends_on("py-xarray@0.21.0:", type=("build","run"))
        depends_on("py-h5netcdf@1.0.2:", type=("build","run"))
        depends_on("py-typing-extensions@4.1.0:", type=("build","run"))
        depends_on("py-xarray-einstats@0.3:", type=("build","run"))

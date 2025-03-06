# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBottleneck(PythonPackage):
    """A collection of fast NumPy array functions written in Cython."""

    homepage = "https://github.com/pydata/bottleneck"
    pypi = "Bottleneck/bottleneck-1.4.2.tar.gz"

    license("BSD-2-Clause")

    version("1.4.2", sha256="fa8e8e1799dea5483ce6669462660f9d9a95649f6f98a80d315b84ec89f449f4")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-versioneer", type="build")
    depends_on("py-numpy", type=("build", "run"))

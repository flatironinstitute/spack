# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJaracoFunctools(PythonPackage):
    """Functools like those found in stdlib"""

    homepage = "https://github.com/jaraco/jaraco.functools"
    pypi = "jaraco.functools/jaraco_functools-2.0.tar.gz"

    license("MIT")

    version("4.1.0", sha256="70f7e0e2ae076498e212562325e805204fc092d7b4c17e0e86c959e249701a9d")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm@1.15.0:", type="build")
    depends_on("py-more-itertools", type=("build", "run"))
    depends_on("python@2.7:", type=("build", "run"))

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHalotools(PythonPackage):
    """Python package for studying large scale structure, cosmology, and galaxy
    evolution using N-body simulations and halo models"""

    homepage = "https://halotools.readthedocs.io/"
    pypi = "halotools/halotools-0.8.1.tar.gz"

    version("0.9.3", sha256="6d7448f00b489cc8a7552bbac57b894f1339280c0a103465fdfe991d3dc59600")
    version("0.8.1", sha256="defc8913f06e2bf69ca33b4167eb61fa5277810a5daedd1b84846186061a78e3")

    variant("extras", default=True, description="Install the 'all' set of extras", when="@0.8.1")

    depends_on("python@3.9:", type=("build", "run"))
    # depends_on("python@3.11:", type=("build", "run"), when="@0.9.3:")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-cython@3.0.2:", type="build", when="@0.9.3:")
    depends_on("py-extension-helpers", type="build")
    depends_on("py-extension-helpers@1", type="build", when="@0.9.3:")
    depends_on("py-numpy@2.0:", type="build", when="@0.9.3:")

    depends_on("py-astropy", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-beautifulsoup4", type=("build", "run"))
    depends_on("py-cython", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-h5py", type=("build", "run"), when="+extras")
    depends_on("py-h5py", type=("build", "run"), when="@0.9.3:")

    @when("@0.9.3")
    def patch(self):
        filter_file(r"requires-python\s*=.*", 'requires-python = ">=3.10"', "pyproject.toml")

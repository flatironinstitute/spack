# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterServerProxy(PythonPackage):
    """
    Jupyter Server Proxy lets you run arbitrary external processes
    (such as RStudio, Shiny Server, Syncthing, PostgreSQL, Code Server, etc)
    alongside your notebook server and provide authenticated web access to them
    using a path like /rstudio next to others like /lab.
    """

    homepage = "https://github.com/jupyterhub/jupyter-server-proxy"
    pypi = "jupyter_server_proxy/jupyter_server_proxy-4.1.0.tar.gz"

    license("BSD-3-Clause")

    version("4.0.0", sha256="f5dc12dd204baca71b013df3522c14403692a2d37cb7adcd77851dbab71533b5")

    depends_on("py-hatchling@1.4.0:", type="build")
    depends_on("py-hatch-jupyter-builder@0.5:", type="build")
    depends_on("py-hatch-nodejs-version", type="build")
    depends_on("py-jupyterlab@3.4.7:3", type="build")
    depends_on("py-setuptools@40.8.0:", type="build")
    depends_on("npm", type="build")

    depends_on("py-aiohttp", type=("build", "run"))
    depends_on("py-jupyter-server@1.0:", type=("build", "run"))
    depends_on("py-simpervisor@0.4:", type=("build", "run"))

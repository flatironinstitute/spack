# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-disbatch
#
# You can edit this file again by typing:
#
#     spack edit py-disbatch
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os

class PyDisbatch(PythonPackage):
    """Distributed processing of a batch of tasks"""

    homepage = "https://github.com/flatironinstitute/disBatch"
    url      = "https://github.com/flatironinstitute/disBatch/archive/refs/tags/1.4.tar.gz"

    version('1.4', sha256='ce3a1079f895ddc0029cd21db3a5f4bf07602392a7587bdf99e4e04834e91516')
    version('2.0-rc1', sha256='d95bcfdb23d5652cd35714e5aaf71d66dc1f39d4486c814567ad80daec4e8484')
    depends_on('py-kvsstcp', type=('run'))

    @run_after('install')
    def create_symlink(self):
        script_source = os.path.join(self.prefix.bin, 'disBatch.py')
        script_dest = os.path.join(self.prefix.bin, 'disBatch')
        os.symlink(script_source, script_dest)

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
#     spack install python-dummy
#
# You can edit this file again by typing:
#
#     spack edit python-dummy
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PythonBlasBackend(BundlePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add proper versions here.
    version('3.8.6')

    # FIXME: Add dependencies if required.
    depends_on('python@3.8.6')
    depends_on('py-numpy@1.19.4')
    depends_on('py-scipy@1.5.4')

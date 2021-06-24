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
#     spack install openmpi-opa
#
# You can edit this file again by typing:
#
#     spack edit openmpi-opa
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class OpenmpiOpa(BundlePackage):
    """Load openmpi4 for Omnipath fabric"""

    # FIXME: Add a proper url for your package's homepage here.
    # homepage = "https://www.example.com"
    # There is no URL since there is no code to download.

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    # FIXME: Add proper versions here.
    version('4.0.5')

    # FIXME: Add dependencies if required.
    depends_on('openmpi@4:')

    # There is no need for install() since there is no code.

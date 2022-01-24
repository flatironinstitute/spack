# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Sina(CachedCMakePackage):
    """Sina C++ Library"""

    homepage = 'https://github.com/LLNL/Sina'
    url = 'https://github.com/LLNL/Sina/releases/download/v1.10.0/sina-cpp-1.10.0.tar.gz'

    maintainers = [
        'estebanpauli',
        'HaluskaR',
        'murray55',
    ]

    version('1.10.0', sha256='b34379ce8cc5eca5a0f16893053fac75be14c2109d1beed4c6d48e11f9b281c7')

    variant('docs', default=False,
            description='Allow generating documentation')
    variant('adiak', default=False,
            description='Create interface for calling Sina through Adiak')
    variant('test', default=False,
            description='Build tests')

    depends_on('cmake@3.8.0:', type='build')
    depends_on('adiak', when='+adiak')
    depends_on('doxygen', type='build', when='+docs')
    depends_on('conduit')

    def cmake_args(self):
        return [
            self.define_from_variant('-DSINA_BUILD_ADIAK_BINDINGS', 'adiak'),
            self.define_from_variant('-DSINA_BUILD_TESTS', 'test'),
            self.define_from_variant('-DSINA_BUILD_DOCS', 'docs'),
        ]

    def initconfig_package_entries(self):
        entries = [
            '#' + 78 * '-',
            '# Library Dependencies',
            '#' + 78 * '-'
        ]

        conduit_dir = self.spec['conduit'].prefix
        entries.append(cmake_cache_path(
            'Conduit_DIR',
            '%s/lib/cmake/conduit' % conduit_dir))

        use_adiak = self.spec.satisfies('^adiak')
        entries.append(cmake_cache_option('SINA_BUILD_ADIAK_BINDINGS', use_adiak))
        if use_adiak:
            adiak_dir = self.spec['adiak'].prefix
            entries.append(cmake_cache_path(
                'adiak_DIR',
                '%s/lib/cmake/adiak/' % adiak_dir))

        entries.append('#' + 78 * '-')
        entries.append('# Devtools')
        entries.append('#' + 78 * '-')

        build_tests = self.spec.satisfies('+test')
        entries.append(cmake_cache_option('SINA_BUILD_TESTS', build_tests))

        build_docs = self.spec.satisfies('+docs')
        entries.append(cmake_cache_option('SINA_BUILD_DOCS', build_docs))
        if build_docs:
            doxygen_bin_dir = self.spec['doxygen'].prefix.bin
            entries.append(cmake_cache_path(
                'DOXYGEN_EXECUTABLE', os.path.join(doxygen_bin_dir, 'doxygen')))

        return entries

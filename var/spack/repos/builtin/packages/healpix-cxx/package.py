# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class HealpixCxx(Package):
    """Healpix is a library for calculating
    Hierarchical Equal Area isoLatitude Pixelation of a sphere."""

    homepage = "https://healpix.sourceforge.io"
    url = "https://downloads.sourceforge.net/project/healpix/Healpix_3.82/Healpix_3.82_2022Jul28.tar.gz"

    license("GPL-2.0-or-later", checked_by="lgarrison")

    version(
        "3.83",
        url="https://downloads.sourceforge.net/project/healpix/Healpix_3.83/Healpix_3.83_2024Nov13.tar.gz",
        sha256="8876c18efc596fd706b2a004ac15f2fb60b795f2db6fbabea9d8ccf549531dda",
    )
    version("3.82", sha256="47629f057a2daf06fca3305db1c6950edb9e61bbe2d7ed4d98ff05809da2a127")

    depends_on("cfitsio")

    phases = ["configure", "install"]

    def patch(self):
        prefix = self.prefix
        config = FileFilter("hpxconfig_functions.sh")
        config.filter(r"^\s*SHARPPREFIX=.*", f"SHARPPREFIX={prefix}")
        config.filter(r"^\s*CXXPREFIX=.*", f"CXXPREFIX={prefix}")
        config.filter(r'SHARP_LIBS="[^"]*"', f'SHARP_LIBS="-L{prefix.lib} -lsharp"')
        config.filter(r'SHARP_CFLAGS="[^"]*"', f'SHARP_CFLAGS="-I{prefix.include}"')
        config.filter(r"^\s*F90_BINDIR=.*", f"F90_BINDIR={prefix.bin}")
        config.filter(r"^\s*F90_INCDIR=.*", f"F90_INCDIR={prefix.include}")
        config.filter(r"^\s*F90_LIBDIR=.*", f"F90_LIBDIR={prefix.lib}")
        config.filter(r'^\s*ExtendCFLAGS "-I.*\/include"', f'ExtendCFLAGS "-I{prefix.include}"')

    def configure(self, spec, prefix):
        configure = Executable("./configure")
        configure(*self.configure_args(), extra_env=self.configure_env(spec))

    def configure_args(self):
        return ["-L", "--auto=c,cxx,f90"]

    def configure_env(self, spec):
        return dict(
            SHELL="sh",
            C_SHARED="1",
            FITSDIR=spec["cfitsio"].prefix.lib,
            FITSINC=spec["cfitsio"].prefix.include,
            SHARP_COPT="-O3 -ffast-math",
            F_SHARED="1",
        )

    def install(self, spec, prefix):
        make = Executable("make")
        make("-j", str(make_jobs), "all", *self.make_args())

    def make_args(self):
        prefix = self.prefix
        return [f"C_LIBDIR={prefix.lib}", f"C_INCDIR={prefix.include}"]

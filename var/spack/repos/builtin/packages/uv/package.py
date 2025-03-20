# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.filesystem as fs

from spack.package import *


class Uv(CargoPackage):
    """An extremely fast Python package and project manager, written in Rust."""

    homepage = "https://docs.astral.sh/uv"
    url = "https://github.com/astral-sh/uv/releases/download/0.6.8/source.tar.gz"

    license("APACHE 2.0 or MIT", checked_by="lgarrison")

    version("0.6.8", sha256="462929b218cdd4c4f197f611f132fa55329a8f3558d164ec06ee5b5b0a48cee0")

    depends_on("c", type="build")

    depends_on("rust@1.83:")

    def build(self, spec, prefix) -> None:
        with fs.working_dir(self.build_directory):
            self.module.cargo(
                "install",
                "--root",
                "out",
                "--path",
                "crates/uv",
                *self.std_build_args,
                *self.build_args,
            )

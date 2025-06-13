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

    version("0.7.13", sha256="04abb241591dd374f7f1b9fea6cc43180e99c8c2607767b06d31c78e1ce3cd65")
    version("0.6.8", sha256="462929b218cdd4c4f197f611f132fa55329a8f3558d164ec06ee5b5b0a48cee0")

    variant("module_append_path", default=False, description="Have the module append to PATH instead of prepending")

    depends_on("c", type="build")

    depends_on("rust@1.83:", when="@0.6.8:")
    depends_on("rust@1.85:", when="@0.7.13:")

    def build(self, spec, prefix) -> None:
        with fs.working_dir(self.build_directory):
            self.module.cargo(
                "install",
                "--locked",
                "--root",
                "out",
                "--path",
                "crates/uv",
                *self.std_build_args,
                *self.build_args,
            )

    def setup_run_environment(self, env):
        if "+module_append_path" in self.spec:
            env.append_path("PATH", self.prefix.bin)
        else:
            env.prepend_path("PATH", self.prefix.bin)

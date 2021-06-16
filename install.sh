#!/bin/bash -e

export LC_ALL=en_US.UTF-8 # work around spack bugs processing log files
source share/spack/setup-env.sh

echo '*** Bootstrapping compilers'
spack env activate -V bootstrap
spack install || { spack env view regenerate && spack install; }

echo '*** Building modules'
spack env activate -V modules
spack concretize -f
spack gc -y || true
spack install --only-concrete --fail-fast

spack_ls () {
	spack find -cx --format '{name}@{version}/{hash:7}' "$@" | sort
}

filter_out () {
	comm -23 - <("$@")
}

echo '*** Activate python packages'
# activate all non-MPI python packages
parallel spack activate -- $(spack_ls '^python'
	| filter_out spack_ls '^python' '^mpi'
	| filter_out spack_ls '^python' '^openblas'
	| filter_out spack_ls '^python' '^qt'
	| grep '^py-')

#sudo $(spack location -i singularity)/bin/spack_perms_fix.sh

echo '*** Building lmod files'
spack module lmod refresh -y --delete-tree
ln -s 7.5.0 $SPACK_ROOT/share/spack/lmod/linux-centos7-x86_64/Core/gcc/default

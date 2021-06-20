#!/bin/bash -e
#SBATCH -c 8

while getopts 'fgj:' o ; do case $o in
	(f) full=1 ;;
	(g) gc=1 ;;
	(j) njobs="$OPTARG" ;;
	(*)
		echo "Usage: ./install.sh [-g] [-f] [-j N]"
		echo "       sbatch -n N install.sh [-g] [-f]"
		echo "Build spack modules. Can be used as an sbatch script."
		echo " -g    gc first"
		echo " -f    concretize -f"
		echo " -j N  parallel jobs"
		exit 1
esac ; done

export LC_ALL=en_US.UTF-8 # work around spack bugs processing log files
source share/spack/setup-env.sh

if [[ $gc ]] ; then
	spack gc -y || true
fi

if [[ -n $SLURM_JOB_ID ]] ; then
	spack_install() {
		srun -K0 -W0 -k spack -l install -j ${njobs:-${SLURM_CPUS_PER_TASK:-40}} "$@"
	}
else
	spack_install() {
		spack install ${njobs:+-j $njobs} "$@"
	}
fi

echo '*** Bootstrapping compilers'
spack env activate -V bootstrap
spack_install || { spack env view regenerate && spack_install --fail-fast; }

echo '*** Building modules'
spack env activate -V modules
spack concretize ${full:+-f}
spack_install --only-concrete --fail-fast

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

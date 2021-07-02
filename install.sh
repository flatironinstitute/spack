#!/bin/bash -e
#SBATCH -c 8

njobs=$SLURM_CPUS_PER_TASK

if [[ $USER == spack ]] ; then
	prod=1
fi

PRODROOT=/cm/shared/sw/spack

while getopts 'fgj:p:rR:' o ; do case $o in
	(f) full=1 ;;
	(g) gc=1 ;;
	(j) njobs="$OPTARG" ;;
	(p) parallel="$OPTARG" ;;
	(r|R) rel=${OPTARG:-$(date +%Y%m%d)} ;;
	(*)
		echo "Usage: ./install.sh [-g] [-f] [-j N]"
		echo "       sbatch -n N install.sh [-g] [-f]"
		echo "Build spack modules. Can be used as an sbatch script."
		echo " -g      gc first"
		echo " -f      concretize -f"
		echo " -j N    parallel jobs within each build"
		echo " -p N    parallel builds"
		echo " -r      use (new) production release named $PRODROOT/YYYYMMDD"
		echo " -R PATH use install root or production release [$PRODROOT/]PATH"
		exit 1
esac ; done

mkdir -p /mnt/home/spack/root/$USER
# work around gpfs lock bug by using ceph instead:
ln -sfT /mnt/ceph/users/spack/db/$USER /mnt/home/spack/root/$USER/.spack-db || echo "*** Please move your .spack-db directory to ceph to enable locking!"

export LC_ALL=en_US.UTF-8 # work around spack bugs processing log files
source share/spack/setup-env.sh

if [[ $prod && ( $USER != spack || $HOST != worker1000 ) || ( -z $prod && $rel ) ]] ; then
	echo "Production should be run as spack@worker1000.  This probably won't work..."
fi

run() {
	echo "> $*"
	"$@"
}

spack_install() {
	set -- spack -l install ${njobs:+-j $njobs} "$@"
	if [[ -n $parallel ]] ; then
		# is there some better way?
		l="${@:$#}"
		n=$[$#-1]
		set -- parallel "${@:1:$n}" --
		for (( i=0 ; i<$parallel ; i++ )) ; do
			set -- "$@" "$l"
		done
	elif [[ -n $SLURM_JOB_ID ]] ; then
		set -- srun -K0 -W0 -k "$@"
	fi
	run "$@"
}

spack_ls () {
	spack find -c --format '{name}@{version}/{hash:7}' "$@" | sort
}

filter_out () {
	comm -23 - <("$@")
}

if [[ $rel ]] ; then
	if [[ $rel != /* ]] ; then
		rel=$PRODROOT/$rel
	fi
	run spack config --scope user add config:install_tree:root:$rel
fi

run spack gpg trust /mnt/home/spack/cache/build_cache/_pgp/*.pub

if [[ $gc ]] ; then
	run spack gc -y || true
fi

echo '*** Bootstrapping compilers'
run spack env activate -V bootstrap
spack_install || { run spack env view regenerate && spack_install --fail-fast; }

echo '*** Building modules'
run spack env activate -V modules
run spack concretize ${full:+-f} | tee concretize.log
spack_install --only-concrete --fail-fast
#run spack env view regenerate

if [[ $prod ]] ; then
	for sing in $(spack location -i singularity) ; do
		run sudo $sing/bin/spack_perms_fix.sh
	done
fi

echo '*** Building lmod files'
run spack module lmod refresh -y --delete-tree
run spack module lmod setdefault gcc@7.5.0%gcc@7.5.0

#!/bin/bash -e

source share/spack/setup-env.sh
export INTEL_LICENSE_FILE=28518@lic1.flatironinstitute.org

SPACK_INSTALL() {
    echo "spack install $@"
    spack install "$@"
}

SPACK_ACTIVATE() {
    echo "spack activate $@"
    spack activate "$@"
}

compilers=(
    %gcc@7.4.0
    %gcc@10.2.0
    # %intel
)

mpis=(
    openmpi@1.10.7
    openmpi@2.1.6
    openmpi@4.0.5
)


in_list() {
    checkval=$1
    shift
    list=("$@")
    for val in "${list[@]}"; do
        if [ "$val" == "$checkval" ]; then
            return 0
        fi
    done
    return 1
}

# python packages that implicitly depend on blas
declare -a python_blas_packages=(
    "py-pandas@1.1.4"
    "py-scikit-learn@0.23.2"
    "py-numba@0.50.1"
    "py-emcee@2.2.1"
    "py-astropy@4.0.1.post1"
    "py-dask@2.16.0"
    "py-seaborn@0.9.0"
    "py-matplotlib@3.3.3"
)

# python packages that don't depend on blas at all
declare -a python_packages=(
    "py-cherrypy@18.1.1"
    "py-flask@1.1.2"
    "py-pip@20.2"
    "py-ipython@7.18.1"
    "py-pyyaml@5.3.1"
    "py-pylint@2.3.1"
    "py-autopep8@1.4.4"
    "py-sqlalchemy@1.3.19"
    "py-nose@1.3.7"
    "py-mako@1.0.4"
    "py-pkgconfig@1.5.1"
    "py-virtualenv@16.7.6"
    "py-sympy@1.4"
    "py-pycairo@1.18.1"
    "py-sphinx@3.2.0"
    "py-pytest@5.3.4"
    "py-hypothesis@5.3.0"
)

compiler=%gcc@7.4.0
SPACK_INSTALL emacs@27.1 $compiler+X toolkit=athena \
      vim@8.2.1201        $compiler+x+python+gui+huge+cscope+lua+ruby \
      zsh@5.8             $compiler \
      mathematica@11.2    $compiler \
      mathematica@11.3    $compiler \
      mathematica@12.1    $compiler \
      mathematica@12.2    $compiler \
      matlab@R2018        $compiler \
      matlab@R2018b       $compiler \
      matlab@R2020a       $compiler \
      cmake@3.18.4        $compiler \
      git@2.29.0          $compiler \
      gdb@9.2             $compiler \
      slurm               $compiler \
      mercurial@5.3       $compiler \
      node-js@12.18.4     $compiler \
      node-js@14.13.0     $compiler \
      go@1.15.2           $compiler \
      rclone@1.51.0       $compiler \
      subversion@1.14.0   $compiler \
      tmux@3.1b           $compiler \
      valgrind@3.15.0~mpi $compiler \
      gperftools@2.7      $compiler \
      lftp@4.8.1          $compiler \
      curl@7.72.0         $compiler \
      r+X@4.0.3           $compiler

for compiler in "${compilers[@]}"; do
    # Core installs
    SPACK_INSTALL boost@1.74.0                     $compiler \
     boost@1.74.0%clang+clanglibcpp ^bzip2         $compiler ^zlib$compiler \
     cuda@11.1.0                                   $compiler \
     cudnn@8.0.4.30-11.1-linux-x64                 $compiler \
     eigen@3.3.8                                   $compiler \
     fftw@2.1.5 mpi=false \
          precision=float,double                   $compiler \
     fftw@3.3.8 mpi=false \
          precision=float,double,quad,long_double  $compiler \
     gsl@2.5+external-cblas ^openblas threads=none $compiler \
     gsl@2.5+external-cblas ^intel-mkl             $compiler \
     hdf5@1.8.21+fortran~mpi+cxx                   $compiler \
     hdf5@1.10.7+fortran~mpi+cxx                   $compiler \
     intel-mkl@2020.3.279                          $compiler \
     intel-oneapi-mkl@2021.1.1                     $compiler \
     llvm@10.0.1                                   $compiler \
     llvm@11.0.1                                   $compiler \
     llvm@12.0.0                                   $compiler \
     nfft@3.4.1 ^fftw@3.3.8~mpi \
          precision=float,double,quad,long_double  $compiler \
     openblas@0.3.12 threads=none                  $compiler \
     openblas@0.3.12 threads=openmp                $compiler \
     openblas@0.3.12 threads=pthreads              $compiler \
     openmpi-opa@4.0.5                             $compiler


    # python time!
    # python default to multithreaded openblas
    # python-blas-backend is a custom package that includes scipy/numpy
    SPACK_INSTALL python@3.8.6      $compiler \
          python-blas-backend@3.8.6 $compiler ^openblas@0.3.12 threads=pthreads \
          python-blas-backend@3.8.6 $compiler ^intel-mkl@2020.3.279

    # I cache the active extensions, because each "activate" alone takes forever, even if it's
    # already activated.
    echo "Getting active python extensions (takes a minute or two)"
    active_python_extensions=$(spack extensions -s activated python$compiler | tail -n+3)

    # blas stuff requires a blas spec
    SPACK_INSTALL $(printf "%s%$compiler ^openblas@0.3.12 threads=pthreads " "${python_blas_packages[@]}")
    for package in ${python_blas_packages[@]}; do
        if ! in_list $package $active_python_extensions; then
            SPACK_ACTIVATE $package $compiler ^openblas@0.3.12 threads=pthreads
        fi
    done

    # all non-blas python packages
    SPACK_INSTALL $(printf "%s%$compiler " "${python_packages[@]}")
    for package in ${python_packages[@]}; do
        if ! in_list $package $active_python_extensions; then
            SPACK_ACTIVATE $package $compiler
        fi
    done

    # Non-default or otherwise special python modules

    # need to have py-pyqt5 as external module for now, because there is a conflict with py-sip
    # on the merge, so we activate py-sip, and then load py-pyqt5 via module if needed.
    # Mesa dependency fails with llvm@12, so we use 11 here.
    # Qt is failing to build with gcc@10
    SPACK_INSTALL py-pyqt5@5.13.1 $compiler ^py-sip@4.19.21 ^llvm@11.0.1
    if ! in_list py-sip@4.19.21 $active_python_extensions; then
        SPACK_ACTIVATE py-sip@4.19.21 $compiler
    fi

    SPACK_INSTALL py-jupyter@1.0.0 $compiler ^llvm@11.0.1

    # h5py, since it uses a variant, needs its own install
    SPACK_INSTALL py-h5py@2.10.0 mpi=false $compiler ^openblas@0.3.12 threads=pthreads ^hdf5@1.10.7+fortran~mpi+cxx
    if ! in_list py-h5py@2.10.0 $active_python_extensions; then
        SPACK_ACTIVATE py-h5py@2.10.0 mpi=false $compiler ^openblas@0.3.12 threads=pthreads ^hdf5@1.10.7+fortran~mpi+cxx
    fi

    # requires git > 2
    spack load git%gcc@7.4.0
    CUDA_ARCH=35,60,70,80
    SPACK_INSTALL py-torch@1.7.0 cuda_arch=$CUDA_ARCH \
          $compiler ^openblas@0.3.12 threads=pthreads ^cudnn@8.0.4.30-11.1-linux-x64 ^nccl cuda_arch=$CUDA_ARCH
    SPACK_INSTALL py-torch@1.7.0 cuda_arch=$CUDA_ARCH \
          $compiler ^intel-mkl@2020.3.279 ^cudnn@8.0.4.30-11.1-linux-x64 ^nccl cuda_arch=$CUDA_ARCH
    spack unload git

    # ipython requires 7.18.1 requires py-prompt-toolkit@2, so ipdb needs this constraint since it tries for v3
    SPACK_INSTALL py-ipdb@0.10.1 $compiler ^py-prompt-toolkit@2:2
    if ! in_list py-ipdb@0.10.1 $active_python_extensions; then
        SPACK_ACTIVATE py-ipdb@0.10.1 $compiler
    fi

    # Anything dependent on MPI
    for mpi in "${mpis[@]}"; do
        SPACK_INSTALL $mpi $compiler

        # openmpi was compiled with gcc@7, so we can't compile hdf5 with fortran, because of
        # binary incompability with the openmpi fortran bindings in our external module
        if [ "$compiler" != "%gcc@7.4.0" ]; then
            SPACK_INSTALL hdf5@1.10.7+mpi~fortran $compiler ^$mpi \
                  hdf5@1.8.21+mpi~fortran $compiler ^$mpi \
                  py-h5py@2.10.0 $compiler ^$mpi ^openblas@0.3.12 threads=pthreads ^hdf5@1.10.7+mpi~fortran
        else
            SPACK_INSTALL hdf5@1.10.7+mpi+fortran $compiler ^$mpi \
                  hdf5@1.8.21+mpi+fortran $compiler ^$mpi \
                  py-h5py@2.10.0 $compiler ^$mpi ^openblas@0.3.12 threads=pthreads ^hdf5@1.10.7+mpi+fortran
        fi

        mpi_hash=$(spack find --format "{hash}" $mpi$compiler)
        SPACK_INSTALL boost@1.74.0+mpi     $compiler ^$mpi \
              # boost@1.74.0%clang+mpi+clanglibcpp  ^bzip2$compiler ^zlib$compiler ^$mpi/$mpi_hash \
              fftw@2.1.5                    $compiler ^$mpi \
              fftw@3.3.8                    $compiler ^$mpi \
              py-mpi4py@3.0.3               $compiler ^$mpi

    done
done

spack module lmod refresh -y --delete-tree
ln -s $PWD/share/spack/lmod/linux-centos7-x86_64/Core/gcc/7.4.0 \
   $PWD/share/spack/lmod/linux-centos7-x86_64/Core/gcc/default

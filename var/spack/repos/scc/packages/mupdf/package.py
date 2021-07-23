from spack import *


class Mupdf(MakefilePackage):
    """ MuPDF is a lightweight PDF, XPS, and E-book viewer. """

    homepage = "https://www.example.com"
    url      = "https://mupdf.com/downloads/archive/mupdf-1.18.0-source.tar.xz"

    version('1.18.0-rc1', sha256='754b4b5dcf00da2f1efef1f3de723607a6c32dd0256b81899e4dff9a297f415b')
    version('1.18.0',     sha256='592d4f6c0fba41bb954eb1a41616661b62b134d5b383e33bd45a081af5d4a59a')
    version('1.17.0-rc1', sha256='d826c16ecbf3fc5bde33685b5039dda7d50487a791cfbd2fadd55a50a7320737')
    version('1.17.0',     sha256='c935fb2593d9a28d9b56b59dad6e3b0716a6790f8a257a68fa7dcb4430bc6086')
    version('1.16.1',     sha256='6fe78184bd5208f9595e4d7f92bc8df50af30fbe8e2c1298b581c84945f2f5da')
    version('1.16.0-rc2', sha256='c94d9ed2dc7aff117a20aa160c14930dd48aaa072052201fb7f2a6da31777fc6')
    version('1.16.0-rc1', sha256='b17e98fcf0a44e61f4758ceaec88730e75259249b603b65682da0bf4b967541c')
    version('1.16.0',     sha256='d28906cea4f602ced98f0b08d04138a9a4ac2e5462effa8c45f86c0816ab1da4')
    version('1.15.0-rc1', sha256='4b8a7047c50265f1949bae6a4334f6e487c5a4b5d350a2abd766e4e00655f1b1')
    version('1.15.0',     sha256='565036cf7f140139c3033f0934b72e1885ac7e881994b7919e15d7bee3f8ac4e')
    version('1.14.0-rc1', sha256='4e432544b4949720a22ef51ea0718f62a5c8992b7882c0f81d040b55de615608')
    version('1.14.0',     sha256='603e69a96b04cdf9b19a3e41bd7b20c63b39abdcfba81a7460fcdcc205f856df')
    version('1.13.0-rc1', sha256='923aa31e360843fa76c9dcf7b73cf47d3c85e1abe3ffc54b5f2c2e2a0160bffa')
    version('1.13.0',     sha256='746698e0d5cd113bdcb8f65d096772029edea8cf20704f0d15c96cb5449a4904')
    version('1.12.0',     sha256='577b3820c6b23d319be91e0e06080263598aa0662d9a7c50af500eb6f003322d')
    version('1.12-rc1',   sha256='5ab34cf1dd23fb8db307eb16f263d654454aa82049a25df72e19e75a183559c6')

    def edit(self, spec, prefix):
        env['XCFLAGS'] = "-std=c99"
        self.install_targets = ['prefix={}'.format(prefix), 'install']

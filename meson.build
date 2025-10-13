project(
  'libpardus-xfce-tweaks',
  version: '0.1.0',
  license: 'GPL-3.0+',
)

py = import('python').find_installation()


src_files = files(
  glob('src/*.py')
)

# Install Python source files
py.install_sources(
  src_files
  subdir: 'libpardus_xfce_tweaks',
)
pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'stringbuddydemo')
gnome = import('gnome')

gnome.compile_resources('stringbuddydemo',
  'stringbuddydemo.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'stringbuddydemo.in',
  output: 'stringbuddydemo',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

stringbuddydemo_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'stringbuddy.py',
  'gousername.py',
]

install_data(stringbuddydemo_sources, install_dir: moduledir)

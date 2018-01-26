require 'rspec/core/rake_task'

build_var = ENV['CENTOS'] || 'centos7'
image_src = "docker/#{build_var}/Dockerfile.build"
image_tag = "wied03/#{build_var}/centos_cron"

desc 'Run serverspec integration tests'
RSpec::Core::RakeTask.new(:integration => :build)

task :default => [:clean, :unit, :integration]

task :clean do
  rm_rf 'centos-package-cron.spec'
end

file 'centos-package-cron.spec' do
  cp 'centos-package-cron.spec.in', 'centos-package-cron.spec'
  # initial installation
  sh './setup.py -V'
  complete_version = `./setup.py -V`.strip
  dist = /.*\.(\d+)/.match(complete_version)[1]
  version = /(.*)\.\d+/.match(complete_version)[1]
  sh "sed -i.bak 's/THE_VERSION/#{version}/g' centos-package-cron.spec"
  sh "sed -i.bak 's/THE_DIST/#{dist}/g' centos-package-cron.spec"
  rm 'centos-package-cron.spec.bak'
end

docker_build = lambda do |tag, src|
  sh "docker build -t #{tag} -f #{src} #{File.dirname(src)}"
end

task :build_image do
  docker_build[image_tag, image_src]
end

desc 'builds RPMs'
task :build => ['centos-package-cron.spec', :build_image] do
  zip_file = 'centos_package_cron_src.tgz'
  rm_rf zip_file
  # clean build
  sh "git archive -o #{zip_file} --prefix centos-package-cron/ HEAD"
  sh "docker run -e \"CENTOS=#{build_var}\" --rm=true -v `pwd`:/code -w /code -u nonrootuser -t #{image_tag} /code/build_inside_container.sh #{zip_file}"
end

task :unit_image do
  next if ENV['SKIP_UNIT']

  sh "docker build -t #{image_tag_unit} #{image_src_unit}"
end

desc 'Runs Python unit tests'
task :unit => :unit_image do
  next if ENV['SKIP_UNIT']
  args = "-a \"#{ENV['TESTS_TO_RUN']}\"" if ENV['TESTS_TO_RUN']
  args ||= ENV['UNIT_ARGS']
  sh "docker run --rm=true -e \"CENTOS=#{build_var}\" -v `pwd`:/code -w /code -u nonrootuser -t #{image_tag_unit} ./setup.py test #{args}"
end

desc 'Pushes to pypi'
task :push do
  sh './setup.py register -r pypi'
  sh './setup.py sdist upload -r pypi'
end

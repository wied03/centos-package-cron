require 'rspec/core/rake_task'

build_var = ENV['CENTOS'] || 'centos7'
version_var = build_var.include?('centos7') ? 'centos7' : 'centos6'
image_src_integration = "docker/#{build_var}/integration"
image_src_unit = "docker/#{build_var}/unit"
ENV['IMAGE_INTEGRATION'] = image_tag_integration = "wied03/#{build_var}_int"
image_tag_unit = "wied03/#{build_var}_unit"

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

task :integration_image do
  sh "docker build -t #{image_tag_integration} #{image_src_integration}"
end

desc 'builds RPMs'
task :build => ['centos-package-cron.spec', :integration_image] do
  zip_file = 'centos_package_cron_src.tgz'
  rm_rf zip_file
  # clean build
  sh "git archive -o #{zip_file} --prefix centos-package-cron/ HEAD"
  sh "docker run -e \"CENTOS=#{version_var}\" --rm=true -v `pwd`:/code -w /code -u nonrootuser -t #{image_tag_integration} /code/build_inside_container.sh #{zip_file}"
end

task :unit_image do
  next if ENV['SKIP_UNIT']

  sh "docker build -t #{image_tag_unit} #{image_src_unit}"
end

desc 'Runs Python unit tests'
task :unit => :unit_image do
  next if ENV['SKIP_UNIT']

  sh "docker run --rm=true -e \"CENTOS=#{version_var}\" -v `pwd`:/code -w /code -u nonrootuser -t #{image_tag_unit} ./setup.py test"
end

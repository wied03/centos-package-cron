require 'rspec/core/rake_task'

build_var = ENV['CENTOS'] || 'centos7'
image_dir = "docker/#{build_var}"
image_tag_prefix = "wied03/centos_cron/#{build_var}"
ENV['RUN_IMAGE_TAG'] = run_tag = "#{image_tag_prefix}/run"
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
  filename = "#{File.join(image_dir, src)}.Dockerfile"
  sh "docker build -t #{tag} -f #{filename} #{File.dirname(filename)}"
end

build_tag = "#{image_tag_prefix}/build"
task :build_images do
  docker_build[run_tag, "run"]
  docker_build[build_tag, "build"]
end

desc 'builds RPMs'
task :build => ['centos-package-cron.spec', :build_images] do
  zip_file = 'centos_package_cron_src.tgz'
  rm_rf zip_file
  # clean build
  sh "git archive -o #{zip_file} --prefix centos-package-cron/ HEAD"
  sh "docker run -e \"CENTOS=#{build_var}\" --rm=true -v `pwd`:/code -w /code -u nonrootuser -t #{build_tag} /code/build_inside_container.sh #{zip_file}"
end

desc 'Runs Python unit tests'
task :unit => :build_images do
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

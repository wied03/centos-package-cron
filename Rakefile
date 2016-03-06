task :default => [:clean, :unit, :integration]

task :clean do
  rm_rf 'centos-package-cron.spec'
end

centos_var = ENV['CENTOS']

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

desc 'builds RPMs'
task :build => 'centos-package-cron.spec' do
  sh "docker build -t wied03/#{centos_var}_int docker/#{centos_var}/integration"
  zip_file = 'centos_package_cron_src.tgz'
  rm_rf zip_file
  # clean build
  sh "git archive -o #{zip_file} --prefix centos-package-cron/ HEAD"
  sh "docker run -e \"CENTOS=#{centos_var}\" --rm=true -v `pwd`:/code -w /code -u nonrootuser -t wied03/#{centos_var}_int /code/build_inside_container.sh #{zip_file}"
end

desc 'Runs Python unit tests'
task :unit do
  if centos_var == 'centos67'
    # no 6.7 tests right now
    next
  end
  
  sh "docker build -t wied03/#{centos_var}_unit docker/#{centos_var}/unit"
  os = centos_var == 'centos7' ? 'centos7' : 'centos6'
  sh "docker run --rm=true -e \"CENTOS=#{os}\" -v `pwd`:/code -w /code -u nonrootuser -t wied03/#{centos_var}_unit ./setup.py test"
end

desc 'Runs integration test'
task :integration => :build do
  sh "docker build -t wied03/#{centos_var}_int docker/#{centos_var}/integration"
  sh "docker run --rm=true -v `pwd`:/code -w /code -u nonrootuser -t wied03/#{centos_var}_int /code/install_and_run_it.sh"
end

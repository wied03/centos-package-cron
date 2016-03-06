task :clean do
  rm_rf 'centos-package-cron.spec'
end

file 'centos-package-cron.spec' do
  cp 'centos-package-cron.spec.in', 'centos-package-cron.spec'
  complete_version = `./setup.py -V`.strip
  dist = /.*\.(\d+)/.match(complete_version)[1]
  version = /(.*)\.\d+/.match(complete_version)[1]
  sh "sed -i.bak 's/THE_VERSION/#{version}/g' centos-package-cron.spec"
	sh "sed -i.bak 's/THE_DIST/#{dist}/g' centos-package-cron.spec"
  rm 'centos-package-cron.spec.bak'
end

task :unit do
  centos_var = ENV['CENTOS']
  if centos_var == 'centos67'
    # no 6.7 tests right now
    next
  end
  
  sh "docker build -t wied03/#{centos_var}_unit docker/#{centos_var}/unit"
  os = centos_var == 'centos7' ? 'centos7' : 'centos6'
  sh "docker run --rm=true -e \"CENTOS=#{os}\" -v `pwd`:/code -w /code -u nonrootuser -t wied03/#{centos_var}_unit ./setup.py test"
end

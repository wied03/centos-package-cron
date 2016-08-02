require 'serverspec'
require 'docker'

set :backend, :docker
set :docker_image, ENV['IMAGE_INTEGRATION']
# testing this can take a while
Docker.options[:read_timeout] = 120
set :docker_container_create_options, {
  'User' => 'nonrootuser',
  'WorkingDir' => '/code',
  'Volumes' => {
    '/code' => {}
  },
  'HostConfig' => {
    'Binds' => ["#{Dir.pwd}:/code"]
  }
}

RSpec.configure do |config|
  config.before(:suite) do
    puts 'Installing RPM'
    result = command('sudo yum -y --disablerepo=updates install /code/built_rpms/RPMS/x86_64/*.rpm')
    expect(result.exit_status).to eq 0
    puts 'Making DB directory non-root owned'
    result = command('sudo mkdir -p /var/lib/centos-package-cron')
    expect(result.exit_status).to eq 0
    result = command('sudo chown nonrootuser /var/lib/centos-package-cron')
    expect(result.exit_status).to eq 0
  end

  config.before(:each) do
    puts 'Wiping clean database'
    # cleanup just in case
    command('rm -rf /var/lib/centos-package-cron/*.sqlite')
  end
end

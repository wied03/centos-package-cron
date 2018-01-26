require 'serverspec'
require 'docker'

set :backend, :docker
set :docker_image, ENV['RUN_IMAGE_TAG']
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
    puts 'Installing built RPM'
    result = command('sudo yum -y --disablerepo=updates install /code/built_rpms/RPMS/x86_64/*.rpm; yum clean all')
    puts result.stdout
    puts result.stderr
    expect(result.exit_status).to eq 0
    puts 'Making DB directory non-root owned'
    result = command('sudo mkdir -p /var/lib/centos-package-cron')
    expect(result.exit_status).to eq 0
    result = command('sudo chown nonrootuser /var/lib/centos-package-cron')
    expect(result.exit_status).to eq 0
  end

  config.before(:each) do
    # cleanup just in case
    output = command('rm -rfv /var/lib/centos-package-cron/*.sqlite').stdout
    puts "**** DB cleanup results: #{output.strip} ****"
  end

  config.filter_run_including focus: true
  config.run_all_when_everything_filtered = true
end


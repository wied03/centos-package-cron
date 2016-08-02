require 'spec_helper'

describe 'centos-package-cron installation' do
  describe file('/usr/bin/centos-package-cron') do
    it { is_expected.to be_file }
    it { is_expected.to be_executable }
  end

  describe command('centos-package-cron --help') do
    its(:stdout) { is_expected.to match /usage: centos-package-cron.* Version/m }
  end
end

require 'spec_helper'

describe 'centos-package-cron state' do
  context '2nd run' do
    before do
      result = command('centos-package-cron --output stdout')
      expect(result.exit_status).to eq 0
    end

    describe command('centos-package-cron --output stdout') do
      its(:exit_status) { should eq 0 }
      its(:stdout) { is_expected.to_not match /The following security advisories exist.*/m }
    end
  end
end

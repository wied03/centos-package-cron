require 'spec_helper'

describe 'centos-package-cron output' do
  describe command('centos-package-cron --output stdout') do
    its(:exit_status) { should eq 0 }
    its(:stdout) { is_expected.to match /The following security advisories exist.*/m }
  end

  describe 'file output' do
    before do
      result = command('centos-package-cron --output stdout > some_file.txt')
      expect(result.exit_status).to eq 0
    end

    describe file('/code/some_file.txt') do
      its(:content) { is_expected.to match /The following security advisories exist.*/m }
    end
  end
end

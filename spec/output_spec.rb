require 'spec_helper'

describe 'centos-package-cron output' do
  describe command('centos-package-cron --output stdout') do
    its(:exit_status) { should eq 0 }
    its(:stdout) { is_expected.to match /The following security advisories exist.*/m }
  end

  describe 'file output' do
    let(:filename) { 'some_file.txt' }

    around do |example|
      FileUtils.rm_rf filename
      example.run
      FileUtils.rm_rf filename
    end

    before do
      result = command("centos-package-cron --output stdout > #{filename}")
      expect(result.exit_status).to eq 0
      expect(result.stdout).to be_empty
      expect(result.stderr).to be_empty
    end

    describe file('/code/some_file.txt') do
      its(:content) { is_expected.to match /The following security advisories exist.*/m }
    end
  end
end

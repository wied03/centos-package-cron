require 'spec_helper'

describe 'centos-package-cron output' do
  context 'plaintext' do
    let(:centos_cmd) { command('centos-package-cron --output stdout') }

    context 'updates available' do
      it 'returns proper output' do
        expect(centos_cmd.exit_status).to eq 1
        expect(centos_cmd.stdout).to match /The following security advisories exist.*/m
        expect(centos_cmd.stderr).to eq 'One or more packages is out of date'
      end
    end

    context 'no updates available' do
      before do
        expect(command('yum update -y').exit_status).to eq 0
      end

      it 'returns proper output' do
        expect(centos_cmd.exit_status).to eq 0
        expect(centos_cmd.stdout).to eq ''
        expect(centos_cmd.stderr).to eq 'All packages are up to date'
      end
    end if ENV['TEST_NO_UPDATES']

    context 'file redirect' do
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
end

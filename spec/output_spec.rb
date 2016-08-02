require 'spec_helper'

describe 'centos-package-cron output' do
  context 'stdout' do
    let(:centos_cmd) { command('centos-package-cron --output stdout') }

    it 'returns proper output' do
      expect(centos_cmd.exit_status).to eq 0
      expect(centos_cmd.stdout).to match /The following security advisories exist.*/m
    end
  end

  context 'file output' do
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

  context 'email' do
    let(:centos_cmd) { command('centos-package-cron --output email') }

    if ENV['NO_EMAIL']
      it 'fails correctly' do
        expect(centos_cmd.exit_status).to eq 1
        expect(centos_cmd.stderr).to match /.*Connection refused.*/m
      end
    else
      fit 'runs correctly' do
        expect(centos_cmd.exit_status).to eq 0
        expect(centos_cmd.stdout).to eq 'no output'
        expect(file('/var/mail/spool/root'))
      end
    end
  end
end

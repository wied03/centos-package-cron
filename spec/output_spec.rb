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

    before do
      cmd = command('sudo /usr/libexec/postfix/aliasesdb; sudo /usr/libexec/postfix/chroot-update; sudo /usr/sbin/postfix start')
       begin
        expect(cmd.exit_status).to eq 0
       ensure
        puts cmd.stdout
        puts cmd.stderr
       end
    end

    it 'emails correctly' do
      expect(centos_cmd.exit_status).to eq 0
      expect(centos_cmd.stdout).to_not match /The following security advisories exist.*/m
      expect(command('sudo cat /var/spool/mail/root').stdout).to match /.*Subject: CentOS Update Check.*/m
    end
  end
end

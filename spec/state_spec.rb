require 'spec_helper'

describe 'centos-package-cron state' do
  context '2nd run' do
    before do
      result = command('centos-package-cron --output stdout')
      expect(result.exit_status).to eq 0
    end

    context 'default' do
      let(:centos_cmd) { command('centos-package-cron --output stdout') }

      it 'returns proper output' do
        expect(centos_cmd.exit_status).to eq 0
        expect(centos_cmd.stdout).to_not match /The following security advisories exist.*/m
      end
    end

    context 'force old' do
      let(:centos_cmd) { command('centos-package-cron --output stdout --forceold') }

      it 'returns proper output' do
        expect(centos_cmd.exit_status).to eq 0
        expect(centos_cmd.stdout).to match /The following security advisories exist.*/m
      end
    end
  end
end

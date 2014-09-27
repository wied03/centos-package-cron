import subprocess

class MockableExecute:
	def run_command(self,command):
		proc = subprocess.Popen(command, stdout=subprocess.PIPE)
		out = proc.communicate()[0]
		return out
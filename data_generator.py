import subprocess
exe_path = '/Users/chanita/projects/pronto/fail2stats_vagrant/ban2stats/client/webservice_client.py'
ip = '72.14.207.100'


def attack(ip, service_name):
    command_arguments = [exe_path,  service_name, "https", "81", ip]
    process = subprocess.Popen(command_arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if exit_code > 0:
        result = 'error.'
        command_output = err
    else:
        result = 'success.'
        command_output = output
    print result, command_output

for i in range(172,190):
    ip = '114.82.{0}.3'.format(i)
    attack(ip, 'Evil Service')

for i in range(2,190):
    ip = '114.{0}.19.3'.format(i)
    attack(ip, 'Company Portal')

for i in range(33, 40):
    ip = '114.48.19.{0}'.format(i)
    attack(ip, 'Human Resource Control Portal')

for i in range(20, 133):
    ip = '114.48.20.{0}'.format( i)
    attack(ip, 'Financial Department Portal')
for i in range(80, 133):

    ip = '114.48.20.{0}'.format( i)
    attack(ip, 'Financial Department Portal')
for i in range(123, 133):
    ip = '114.48.20.{0}'.format( i)
    attack(ip, 'Financial Department Portal')
for i in range(12, 40):
    ip = '114.109.188.{0}'.format( i)
    attack(ip, 'Financial Department Portal')
for i in range(12, 99):
    ip = '72.14.20.{0}'.format( i)
    attack(ip, 'Financial Department Portal')
for i in range(12, 99):
    ip = '72.14.12.{0}'.format( i)
    attack(ip, 'Human Resource Control Portal')

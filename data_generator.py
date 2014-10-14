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



# import time
# if not AttackedService.exists():
#     AttackedService.create_table()
#     time.sleep(settings.TESTING_SLEEP_TIME)
# item1 = AttackedService(key="Internal Wordpress System", count=32923)
# item1.save()
# item1_1 = AttackedService(key="Mail Server", count=300)
# item1_1.save()
# item1_2 = AttackedService(key="Company Secured Server", count=127563)
# item1_2.save()
#
# if not BlockedIP.exists():
#     time.sleep(settings.TESTING_SLEEP_TIME)
#     BlockedIP.create_table()
# item2 = BlockedIP("blocked_ip_72.14.207.99",
#                        key="72.14.20.99",
#                        service_name='Company Wordpress System',
#                        protocol='http',
#                        port='80',
#
#                        longitude=-122.05740356445312,
#                        latitude=37.419200897216797,
#                        country='US',
#                        geo_location='CA, United States',
#
#                        count=1000,
#                        last_seen='2014-09-27T08:49:28.556775+0000'
#                        )
# item2.save()
#
# item1.delete()
# item1_1.delete()
# item1_2.delete()
# item2.delete()
#
# if not BlockedCountry.exists():
#     BlockedCountry.create_table()
# time.sleep(settings.TESTING_SLEEP_TIME)
# item1 = BlockedCountry("blocked_country", key='US', country_name='United States', count=22)
# item1.save()
# item2 = BlockedCountry("blocked_country", key='TH', country_name='Thailand', count=3000)
# item2.save()
# item3 = BlockedCountry("blocked_country", key='SG', country_name='Singapore', count=12094)
# item3.save()
# item4 = BlockedCountry("blocked_country", key='AL', country_name='Albania', count=3)
# item4.save()
# item5 = BlockedCountry("blocked_country", key='MA', country_name='Morocco', count=34123)
# item5.save()
# item6 = BlockedCountry("blocked_country", key='PE', country_name='Peru', count=50)
# item6.save()
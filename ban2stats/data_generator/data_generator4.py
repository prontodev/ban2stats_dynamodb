from ban2stats.data_generator.data_generator import attack

for i in range(83, 133):
    ip = '114.48.20.{0}'.format( i)
    attack(ip, 'Financial Department Portal')

for i in range(12, 140):
    ip = '114.109.188.{0}'.format(i)
    attack(ip, 'Financial Department Portal')
for i in range(32, 109):
    ip = '13.14.20.{0}'.format(i)
    attack(ip, 'Financial Department Portal')
for i in range(2, 179):
    ip = '14.14.12.{0}'.format(i)
    attack(ip, 'Human Resource Control Portal')

for i in range(12, 240):
    ip = '114.109.{0}.4'.format(i)
    attack(ip, 'Financial Department Portal')
    for j in range(32, 109):
        ip = '72.90.20.{0}'.format(i)
        attack(ip, 'Financial Department Portal')
        for k in range(2, 179):
            ip = '{2}.{1}.1.{0}'.format(i, j, k)
            attack(ip, 'Human Resource Control Portal')
            for l in range(2,243):
                ip = '{0}.{1}.{2}.{3}'.format(k,j,l,i)
                attack(ip, 'Magic Department')


for i in range(172,210):
    for j in range(2,220):
        for k in range(2,220):
            for l in range(1, 248):
                ip = '{0}.{1}.{2}.{3}'.format(i,j,k,l)
                attack(ip, 'Evil Service')

            ip = '114.{0}.{1}.{2}'.format(i,j,k)
            attack(ip, 'Company Portal')

        ip = '{3}.{1}.{2}.{0}'.format(i,j,k)
        attack(ip, 'Human Resource Control Portal')

        ip = '114.{j}.20.{0}'.format(i,j)
        attack(ip, 'Financial Department Portal')

    for j in range(40, 233):
        ip = '114.48.{1}.{0}'.format(i,j)
        attack(ip, 'Financial Department Portal')

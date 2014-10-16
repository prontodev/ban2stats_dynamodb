from data_generator import attack
for i in range(3,210):
    for j in range(2,220):
        for k in range(2,220):
            for l in range(1, 248):
                ip = '{3}.{1}.{2}.{0}'.format(i,j,k,l)
                attack(ip, 'Human Resource Control Portal')
        #         ip = '{0}.{1}.{2}.{3}'.format(i,j,k,l)
        #         attack(ip, 'Evil Service')
        #
        #     ip = '114.{0}.{1}.{2}'.format(i,j,k)
        #     attack(ip, 'Company Portal')
        #
        #
        #
        # ip = '{1}.{2}.20.{0}'.format(i,j,k)
        # attack(ip, 'Financial Department Portal')
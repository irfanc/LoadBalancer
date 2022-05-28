from balancer import balancer

if __name__ == '__main__':
    # balancer = Balancer()
    S = balancer.get_server('Maths')
    S.ping()

    balancer.get_list_of_servers()
    print("1")
    balancer.health_check()
    print("2")
    balancer.health_check()
    print("3")
    balancer.health_check()


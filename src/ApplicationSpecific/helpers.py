
def rtt(netModel):
    rtt = 0

    clients = netModel.get_clients()
    for i in range(len(clients)):
        for adj in clients[i].get_all_adj():
            try:
                if adj[0] == clients[i+1]:
                    rtt += adj[1].get_latencia()
            except:
                pass
            
    return rtt*2
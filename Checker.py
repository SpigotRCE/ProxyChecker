import os
import socket
import threading

print("Proxy checker made by @spigotrce on discord and youtube =)")


def check_proxy(proxy, online_proxies, offline_proxies):
    try:
        proxy_ip, proxy_port = proxy.split(':')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)  # Adjust the timeout as needed
        s.connect((proxy_ip, int(proxy_port)))
        print(f"Proxy {proxy} is online.")
        online_proxies.append(proxy)
        s.close()
    except Exception as e:
        offline_proxies.append(proxy)


def main():
    proxy_file = input("Enter the path to the file containing SOCKS4 proxies: ")

    if not os.path.exists(proxy_file):
        print("File not found.")
        return

    try:
        with open(proxy_file, 'r') as f:
            proxy_list = f.read().splitlines()
    except FileNotFoundError:
        print("File not found.")
        return

    online_proxies = []
    offline_proxies = []

    threads = []

    for proxy in proxy_list:
        t = threading.Thread(target=check_proxy, args=(proxy, online_proxies, offline_proxies))
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Save online proxies to a file
    with open("online_proxies.txt", 'w') as f:
        for proxy in online_proxies:
            f.write(proxy + '\n')

    # Save offline proxies to a file
    with open("offline_proxies.txt", 'w') as f:
        for proxy in offline_proxies:
            f.write(proxy + '\n')


if __name__ == "__main__":
    main()

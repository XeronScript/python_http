import http.client


def send_get_request(host, port):
    conn = http.client.HTTPConnection(host, port)
    conn.request('GET', '/')
    response = conn.getresponse()
    print("Response status: ", response.status)
    print("Response body: ", response.read().decode('utf-8'))


if __name__ == '__main__':
    host = 'localhost'
    port = 8000

    # Send get request
    print('Sending GET request...')
    send_get_request(host, port)

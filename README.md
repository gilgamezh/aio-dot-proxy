# aio-dot-proxy

## DNS-over-TLS Proxy 


After some tests with sockets I decided to implement it with the high level API of Asyncio. 
It’s really simple, the code is easy to read and it allows the proxy to manage multiple connections. 

As I only have to proxy the requests I’m not doing any parsing of the queries. The server is just proxying the data without any intervention. 
To implement a cache or other feature it could be needed. (and for debug) 


### What are the security concerns for this kind of service?

From the client side I assume it’s an internal service not exposed to the internet. DoS attack or Man-in-the-middle would be a really weird situation.

My security concerns will be particularly with the identity of the backend server. 
The proxy could implement extra validations and execute them periodically. 
Of course the CA certificates installed on the server should be audited. 

### Considering a microservice architecture; how would you see this the dns to dns-over-tls proxy used?

It can be implemented to run on every node as a local proxy-cache server.

### What other improvements do you think would be interesting to add to the project? 

My approach was really simple so I think there are lot of improvements: 

- Error handling.
- It's currently reconnecting for every query. Connection reuse it’s asked in the RFC (to pipeline queries). The server could use a pool of connections. As the responses are not guaranteed to be ordered It will need to parse the queries and responses to use de Message ID to identify which response is for which client
- Caching (expiring it using the TTL). 
- A health check endpoint.
- An endpoint to publish stats/metrics 


## How to run it. 

- a `Dockerfile` is provided. Build it running

    `docker build . -t aio-dot-proxy:test`

- After the build just run the image with: 

    `docker run -p 127.0.0.2:53:8853 -p 127.0.0.2:53:9953/udp aio-dot-proxy:test`

- Test it using `dig`

    ``` 
    ~  dig @127.0.0.2  gilgamezh.me +short +tcp  # TCP
        185.199.110.153
        185.199.111.153
        185.199.108.153
        185.199.109.153
    
    ~  dig @127.0.0.2  gilgamezh.me +short  # UDP
        185.199.110.153
        185.199.111.153
        185.199.108.153
        185.199.109.153
    ```

## Configuration 

The default settings are using cloudflare DNS-over-TLS servers. You can override it running

    `docker run -p 127.0.0.2:53:8888 aio-dot-proxy:test --backend-hostname dns.quad9.net --backend-port 853`



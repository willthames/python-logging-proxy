# Logging HTTP Proxy

Proxy that logs full HTTP request and response. Obviously things
like Fiddler etc exist and are very good, but this is really for
seeing what's going wrong when making API calls from a client.

To use, run `./proxy.py` (takes an optional port argument).

From the client side, set the proxy using 
`export HTTP_PROXY=http://localhost:8000`
(assuming default port). 

You'll get something like this:

```
*** REQUEST ***
GET http://bot.whatismyipaddress.com/
Host = bot.whatismyipaddress.com
Proxy-Connection = Keep-Alive
Accept = */*
User-Agent = curl/7.30.0

*** END REQUEST ***
*** RESPONSE ***
200 OK
Content-Length = 14
X-Powered-By = PHP/5.3.28
Vary = Accept-Encoding
Keep-Alive = timeout=15, max=100
Ms-Author-Via = DAV
Server = Apache/2.2.26 (Unix) DAV/2 PHP/5.3.28 mod_ssl/2.2.26 OpenSSL/0.9.8za
Connection = Keep-Alive
Date = Sat, 13 Dec 2014 08:31:42 GMT
Content-Type = text/html

122.149.212.59
*** END RESPONSE ***
```

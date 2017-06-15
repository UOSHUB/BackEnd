# Blackboard Scraping Package

This module contains an unofficial api (through web scraping) to allow interaction with UOS Blackboard system.  
it's using python3-requests library to get and post data, and using lxml scrape the needed information.

***

### Why not use the official Blackboard APIs?

Even though Blackboard has two types of APIs, our university system does not have any of them!


##### REST API (JSON):
It's the better option between the two, it's simple, well documented and new (introduced in Q2 2016).  
But because it's new, it's not available in our university's Blackboard as they're still using October 2014 version.

Blackboard REST API documentation can be found here:  
https://developer.blackboard.com/portal/displayApi


##### SOAP API (XML):
This is the older (almost obsolete), less elegant and very poorly documented option.  
Blackboard has this API since a while, it should be supported by our university's system,  
but it does not seem to be the case.


When using the official way of initializing SOAP requests, it returns a `500 Internal Server Error`:

```
from suds.client import Client
Client("https://elearning.sharjah.ac.ae/webapps/ws/services/Context.WS?wsdl", autoblend=True)
```

And when manually posting a proper XML request to initialize a session, it returns `java.lang.NoSuchMethodError`:

```
import requests
requests.post(
    "https://elearning.sharjah.ac.ae/webapps/ws/services/Context.WS?wsdl",
    data="""
        <env:Envelope xmlns:env="http://www.w3.org/2003/05/soap-envelope">
            <env:Header>
                <wsa:Action >initialize</wsa:Action>
                <wsse:Security>
                    <wsse:UsernameToken>
                        <wsse:Username>session</wsse:Username>
                        <wsse:Password>nosession</wsse:Password>
                    </wsse:UsernameToken>
                </wsse:Security>
            </env:Header>
        </env:Envelope>
    """
)
```

It seems that our university decided to disable this API, or not enable it in the first place!  
So the only choice that's left is to make our own API.

***

### References
- [UOS Blackboard](https://elearning.sharjah.ac.ae)
- [Requests](https://github.com/requests/requests)
- [lxml](https://github.com/lxml/lxml)
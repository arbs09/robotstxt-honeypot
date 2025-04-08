# robotstxt-honeypot

There are some Crawlers out there, wich don't respect robots.txt.
This Honeypot tries to find them and report them via some ways.

## Installation

### Docker

```yml
services:
  honeypot:
    container_name: robotstxt-honeypot
    image: ghcr.io/arbs09/robotstxt-honeypot:main
    ports:
      - 80:5000
```

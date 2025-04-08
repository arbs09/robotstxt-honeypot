# a web-honeypot

There are some Crawlers oput there, wich don't respect robots.txt.
This Honeypot tries to find them and report them via some ways.

## Installation

### Docker

```yml
services:
  honeypot:
    container_name: web-honeypot
    image: ghcr.io/arbs09/web-honeypot:main
    ports:
      - 80:5000
```

###Create rules.toml

```
[backends]
  [backends.backend-homeassistant]
    [backends.backend-homeassistant.servers]
      [backends.backend-homeassistant.servers.server-homeassistant-ext]
      url = "http://IP:8123"
      weight = 2

[frontends]
  [frontends.frontend-homeassistant]
  backend = "backend-homeassistant"
  passHostHeader = true
  InsecureSkipVerify = true
  [frontends.frontend-homeassistant.routes]
    [frontends.frontend-homeassistant.routes.route-homeassistant-ext]
    rule = "Host:HOST"
```
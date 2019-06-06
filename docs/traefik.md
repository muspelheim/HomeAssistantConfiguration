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

```
[backends]
  [backends.backend-esphome]
    [backends.backend-esphome.servers]
      [backends.backend-esphome.servers.server-esphome-ext]
      url = "http://IP:6053"
      weight = 2

[frontends]
  [frontends.frontend-esphome]
  backend = "backend-esphome"
  passHostHeader = true
  InsecureSkipVerify = true
  [frontends.frontend-esphome.routes]
    [frontends.frontend-esphome.routes.route-esphome-ext]
    rule = "Host:DOMAIN"

  [frontends.frontend-esphome.auth]
    headerField = "X-WebAuth-User"
    [frontends.frontend1.auth.basic]
      removeHeader = true
      users = [
        "user:password",
      ]

```

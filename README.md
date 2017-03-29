# Namesilo DNS updater

Dynamically update the A record of a subdomain registered at
[namesilo](https://namesilo.com).

Copy the `service` and `timer` file to `/etc/systemd/system` and edit the
service file accordingly.

```
# systemctl start dnsupdate.timer
# systemctl enable dnsupdate.timer
```

## License

Licensed under either of

* Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
* MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

at your option.
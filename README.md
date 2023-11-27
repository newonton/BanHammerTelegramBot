# Simple Telegram Ban Bot

## How to Run
Install and run
```bash
make
```
Install only
```bash
make deps
make configs
```
Run only
```bash
make run
```

## How to use
It has two commands:<br />
`/id` with reply message gets author id of the message<br />
`/ban {time} {reason}` with reply message bans author of the message

### Time format
`1m` = 1 minute<br />
`2h` = 2 hours<br />
`3d` = 3 days<br />
`4w` = 4 weeks<br />

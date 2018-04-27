# chessd
## description
**chessd** is a web api server/client, serving as a frontend for the stockfish engine. for further information on how to use the project, please refer to `/templates/static.html`

## usage example
```bash
./chesscli new > game_token
cat game_token | ./chesscli move e2e4
cat game_token | ./chesscli best
```

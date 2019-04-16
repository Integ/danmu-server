import fs from 'fs';
import Express from 'express';
import ExpressWebSocket from 'express-ws';

const POS = ['fly', 'top', 'bottom']
const COL = ['white', 'black', 'blue', 'cyan', 'red', 'yellowgreen', 'purple']

const app = new Express();
ExpressWebSocket(app);

var msgTexts = []
var wsClients = []

function socketProxy(ws, req) {
  console.log(`[DANMU-SERVER] Websocket Request: ${req.url}`)
  wsClients.push(ws)
  ws.send('INFO:OK');
  ws.on('message', function(msg) {
    console.log(`[DANMU-SERVER] New Danmu: ${msg}`)
    msgTexts.push(msg.replace(/^DANMAKU:/, ''))
    for (var i=0; i<wsClients.length; i++) {
      if(wsClients[i].readyState === 1) {
        wsClients[i].send(msg);
      }
    }
  });
}

function choice(arr) {
  var rand = Math.random()
  rand *= arr.length
  rand = Math.floor(rand)
  return arr[rand]
}

function getDanmu(req, res) {
  console.log(`[DANMU-SERVER] Http Request: ${req.url}`)
  if(msgTexts.length) {
    res.writeHeader(200, {"Content-Type": "application/json"});
    var resBody = msgTexts.map((text) => {
        return {
          'text': text,
          'style': choice(COL),
          'position': choice(POS)
        }
    })
    res.write(JSON.stringify(resBody))
    msgTexts = []
    res.end()
  }
}

app.get('/', (req, res)=> {
    fs.readFile('index.html', 'utf8', (err, text) => {
        res.send(text);
    });
})
app.get('/api/v1.1/channels/demo/danmaku', getDanmu) 
app.ws('/ws', socketProxy);

app.listen(8080, () => {
  console.log('[DANMU-SERVER] Running at port 8080');
});

const express = require("express");
const { spawn } = require("child_process");
const WebSocket = require("ws");
const http = require("http");
const path = require("path");

const app = express();
app.use(express.json());
app.use(express.static("public"));
app.use(express.static("output"));

// serve main page explicitly (static middleware will also handle it)
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

let clients = [];

wss.on("connection", (ws) => {
  clients.push(ws);
});

function sendProgress(step, percent) {
  clients.forEach(client => {
    client.send(JSON.stringify({ step, percent }));
  });
}

app.post("/generate-pcb", (req, res) => {

  const python = spawn("python", [
    "hh_enhanced.py",
    "--project-data",
    JSON.stringify(req.body),
    "--pcb-file",
    "./workspace/board.kicad_pcb"
  ]);

  let percent = 0;

  python.stdout.on("data", (data) => {
    const output = data.toString();

    // كل مرحلة KiCad نترجمها لنسبة
    if (output.includes("Preparing")) percent = 10;
    if (output.includes("Placing")) percent = 30;
    if (output.includes("Routing")) percent = 50;
    if (output.includes("Exporting Gerbers")) percent = 70;
    if (output.includes("Exporting STEP")) percent = 85;
    if (output.includes("Done")) percent = 100;

    sendProgress(output.trim(), percent);
  });

  python.stderr.on("data", (err) => {
    sendProgress("Error: " + err.toString(), 0);
  });

  python.on("close", (code) => {
    sendProgress("Completed ✅", 100);
  });

  res.json({ status: "STARTED" });
});

server.listen(3000, () => {
  console.log("🚀 Real AI PCB Server running on http://localhost:3000");
});
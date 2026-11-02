const http = require('http');
const fs = require('fs');
const path = require('path');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.xml': 'application/xml',
  '.txt': 'text/plain'
};

const server = http.createServer((req, res) => {
  let reqPath = decodeURI(req.url.split('?')[0]);
  if (reqPath === '/' || reqPath === '') reqPath = '/index.html';
  const filePath = path.join(__dirname, reqPath);

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      const notFoundPath = path.join(__dirname, '404.html');
      if (fs.existsSync(notFoundPath)) {
        res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(fs.readFileSync(notFoundPath));
      } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 Not Found');
      }
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME[ext] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': contentType });
    fs.createReadStream(filePath).pipe(res);
  });
});

const portsToTry = [8080, 5500, 5000, 4173, 8000, 0];

function startServer(index) {
  const port = portsToTry[index];
  server.removeAllListeners('error');
  server.once('error', (err) => {
    if (err.code === 'EACCES' || err.code === 'EADDRINUSE') {
      console.log(`Port ${port} unavailable, trying next...`);
      startServer(index + 1);
    } else {
      console.error(err);
    }
  });

  server.listen(port, '127.0.0.1', () => {
    const actualPort = server.address().port;
    console.log(`Local dev server is running at: http://localhost:${actualPort}`);
    console.log(`Open http://localhost:${actualPort}/index.html in your browser.`);
  });
}

startServer(0);

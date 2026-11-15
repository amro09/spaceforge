// Dependency-free local demo server. Not a production hosting server.
import http from "node:http";
import { readFile, realpath } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = await realpath(fileURLToPath(new URL("../artifacts/mission-forge/public/", import.meta.url)));
const port = Number(process.argv[2] || 8080);
const apiPort = Number(process.argv[3] || 3001);
const host = process.argv.includes("--lan") ? "0.0.0.0" : "127.0.0.1";
if (![port, apiPort].every(n => Number.isInteger(n) && n > 0 && n < 65536)) {
  throw new Error("Ports must be integers between 1 and 65535.");
}
const types = { ".html": "text/html", ".js": "text/javascript", ".json": "application/json", ".css": "text/css", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml", ".webp": "image/webp", ".woff2": "font/woff2" };
const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://localhost");
  if (url.pathname.startsWith("/api/")) {
    const upstream = http.request({ hostname: "127.0.0.1", port: apiPort, path: url.pathname + url.search, method: req.method, headers: { ...req.headers, host: `127.0.0.1:${apiPort}` } }, response => {
      res.writeHead(response.statusCode, response.headers);
      response.pipe(res);
    });
    upstream.on("error", () => {
      if (!res.headersSent) res.writeHead(502, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Online play needs the API server. Follow the README online setup." }));
    });
    upstream.setTimeout(15000, () => upstream.destroy());
    req.pipe(upstream);
    return;
  }
  if (!["GET", "HEAD"].includes(req.method)) { res.writeHead(405); res.end(); return; }
  try {
    const target = await realpath(path.resolve(root, "." + decodeURIComponent(url.pathname === "/" ? "/mission-forge.html" : url.pathname)));
    if (!target.startsWith(root + path.sep)) { res.writeHead(403); res.end(); return; }
    const data = await readFile(target);
    res.writeHead(200, { "Content-Type": types[path.extname(target)] || "application/octet-stream", "Cache-Control": "no-store" });
    res.end(req.method === "HEAD" ? undefined : data);
  } catch { res.writeHead(404); res.end("Not found"); }
});
server.listen(port, host, () => console.log(`Mission Forge: http://localhost:${port}\nOnline API target: 127.0.0.1:${apiPort}\nPress Ctrl+C to stop.${host === "0.0.0.0" ? "\nLAN access enabled. Use only on a trusted network." : ""}`));

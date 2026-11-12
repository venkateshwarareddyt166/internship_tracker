import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

db = sqlite3.connect("internships.db")
db.execute("CREATE TABLE IF NOT EXISTS jobs(id INTEGER PRIMARY KEY,company TEXT,role TEXT,status TEXT)")
db.commit()

class App(BaseHTTPRequestHandler):
 def do_GET(self):
  rows=db.execute("SELECT * FROM jobs ORDER BY id DESC").fetchall()
  html="""<html>
  <head>
  <title>Internship Tracker</title>
  <style>
  body{font-family:Arial;background:linear-gradient(120deg,#667eea,#764ba2);padding:30px;color:#333}
  .box{background:white;padding:25px;border-radius:18px;max-width:750px;margin:auto;box-shadow:0 5px 20px #3335}
  h1{text-align:center;color:#7048c8}
  input,select,button{padding:12px;margin:7px;border:1px solid #ddd;border-radius:8px}
  input{width:38%}button{background:#7048c8;color:white;border:0;cursor:pointer}
  .job{background:#f1edff;padding:15px;margin:12px 0;border-left:5px solid #805ad5;border-radius:10px}
  .status{color:#7048c8;font-weight:bold}
  </style>
  </head>
  <body><div class='box'>
  <h1>Internship Tracker</h1>
  <h3>Add New Application</h3>
  <form method='POST'><input name='company' placeholder='Company Name' required>
  <input name='role' placeholder='Job Role' required>
  <button>Add Application</button>
  </form>
  <hr>
  <h3>Application History</h3>"""
  for i,c,r,s in rows:
   html+=f"""<div class='job'><b> {c}</b> | {r}<br>
   <p class='status'>Status: {s}</p><form method='POST'>
   <input type='hidden' name='id' value='{i}'>
   <select name='status'><option>Applied</option><option>Interview</option>
   <option>Selected</option><option>Rejected</option></select>
   <button>Update Status</button></form></div>"""
  html+="</div></body></html>"
  self.send_response(200);self.send_header("Content-type","text/html");self.end_headers();self.wfile.write(html.encode())

 def do_POST(self):
  d=parse_qs(self.rfile.read(int(self.headers['Content-Length'])).decode())
  if 'id' in d:
   db.execute("UPDATE jobs SET status=? WHERE id=?",(d['status'][0],d['id'][0]))
  else:
   db.execute("INSERT INTO jobs(company,role,status) VALUES(?,?,?)",(d['company'][0],d['role'][0],"Applied"))
  db.commit();self.send_response(303);self.send_header("Location","/");self.end_headers()

print("Open http://localhost:8000")
HTTPServer(("localhost",8000),App).serve_forever()
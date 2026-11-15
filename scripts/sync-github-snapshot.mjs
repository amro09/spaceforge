// Safe snapshot synchronization for this repository's separate GitHub history.
// Requires an explicitly reviewed remote parent. Never force-pushes or deletes remote-only files.
import {ReplitConnectors} from "@replit/connectors-sdk";
import {readFileSync,writeFileSync,lstatSync} from "node:fs";
import {execFileSync} from "node:child_process";
import {createHash} from "node:crypto";
const expected=process.argv[2];
if(!/^[a-f0-9]{40}$/.test(expected||""))throw Error("Pass the reviewed remote parent SHA.");
const c=new ReplitConnectors(),root="/repos/MahmoudFarah003/spaceforge";
async function api(path,method="GET",body){
  const response=await c.proxy("github",root+path,{method,headers:{"Content-Type":"application/json"},...(body?{body:JSON.stringify(body)}:{})});
  const result=await response.json();if(!response.ok)throw Error(`${method} ${path}: ${response.status} ${result.message}`);return result;
}
const ref=await api("/git/ref/heads/main");
if(ref.object.sha!==expected)throw Error("GitHub changed. Stop and merge the newer remote changes first.");
const parent=await api("/git/commits/"+expected),base=await api("/git/trees/"+parent.tree.sha+"?recursive=1");
if(base.truncated)throw Error("Cannot safely compare truncated tree.");
const remote=new Map(base.tree.map(f=>[f.path,f.sha]));
const paths=execFileSync("git",["ls-files","--cached","--others","--exclude-standard","-z"],{encoding:"utf8"}).split("\0").filter(Boolean);
const files=[...new Set(paths)].filter(p=>!/^(\.agents|\.local|generated-artifacts|node_modules)\//.test(p)&&!/(^|\/)\.env($|\.)|\.(pem|key)$/.test(p));
const changes=[],checks=[];
for(const path of files){
  if(!lstatSync(path).isFile())continue;
  const data=readFileSync(path),sha=createHash("sha1").update(`blob ${data.length}\0`).update(data).digest("hex");
  if(remote.get(path)===sha)continue;
  if(data.length>8*1024*1024)throw Error("Review large file before upload: "+path);
  const text=data.toString("utf8"),isText=Buffer.from(text).equals(data)&&!data.includes(0);
  if(isText&&/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}/.test(text))throw Error("Potential credential in "+path);
  const mode=(lstatSync(path).mode&0o111)?"100755":"100644";
  if(isText)changes.push({path,mode,type:"blob",content:text});
  else{const blob=await api("/git/blobs","POST",{content:data.toString("base64"),encoding:"base64"});if(blob.sha!==sha)throw Error("Blob verification failed");changes.push({path,mode,type:"blob",sha});}
  checks.push({path,sha});
}
if(!changes.length){console.log("Remote already matches.");process.exit(0);}
const tree=await api("/git/trees","POST",{base_tree:parent.tree.sha,tree:changes});
const commit=await api("/git/commits","POST",{message:process.argv[3] || "Synchronize reviewed Mission Forge project updates",tree:tree.sha,parents:[expected]});
if((await api("/git/ref/heads/main")).object.sha!==expected)throw Error("Remote advanced during upload. Branch was not modified.");
await api("/git/refs/heads/main","PATCH",{sha:commit.sha,force:false});
const verified=await api("/git/trees/"+tree.sha+"?recursive=1");
const actual=new Map(verified.tree.map(f=>[f.path,f.sha]));
for(const f of checks)if(actual.get(f.path)!==f.sha)throw Error("Verification failed for "+f.path);
writeFileSync(".local/github-sync.json",JSON.stringify({repository:"MahmoudFarah003/spaceforge",lastIntegratedRemoteCommit:commit.sha,method:"Verified non-force snapshot update; remote-only files retained."},null,2));
console.log(JSON.stringify({commit:commit.sha,url:commit.html_url,files:checks.length,verified:true}));

import assert from "node:assert/strict";
const url = `https://${process.env.REPLIT_DEV_DOMAIN}/api/coop`;
async function call(body, status=200) {
  const response=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
  const result=await response.json();
  assert.equal(response.status,status,JSON.stringify(result));
  return result;
}
for(const size of [2,3,4]){
  const h=await call({action:"create",name:"Test host",size,level:1,goal:"air"});
  const code=h.room.code, crew=[h];
  try{
    for(let i=1;i<size;i++)crew.push(await call({action:"join",code,name:`Crew ${i+1}`}));
    await call({action:"join",code,name:"Extra"},409);
    await call({action:"poll",code,token:"invalid"},403);
    await call({action:"start",code,token:crew[1].token},403);
    await call({action:"start",code,token:h.token},409);
    for(const p of crew)await call({action:"ready",code,token:p.token});
    await call({action:"start",code,token:h.token});
    await call({action:"settings",code,token:h.token,size,level:1,goal:"air"},409);
    await call({action:"command",code,token:crew[1].token,command:"pickPower",value:"solar"},403);
    const command=await call({action:"command",code,token:h.token,command:"pickPower",value:"solar"});
    assert.equal(command.room.commands.length,1);
    const design={mission:"earth",goal:"air",instruments:[],rocket:null,power:"solar",comms:null,orbit:null};
    const flight={screen:"mission",levelId:1,design,selectionReady:true,mission:{seg:1},dialog:{type:"event",id:"solarStorm"},result:null};
    await call({action:"snapshot",code,token:crew[1].token,snapshot:flight},403);
    await call({action:"snapshot",code,token:h.token,snapshot:flight,ack:command.room.commands[0].id});
    await call({action:"command",code,token:h.token,command:"option",value:"1",event:"1:solarStorm"},403);
    await call({action:"command",code,token:crew[1].token,command:"option",value:"1",event:"1:solarStorm"});
    await call({action:"command",code,token:crew[1].token,command:"option",value:"1",event:"1:solarStorm"},409);
    const guest=await call({action:"poll",code,token:crew[1].token});
    assert.equal(guest.room.commands.length,0);
    assert.ok(guest.room.players.every(p=>!("token" in p)));
    assert.equal(guest.room.snapshot.dialog.id,"solarStorm");
    console.log(`${size}-player room passed: capacity, auth, ready, roles, snapshots, event ownership, duplicate rejection.`);
  }finally{await call({action:"leave",code,token:h.token});}
  await call({action:"poll",code,token:h.token},404);
}

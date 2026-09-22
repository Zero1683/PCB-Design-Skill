// Pure constraint evaluator. Serializable for the Gateway runtime; no filesystem or EDA writes.
export function checkConstraints(snapshot, contract) {
  const fail = message => {throw Error('CONSTRAINT: '+message);};
  const keys=(obj,allowed)=>{if(!obj||typeof obj!=='object'||Array.isArray(obj))fail('Expected object');for(const k of Object.keys(obj))if(!allowed.includes(k))fail('Unsupported field '+k);};
  const text=v=>{if(typeof v!=='string'||!v.trim())fail('Missing identity/source');return v;};
  const number=v=>{if(typeof v!=='number'||!Number.isFinite(v))fail('Invalid number');return v;};
  const rect=v=>{if(!Array.isArray(v)||v.length!==4)fail('Expected rectangle');v.forEach(number);if(v[2]<v[0]||v[3]<v[1])fail('Reversed rectangle');return v;};
  const inside=(a,b)=>a[0]>=b[0]&&a[1]>=b[1]&&a[2]<=b[2]&&a[3]<=b[3];
  keys(contract,['schema','revision','domain','projectId','documentId','units','axis','source','bounds','rules']);
  if(contract.schema!==1||!['schematic','pcb'].includes(contract.domain))fail('Unsupported schema/domain');
  for(const k of ['revision','projectId','documentId','units','axis','source'])text(contract[k]);
  if(contract.axis!=='y-up'||contract.units!==(contract.domain==='pcb'?'mm':'raw-0.01inch'))fail('Unsupported units/axis');
  for(const k of ['projectId','documentId','units','axis'])if(contract[k]!==snapshot[k])fail('Identity/units mismatch: '+k);
  const native=Array.isArray(snapshot.components)&&snapshot.units==='raw-0.01inch';
  if((native?'schematic':snapshot.domain)!==contract.domain)fail('Domain mismatch');
  if(!native&&(snapshot.schema!==1||snapshot.coverage!=='complete'))fail('Explicit complete geometry required');
  const objects=native?snapshot.components.filter(c=>c.props.ComponentType==='part').map(c=>({id:c.id,anchor:[c.props.X,c.props.Y],rotation:c.props.Rotation,side:'schematic',bbox:c.bbox})):snapshot.objects;
  if(!Array.isArray(objects)||!objects.length)fail('Missing object inventory');
  const byId=new Map();
  for(const o of objects){text(o.id);if(byId.has(o.id))fail('Duplicate object ID');rect(o.bbox);if(!Array.isArray(o.anchor)||o.anchor.length!==2)fail('Missing anchor');o.anchor.forEach(number);number(o.rotation);text(o.side);byId.set(o.id,o);}
  rect(contract.bounds);if(!Array.isArray(contract.rules))fail('Missing rules');
  const violations=[];const add=(code,id,expected,actual)=>violations.push({code,id,expected,actual});
  for(const o of objects)if(!inside(o.bbox,contract.bounds))add('BOARD_OR_PAGE_BOUNDS',o.id,contract.bounds,o.bbox);
  for(const rule of contract.rules){
    keys(rule,['type','ids','source','anchor','rotation','side','box','gap','max']);text(rule.source);
    if(!['lock','region','keepout','height'].includes(rule.type))fail('Unsupported rule');
    if(rule.ids!=='*'&&(!Array.isArray(rule.ids)||!rule.ids.length||new Set(rule.ids).size!==rule.ids.length))fail('Invalid rule IDs');
    const selected=rule.ids==='*'?objects:rule.ids.map(id=>{if(!byId.has(id))fail('Unknown object '+id);return byId.get(id);});
    const fields={lock:['anchor','rotation','side'],region:['box'],keepout:['box','gap'],height:['max']}[rule.type];
    for(const k of Object.keys(rule))if(!['type','ids','source',...fields].includes(k))fail('Unexpected rule field '+k);
    if(rule.type==='lock'){
      if(!Array.isArray(rule.anchor)||rule.anchor.length!==2)fail('Lock requires anchor');rule.anchor.forEach(number);number(rule.rotation);text(rule.side);
      for(const o of selected)if(o.anchor.some((v,i)=>v!==rule.anchor[i])||o.rotation!==rule.rotation||o.side!==rule.side)add('LOCKED_PLACEMENT',o.id,{anchor:rule.anchor,rotation:rule.rotation,side:rule.side},{anchor:o.anchor,rotation:o.rotation,side:o.side});
    }else if(rule.type==='region'){
      rect(rule.box);for(const o of selected)if(!inside(o.bbox,rule.box))add('ALLOWED_REGION',o.id,rule.box,o.bbox);
    }else if(rule.type==='keepout'){
      const b=rect(rule.box),gap=number(rule.gap);if(gap<0)fail('Negative clearance');
      for(const o of selected){const a=o.bbox;if(a[0]<b[2]+gap&&b[0]<a[2]+gap&&a[1]<b[3]+gap&&b[1]<a[3]+gap)add('KEEPOUT',o.id,{box:b,gap},a);}
    }else{
      if(contract.domain!=='pcb'||number(rule.max)<0)fail('Height requires PCB mm geometry');
      for(const o of selected)if(typeof o.height!=='number'||!Number.isFinite(o.height)||o.height<0)add('HEIGHT_UNKNOWN',o.id,rule.max,null);else if(o.height>rule.max)add('HEIGHT_LIMIT',o.id,rule.max,o.height);
    }
  }
  return {requirementCoverage:'NOT_ASSESSED',scope:'supplied rules only',state:violations.length?'BLOCKED':'PASS',revision:contract.revision,domain:contract.domain,checked:objects.length,violations};
}

// Serialized into the selected Gateway window. All mutation paths are typed and scoped.
export async function liveRuntime(eda, input) {
  const root = globalThis.__pcbSkillLive16 ??= {busy:false, operations:Object.create(null)};
  const norm = v => v === undefined ? null : v === null || typeof v !== 'object' ? v
    : Array.isArray(v) ? v.map(norm) : Object.fromEntries(Object.keys(v).sort().map(k=>[k,norm(v[k])]));
  const same = (a,b) => JSON.stringify(norm(a)) === JSON.stringify(norm(b));
  const clone = a => JSON.parse(JSON.stringify(a));
  const finite = n => { if(typeof n !== 'number' || !Number.isFinite(n)) throw Error('Invalid coordinate'); return n; };
  const round = n => Math.round(n*1e6)/1e6;
  const componentFields = 'PrimitiveId ComponentType X Y Rotation Mirror AddIntoBom AddIntoPcb Component Symbol Footprint Designator Name UniqueId SubPartName Manufacturer ManufacturerId Supplier SupplierId OtherProperty Net'.split(' ');
  const pinFields = 'PinNumber PinName NoConnected PinLength PinShape Rotation X Y OtherProperty'.split(' ');
  const attrFields = 'PrimitiveId ParentPrimitiveId Key Value KeyVisible ValueVisible X Y Rotation AlignMode FontName FontSize Bold Italic UnderLine Color FillColor'.split(' ');
  function fields(obj, names) {
    return Object.fromEntries(names.map(k=>{
      if(typeof obj['getState_'+k] !== 'function') throw Error('Unsupported getter: '+k);
      return [k,norm(obj['getState_'+k]())];
    }));
  }
  function movement(props,x,y) {
    const out={};
    for(const key of 'X Y Rotation Mirror AddIntoBom AddIntoPcb Designator Name UniqueId Manufacturer ManufacturerId Supplier SupplierId OtherProperty'.split(' '))
      out[key[0].toLowerCase()+key.slice(1)]=clone(props[key]);
    out.x=x;out.y=y;return out;
  }
  async function identity() {
    const d=await eda.dmt_SelectControl.getCurrentDocumentInfo();
    if(!d || d.documentType!==1 || !d.uuid || !d.parentProjectUuid) throw Error('Select a schematic page');
    if(d.uuid!==input.documentId || d.parentProjectUuid!==input.projectId) throw Error('TARGET_CHANGED');
    return d;
  }
  function bbox(b) {
    if(!b) throw Error('Missing native bbox');
    const out=[b.minX,b.minY,b.maxX,b.maxY].map(finite);
    if(out[2]<out[0] || out[3]<out[1]) throw Error('Degenerate bbox');
    return out;
  }
  async function capture() {
    await identity();
    const parts=await eda.sch_PrimitiveComponent.getAll(undefined,false);
    const attrs=await eda.sch_PrimitiveAttribute.getAll();
    const components=[];
    for(const c of parts) {
      const props=fields(c,componentFields), id=props.PrimitiveId;
      const own=attrs.filter(a=>a.getState_ParentPrimitiveId()===id).map(a=>fields(a,attrFields));
      const visible=own.filter(a=>a.KeyVisible===true||a.ValueVisible===true).map(a=>a.PrimitiveId);
      const box=bbox(await eda.sch_Primitive.getPrimitivesBBox([id,...visible]));
      const pins=props.ComponentType==='part' ? await c.getAllPins() : [];
      if(!Array.isArray(pins)) throw Error('Missing native pins');
      const local=pins.map(p=>fields(p,pinFields));
      for(const item of [...own,...local]) for(const k of ['X','Y']) {
        if(item[k]!==null) item[k]=round(finite(item[k])-finite(props[k]));
      }
      own.sort((a,b)=>a.PrimitiveId.localeCompare(b.PrimitiveId));
      local.sort((a,b)=>JSON.stringify(a).localeCompare(JSON.stringify(b)));
      components.push({id,props,bbox:box,pins:local,attributes:own});
    }
    components.sort((a,b)=>a.id.localeCompare(b.id));
    const graphics=[];
    // Fixed graphics are obstacles. Getter names are state-only API accessors.
    for(const kind of ['Arc','Circle','Polygon','Rectangle','Text','Object','Pin']) {
      const api=eda['sch_Primitive'+kind];
      if(typeof api?.getAll!=='function') throw Error('Unsupported primitive inventory: '+kind);
      for(const obj of await api.getAll()) {
        const names=new Set();
        for(let p=obj;p&&p!==Object.prototype;p=Object.getPrototypeOf(p))
          for(const name of Object.getOwnPropertyNames(p)) if(name.startsWith('getState_')&&typeof obj[name]==='function') names.add(name.slice(9));
        const props=fields(obj,[...names].sort());
        graphics.push({kind,id:props.PrimitiveId,props,bbox:bbox(await eda.sch_Primitive.getPrimitivesBBox([props.PrimitiveId]))});
      }
    }
    graphics.sort((a,b)=>(a.kind+a.id).localeCompare(b.kind+b.id));
    const wires=(await eda.sch_PrimitiveWire.getAll()).length;
    const buses=(await eda.sch_PrimitiveBus.getAll()).length;
    await identity();
    return norm({schema:1,projectId:input.projectId,documentId:input.documentId,units:'raw-0.01inch',axis:'y-up',components,graphics,orphanAttributes:attrs.filter(a=>!parts.some(c=>c.getState_PrimitiveId()===a.getState_ParentPrimitiveId())).map(a=>fields(a,attrFields)).sort((a,b)=>a.PrimitiveId.localeCompare(b.PrimitiveId)),wires,buses});
  }
  function equivalent(a,b) {
    const aa=clone(a),bb=clone(b);
    if(aa.components.length!==bb.components.length)return false;
    for(let i=0;i<aa.components.length;i++) {
      for(let j=0;j<4;j++) if(Math.abs(aa.components[i].bbox[j]-bb.components[i].bbox[j])>0.001)return false;
      aa.components[i].bbox=bb.components[i].bbox;
    }
    return same(aa,bb);
  }
  function preflight(source,moves,bounds,gap) {
    if(source.orphanAttributes?.length)throw Error('UNOWNED_ATTRIBUTES_UNSUPPORTED');
    if(source.wires!==0||source.buses!==0)throw Error('WIRED_PAGE_UNSUPPORTED');
    if(!Array.isArray(bounds)||bounds.length!==4)throw Error('Explicit usable bounds required');
    bounds.forEach(finite);finite(gap);
    if(gap<=0||bounds[2]<=bounds[0]||bounds[3]<=bounds[1])throw Error('Invalid bounds/clearance');
    if(!Array.isArray(moves)||!moves.length)throw Error('Empty move batch');
    const target=clone(source),ids=new Set();
    for(const move of moves) {
      if(Object.keys(move).sort().join(',')!=='id,x,y')throw Error('Only id/x/y moves are allowed');
      if(ids.has(move.id))throw Error('Duplicate move'); ids.add(move.id);
      const c=target.components.find(c=>c.id===move.id);
      if(!c||c.props.ComponentType!=='part')throw Error('Only native part movement supported');
      const dx=finite(move.x)-c.props.X,dy=finite(move.y)-c.props.Y;
      c.props.X=move.x;c.props.Y=move.y;
      c.bbox=c.bbox.map((v,i)=>round(v+(i%2===0?dx:dy)));
    }
    const collision=(a,b)=>a[0]<b[2]+gap&&b[0]<a[2]+gap&&a[1]<b[3]+gap&&b[1]<a[3]+gap;
    for(const c of target.components.filter(c=>ids.has(c.id))) {
      const b=c.bbox;
      if(b[0]<bounds[0]||b[1]<bounds[1]||b[2]>bounds[2]||b[3]>bounds[3])throw Error('OUT_OF_BOUNDS: '+c.id);
      for(const other of target.components) if(other.id!==c.id&&other.props.ComponentType!=='sheet'&&collision(b,other.bbox))throw Error('COLLISION: '+c.id+'/'+other.id);
      for(const g of target.graphics) if(collision(b,g.bbox))throw Error('GRAPHIC_COLLISION: '+c.id+'/'+g.id);
    }
    return target;
  }
  if(input.action==='status'){await identity();return clone(root.operations[input.operationId]??{state:'NOT_FOUND'});}
  if(root.busy)throw Error('LIVE_WRITER_BUSY');
  root.busy=true;
  try {
    if(input.action==='capture')return {state:'CAPTURED',snapshot:await capture()};
    if(!['apply','rollback','reopen'].includes(input.action))throw Error('Unsupported guarded action');
    if(typeof input.operationId!=='string'||!input.operationId.trim())throw Error('Operation ID required');
    let op=root.operations[input.operationId];
    if(input.action==='apply') {
      const signature=JSON.stringify(norm({source:input.source,moves:input.moves,bounds:input.bounds,gap:input.gap}));
      if(op) {if(op.signature!==signature)throw Error('OPERATION_ID_REUSED');return clone(op);}
      const current=await capture();
      if(!equivalent(input.source,current))throw Error('STALE_SOURCE');
      const target=preflight(current,input.moves,input.bounds,input.gap);
      op=root.operations[input.operationId]={operationId:input.operationId,projectId:input.projectId,documentId:input.documentId,
        signature,state:'PREPARED',source:current,target,steps:[clone(current)],moves:input.moves};
      let expected=clone(current);
      try {
        op.state='APPLYING';
        for(const m of input.moves) {
          if(!equivalent(await capture(),expected))throw Error('CONCURRENT_CHANGE');
          const next=clone(expected),c=next.components.find(c=>c.id===m.id),t=target.components.find(c=>c.id===m.id);
          Object.assign(c,clone(t));op.steps.push(next);
          await identity();
          const result=await eda.sch_PrimitiveComponent.modify(m.id,movement(expected.components.find(c=>c.id===m.id).props,m.x,m.y));
          if(!result)throw Error('MODIFY_REJECTED');
          const observed=await capture();
          if(!equivalent(next,observed))throw Error('READBACK_MISMATCH');
          expected=observed;op.last=observed;
        }
        op.last=await capture();op.state='APPLIED';return clone(op);
      } catch(error) {
        op.error=String(error.message??error);op.state='FAILED';
        // Continue to guarded compensation; uncertain/unexpected state is never overwritten.
      }
    } else {
      if(!op)throw Error('UNKNOWN_OPERATION: session lost; use saved journal and manual reconciliation');
      if(op.projectId!==input.projectId||op.documentId!==input.documentId)throw Error('TARGET_CHANGED');
      if(input.action==='reopen') {
        if(op.state!=='APPLIED')throw Error('Only applied state can be saved/reopened');
        if(!equivalent(await capture(),op.last))throw Error('CONCURRENT_CHANGE');
        const d=await identity();
        if(await eda.sch_Document.save()!==true)throw Error('SAVE_FAILED');
        op.saveResult=true;
        if(!equivalent(await capture(),op.last))throw Error('POST_SAVE_CHANGED');
        if(await eda.dmt_EditorControl.closeDocument(d.tabId)!==true)throw Error('CLOSE_FAILED');
        const tab=await eda.dmt_EditorControl.openDocument(d.uuid);
        if(!tab)throw Error('REOPEN_FAILED');
        op.reloaded=await capture();
        op.state=equivalent(op.last,op.reloaded)?'RELOADED_MATCH':'RELOAD_MISMATCH';
        return clone(op);
      }
      if(!['APPLIED','RELOADED_MATCH','FAILED','RECOVERY_BLOCKED'].includes(op.state))return clone(op);
    }
    let now=await capture();
    if(!op.steps.some(s=>equivalent(s,now))) {op.state='RECOVERY_BLOCKED';op.recoveryObserved=now;return clone(op);}
    try {
      op.state='ROLLING_BACK';
      for(const m of [...op.moves].reverse()) {
        if(!equivalent(await capture(),now))throw Error('CONCURRENT_CHANGE');
        const original=op.source.components.find(c=>c.id===m.id),current=now.components.find(c=>c.id===m.id);
        if(same(original,current))continue;
        const expected=clone(now);Object.assign(expected.components.find(c=>c.id===m.id),clone(original));
        await identity();
        if(!await eda.sch_PrimitiveComponent.modify(m.id,movement(original.props,original.props.X,original.props.Y)))throw Error('INVERSE_REJECTED');
        now=await capture();if(!equivalent(expected,now))throw Error('INVERSE_MISMATCH');
      }
      if(!equivalent(op.source,now))throw Error('RESTORE_MISMATCH');
      op.restored=now;op.state='ROLLED_BACK';
      // Persist compensation only when this operation had explicitly saved its changes.
      if(op.saveResult) {if(await eda.sch_Document.save()!==true)throw Error('RESTORE_SAVE_FAILED');if(!equivalent(op.source,await capture()))throw Error('RESTORE_POST_SAVE_CHANGED');op.restoreSaved=true;}
    } catch(error) {op.state='RECOVERY_BLOCKED';op.recoveryError=String(error.message??error);}
    return clone(op);
  } catch(error) {
    if(input.action==='apply'&&!root.operations[input.operationId])return {state:'REJECTED',error:String(error.message??error)};
    throw error;
  } finally {root.busy=false;}
}

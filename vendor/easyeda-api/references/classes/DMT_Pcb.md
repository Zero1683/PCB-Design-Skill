# DMT\_Pcb class

Document tree / PCB management class

## Signature

```typescript
class DMT_Pcb
```

## Remarks

Operations related to PCB management in the currently open project

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[copyPcb(pcbUuid, boardName)](./DMT_Pcb.md)

</td><td>

</td><td>

Copy PCB

</td></tr>
<tr><td>

[createPcb(boardName)](./DMT_Pcb.md)

</td><td>

</td><td>

Create PCB

</td></tr>
<tr><td>

[deletePcb(pcbUuid)](./DMT_Pcb.md)

</td><td>

</td><td>

Delete PCB

</td></tr>
<tr><td>

[getAllPcbsInfo()](./DMT_Pcb.md)

</td><td>

</td><td>

Get all in the project PCB detailed properties of

</td></tr>
<tr><td>

[getCurrentPcbInfo()](./DMT_Pcb.md)

</td><td>

</td><td>

Get detailed properties of Current PCB

</td></tr>
<tr><td>

[getPcbInfo(pcbUuid)](./DMT_Pcb.md)

</td><td>

</td><td>

Get detailed properties of PCB

</td></tr>
<tr><td>

[modifyPcbName(pcbUuid, pcbName)](./DMT_Pcb.md)

</td><td>

</td><td>

Modify PCB name

</td></tr>
</tbody></table>

---

## 方法详情

### copypcb

# DMT\_Pcb.copyPcb() method

Copy PCB

## Signature

```typescript
function copyPcb(pcbUuid: string, boardName?: string): Promise<string | undefined>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

pcbUuid

</td><td>

string

</td><td>

Source PCB UUID

</td></tr>
<tr><td>

boardName

</td><td>

string

</td><td>

_(Optional)_ Name of the board the new PCB belongs to. If not specified, it is a free PCB

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

New PCB UUID. If it is `undefined`<!-- -->, the copy failed

## Remarks

Even if the PCB here is already associated with a reuse block (a reuse block symbol with the same name exists in the project library), no new reuse block symbol will be created. This operation logic is consistent with the current editor front end

### createpcb

# DMT\_Pcb.createPcb() method

Create PCB

## Signature

```typescript
function createPcb(boardName?: string): Promise<string | undefined>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

boardName

</td><td>

string

</td><td>

_(Optional)_ Name of the board it belongs to. If not specified, it is a free PCB

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

PCB UUID, if it is `undefined` creation fails

### deletepcb

# DMT\_Pcb.deletePcb() method

Delete PCB

## Signature

```typescript
function deletePcb(pcbUuid: string): Promise<boolean>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

pcbUuid

</td><td>

string

</td><td>

PCB UUID

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

If the PCB is already associated with a reuse block (a reuse block symbol with the same name exists in the project library), deleting the PCB will also delete the associated schematic and reuse block symbol. If the reuse block symbol cannot be deleted, it will be skipped

### getallpcbsinfo

# DMT\_Pcb.getAllPcbsInfo() method

Get all in the project PCB detailed properties of

## Signature

```typescript
function getAllPcbsInfo(): Promise<Array<IDMT_PcbItem>>;
```

## Returns

Promise&lt;Array&lt;[IDMT\_PcbItem](../interfaces/IDMT_PcbItem.md)<!-- -->&gt;&gt;

Array of detailed properties of all PCBs

### getcurrentpcbinfo

# DMT\_Pcb.getCurrentPcbInfo() method

Get detailed properties of Current PCB

## Signature

```typescript
function getCurrentPcbInfo(): Promise<IDMT_PcbItem | undefined>;
```

## Returns

Promise&lt;[IDMT\_PcbItem](../interfaces/IDMT_PcbItem.md) \| undefined&gt;

PCB detailed properties of; if it is `undefined`<!-- -->, the retrieval failed

## Remarks

It will get the detailed properties of the currently open PCB that has the last input focus

### getpcbinfo

# DMT\_Pcb.getPcbInfo() method

Get detailed properties of PCB

## Signature

```typescript
function getPcbInfo(pcbUuid: string): Promise<IDMT_PcbItem | undefined>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

pcbUuid

</td><td>

string

</td><td>

PCB UUID

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IDMT\_PcbItem](../interfaces/IDMT_PcbItem.md) \| undefined&gt;

PCB detailed properties of; if it is `undefined`<!-- -->, the retrieval failed

### modifypcbname

# DMT\_Pcb.modifyPcbName() method

Modify PCB name

## Signature

```typescript
function modifyPcbName(pcbUuid: string, pcbName: string): Promise<boolean>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

pcbUuid

</td><td>

string

</td><td>

PCB UUID

</td></tr>
<tr><td>

pcbName

</td><td>

string

</td><td>

PCB name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether Modify Successful

## Remarks

If the PCB is already associated with a reuse block (a reuse block symbol with the same name exists in the project library), modifying the name will also modify the reuse block symbol name and the associated schematic name

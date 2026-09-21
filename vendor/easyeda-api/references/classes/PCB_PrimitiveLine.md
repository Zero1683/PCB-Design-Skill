# PCB\_PrimitiveLine class

PCB &amp; footprint / line primitive class

## Signature

```typescript
class PCB_PrimitiveLine implements IPCB_PrimitiveAPI
```
**Implements:** [IPCB\_PrimitiveAPI](../interfaces/IPCB_PrimitiveAPI.md)

## Remarks

Both lines and arc lines are wires, corresponding to the line traces and arc traces on the canvas

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[create(net, layer, startX, startY, endX, endY, lineWidth, primitiveLock)](./PCB_PrimitiveLine.md)

</td><td>

</td><td>

Create a line

</td></tr>
<tr><td>

[delete(primitiveIds)](./PCB_PrimitiveLine.md)

</td><td>

</td><td>

**_(BETA)_** Delete the line

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitiveLine.md)

</td><td>

</td><td>

**_(BETA)_** Get the line

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitiveLine.md)

</td><td>

</td><td>

**_(BETA)_** Get the line

</td></tr>
<tr><td>

[getAll(net, layer, primitiveLock)](./PCB_PrimitiveLine.md)

</td><td>

</td><td>

**_(BETA)_** Get all lines

</td></tr>
<tr><td>

[getAllPrimitiveId(net, layer, primitiveLock)](./PCB_PrimitiveLine.md)

</td><td>

</td><td>

**_(BETA)_** Get the primitive IDs of all lines

</td></tr>
<tr><td>

[modify(primitiveId, property)](./PCB_PrimitiveLine.md)

</td><td>

</td><td>

**_(BETA)_** Modify the line

</td></tr>
</tbody></table>

---

## 方法详情

### create

# PCB\_PrimitiveLine.create() method

Create a line

## Signature

```typescript
function create(
	net: string,
	layer: TPCB_LayersOfLine,
	startX: number,
	startY: number,
	endX: number,
	endY: number,
	lineWidth?: number,
	primitiveLock?: boolean,
): Promise<IPCB_PrimitiveLine | undefined>;
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

net

</td><td>

string

</td><td>

Net name

</td></tr>
<tr><td>

layer

</td><td>

[TPCB\_LayersOfLine](../types/TPCB_LayersOfLine.md)

</td><td>

Layer

</td></tr>
<tr><td>

startX

</td><td>

number

</td><td>

Start position X

</td></tr>
<tr><td>

startY

</td><td>

number

</td><td>

Start position Y

</td></tr>
<tr><td>

endX

</td><td>

number

</td><td>

End position X

</td></tr>
<tr><td>

endY

</td><td>

number

</td><td>

End position Y

</td></tr>
<tr><td>

lineWidth

</td><td>

number

</td><td>

_(Optional)_ Line width

</td></tr>
<tr><td>

primitiveLock

</td><td>

boolean

</td><td>

_(Optional)_ Whether it is locked

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveLine](./IPCB_PrimitiveLine.md) \| undefined&gt;

Line primitive object

### delete

# PCB\_PrimitiveLine.delete() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete the line

## Signature

```typescript
function delete(primitiveIds: string | IPCB_PrimitiveLine | Array<string> | Array<IPCB_PrimitiveLine>): Promise<boolean>;
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

primitiveIds

</td><td>

string \| [IPCB\_PrimitiveLine](./IPCB_PrimitiveLine.md) \| Array&lt;string&gt; \| Array&lt;[IPCB\_PrimitiveLine](./IPCB_PrimitiveLine.md)<!-- -->&gt;

</td><td>

Primitive ID of the line or the line primitive object

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Delete Whether the operation is successful

### get

# PCB\_PrimitiveLine.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the line

## Signature

```typescript
function get(primitiveIds: string): Promise<IPCB_PrimitiveLine | undefined>;
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

primitiveIds

</td><td>

string

</td><td>

Primitive ID of the line, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveLine](./IPCB_PrimitiveLine.md) \| undefined&gt;

Line primitive object, `undefined` indicates that the retrieval failed

### get_1

# PCB\_PrimitiveLine.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the line

## Signature

```typescript
function get(primitiveIds: Array<string>): Promise<Array<IPCB_PrimitiveLine>>;
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

primitiveIds

</td><td>

Array&lt;string&gt;

</td><td>

Primitive ID of the line, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveLine](./IPCB_PrimitiveLine.md)<!-- -->&gt;&gt;

Line primitive object; an empty array indicates that the retrieval failed

## Remarks

If multiple primitive IDs are passed in, a primitive ID that is not matched will not affect the return of other primitives; that is, fewer primitive objects than the number of primitive IDs passed in may be returned.

### getall

# PCB\_PrimitiveLine.getAll() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all lines

## Signature

```typescript
function getAll(
	net?: string,
	layer?: TPCB_LayersOfLine,
	primitiveLock?: boolean,
): Promise<Array<IPCB_PrimitiveLine>>;
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

net

</td><td>

string

</td><td>

_(Optional)_ Net name

</td></tr>
<tr><td>

layer

</td><td>

[TPCB\_LayersOfLine](../types/TPCB_LayersOfLine.md)

</td><td>

_(Optional)_ Layer

</td></tr>
<tr><td>

primitiveLock

</td><td>

boolean

</td><td>

_(Optional)_ Whether it is locked

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveLine](./IPCB_PrimitiveLine.md)<!-- -->&gt;&gt;

Line primitive object array

### getallprimitiveid

# PCB\_PrimitiveLine.getAllPrimitiveId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the primitive IDs of all lines

## Signature

```typescript
function getAllPrimitiveId(
	net?: string,
	layer?: TPCB_LayersOfLine,
	primitiveLock?: boolean,
): Promise<Array<string>>;
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

net

</td><td>

string

</td><td>

_(Optional)_ Net name

</td></tr>
<tr><td>

layer

</td><td>

[TPCB\_LayersOfLine](../types/TPCB_LayersOfLine.md)

</td><td>

_(Optional)_ Layer

</td></tr>
<tr><td>

primitiveLock

</td><td>

boolean

</td><td>

_(Optional)_ Whether it is locked

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;string&gt;&gt;

Array of polyline primitive IDs

### modify

# PCB\_PrimitiveLine.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify the line

## Signature

```typescript
function modify(
	primitiveId: string | IPCB_PrimitiveLine,
	property: {
		net?: string;
		layer?: TPCB_LayersOfLine;
		startX?: number;
		startY?: number;
		endX?: number;
		endY?: number;
		lineWidth?: number;
		primitiveLock?: boolean;
	},
): Promise<IPCB_PrimitiveLine | undefined>;
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

primitiveId

</td><td>

string \| [IPCB\_PrimitiveLine](./IPCB_PrimitiveLine.md)

</td><td>

Primitive ID

</td></tr>
<tr><td>

property

</td><td>

{ net?: string; layer?: [TPCB\_LayersOfLine](../types/TPCB_LayersOfLine.md)<!-- -->; startX?: number; startY?: number; endX?: number; endY?: number; lineWidth?: number; primitiveLock?: boolean }

</td><td>

Modify Parameter

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveLine](./IPCB_PrimitiveLine.md) \| undefined&gt;

Line primitive object

# PCB\_PrimitiveArc class

PCB &amp; footprint / arc line primitive class

## Signature

```typescript
class PCB_PrimitiveArc implements IPCB_PrimitiveAPI
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

[create(net, layer, startX, startY, endX, endY, arcAngle, lineWidth, interactiveMode, primitiveLock)](./PCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Create Arc line

</td></tr>
<tr><td>

[delete(primitiveIds)](./PCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Delete Arc line

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Get Arc line

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Get Arc line

</td></tr>
<tr><td>

[getAll(net, layer, primitiveLock)](./PCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Get all Arc line

</td></tr>
<tr><td>

[getAllPrimitiveId(net, layer, primitiveLock)](./PCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Get all Arc line primitive IDs

</td></tr>
<tr><td>

[modify(primitiveId, property)](./PCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Modify Arc line

</td></tr>
</tbody></table>

---

## 方法详情

### create

# PCB\_PrimitiveArc.create() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create Arc line

## Signature

```typescript
function create(
	net: string,
	layer: TPCB_LayersOfLine,
	startX: number,
	startY: number,
	endX: number,
	endY: number,
	arcAngle: number,
	lineWidth?: number,
	interactiveMode?: EPCB_PrimitiveArcInteractiveMode,
	primitiveLock?: boolean,
): Promise<IPCB_PrimitiveArc | undefined>;
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

arcAngle

</td><td>

number

</td><td>

Arc angle

</td></tr>
<tr><td>

lineWidth

</td><td>

number

</td><td>

_(Optional)_ Line width

</td></tr>
<tr><td>

interactiveMode

</td><td>

[EPCB\_PrimitiveArcInteractiveMode](../enums/EPCB_PrimitiveArcInteractiveMode.md)

</td><td>

_(Optional)_ Interaction mode

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

Promise&lt;[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md) \| undefined&gt;

Arc line primitive object

### delete

# PCB\_PrimitiveArc.delete() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete Arc line

## Signature

```typescript
function delete(primitiveIds: string | IPCB_PrimitiveArc | Array<string> | Array<IPCB_PrimitiveArc>): Promise<boolean>;
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

string \| [IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md) \| Array&lt;string&gt; \| Array&lt;[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)<!-- -->&gt;

</td><td>

Arc line primitive ID or Arc line primitive object

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Delete Whether the operation is successful

### get

# PCB\_PrimitiveArc.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Arc line

## Signature

```typescript
function get(primitiveIds: string): Promise<IPCB_PrimitiveArc | undefined>;
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

Arc line primitive ID, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md) \| undefined&gt;

Arc line primitive object, `undefined` indicates that the retrieval failed

### get_1

# PCB\_PrimitiveArc.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Arc line

## Signature

```typescript
function get(primitiveIds: Array<string>): Promise<Array<IPCB_PrimitiveArc>>;
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

Arc line primitive ID, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)<!-- -->&gt;&gt;

Arc line primitive object; an empty array indicates that the retrieval failed

## Remarks

If multiple primitive IDs are passed in, a primitive ID that is not matched will not affect the return of other primitives; that is, fewer primitive objects than the number of primitive IDs passed in may be returned.

### getall

# PCB\_PrimitiveArc.getAll() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all Arc line

## Signature

```typescript
function getAll(
	net?: string,
	layer?: TPCB_LayersOfLine,
	primitiveLock?: boolean,
): Promise<Array<IPCB_PrimitiveArc>>;
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

Promise&lt;Array&lt;[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)<!-- -->&gt;&gt;

Array of Arc line primitive objects

### getallprimitiveid

# PCB\_PrimitiveArc.getAllPrimitiveId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all Arc line primitive IDs

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

Array of Arc line primitive IDs

### modify

# PCB\_PrimitiveArc.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Arc line

## Signature

```typescript
function modify(
	primitiveId: string | IPCB_PrimitiveArc,
	property: {
		net?: string;
		layer?: TPCB_LayersOfLine;
		startX?: number;
		startY?: number;
		endX?: number;
		endY?: number;
		arcAngle?: number;
		lineWidth?: number;
		interactiveMode?: EPCB_PrimitiveArcInteractiveMode;
		primitiveLock?: boolean;
	},
): Promise<IPCB_PrimitiveArc | undefined>;
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

string \| [IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)

</td><td>

Primitive ID

</td></tr>
<tr><td>

property

</td><td>

{ net?: string; layer?: [TPCB\_LayersOfLine](../types/TPCB_LayersOfLine.md)<!-- -->; startX?: number; startY?: number; endX?: number; endY?: number; arcAngle?: number; lineWidth?: number; interactiveMode?: [EPCB\_PrimitiveArcInteractiveMode](../enums/EPCB_PrimitiveArcInteractiveMode.md)<!-- -->; primitiveLock?: boolean }

</td><td>

Modify Parameter

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md) \| undefined&gt;

Arc line primitive object

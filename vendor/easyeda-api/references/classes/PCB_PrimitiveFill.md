# PCB\_PrimitiveFill class

PCB &amp; footprint / fill primitive class

## Signature

```typescript
class PCB_PrimitiveFill implements IPCB_PrimitiveAPI
```
**Implements:** [IPCB\_PrimitiveAPI](../interfaces/IPCB_PrimitiveAPI.md)

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[create(layer, complexPolygon, net, fillMode, lineWidth, primitiveLock)](./PCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Create a fill

</td></tr>
<tr><td>

[delete(primitiveIds)](./PCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Delete the fill

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Get the fill

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Get the fill

</td></tr>
<tr><td>

[getAll(layer, net, primitiveLock)](./PCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Get all fills

</td></tr>
<tr><td>

[getAllPrimitiveId(layer, net, primitiveLock)](./PCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Get the primitive IDs of all fills

</td></tr>
<tr><td>

[modify(primitiveId, property)](./PCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Modify the fill

</td></tr>
</tbody></table>

---

## 方法详情

### create

# PCB\_PrimitiveFill.create() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create a fill

## Signature

```typescript
function create(
	layer: TPCB_LayersOfFill,
	complexPolygon: IPCB_Polygon,
	net?: string,
	fillMode?: EPCB_PrimitiveFillMode,
	lineWidth?: number,
	primitiveLock?: boolean,
): Promise<IPCB_PrimitiveFill | undefined>;
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

layer

</td><td>

[TPCB\_LayersOfFill](../types/TPCB_LayersOfFill.md)

</td><td>

Layer

</td></tr>
<tr><td>

complexPolygon

</td><td>

[IPCB\_Polygon](./IPCB_Polygon.md)

</td><td>

Complex polygon object

</td></tr>
<tr><td>

net

</td><td>

string

</td><td>

_(Optional)_ Net name

</td></tr>
<tr><td>

fillMode

</td><td>

[EPCB\_PrimitiveFillMode](../enums/EPCB_PrimitiveFillMode.md)

</td><td>

_(Optional)_ Fill mode

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

Promise&lt;[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md) \| undefined&gt;

Fill primitive object

### delete

# PCB\_PrimitiveFill.delete() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete the fill

## Signature

```typescript
function delete(primitiveIds: string | IPCB_PrimitiveFill | Array<string> | Array<IPCB_PrimitiveFill>): Promise<boolean>;
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

string \| [IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md) \| Array&lt;string&gt; \| Array&lt;[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)<!-- -->&gt;

</td><td>

Primitive ID of the fill or the fill primitive object

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Delete Whether the operation is successful

### get

# PCB\_PrimitiveFill.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the fill

## Signature

```typescript
function get(primitiveIds: string): Promise<IPCB_PrimitiveFill | undefined>;
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

Primitive ID of the fill, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md) \| undefined&gt;

Fill primitive object, `undefined` indicates that the retrieval failed

### get_1

# PCB\_PrimitiveFill.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the fill

## Signature

```typescript
function get(primitiveIds: Array<string>): Promise<Array<IPCB_PrimitiveFill>>;
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

Primitive ID of the fill, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)<!-- -->&gt;&gt;

Fill primitive object; an empty array indicates that the retrieval failed

## Remarks

If multiple primitive IDs are passed in, a primitive ID that is not matched will not affect the return of other primitives; that is, fewer primitive objects than the number of primitive IDs passed in may be returned.

### getall

# PCB\_PrimitiveFill.getAll() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all fills

## Signature

```typescript
function getAll(
	layer?: TPCB_LayersOfFill,
	net?: string,
	primitiveLock?: boolean,
): Promise<Array<IPCB_PrimitiveFill>>;
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

layer

</td><td>

[TPCB\_LayersOfFill](../types/TPCB_LayersOfFill.md)

</td><td>

_(Optional)_ Layer

</td></tr>
<tr><td>

net

</td><td>

string

</td><td>

_(Optional)_ Net name

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

Promise&lt;Array&lt;[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)<!-- -->&gt;&gt;

Fill primitive object array

### getallprimitiveid

# PCB\_PrimitiveFill.getAllPrimitiveId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the primitive IDs of all fills

## Signature

```typescript
function getAllPrimitiveId(
	layer?: TPCB_LayersOfFill,
	net?: string,
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

layer

</td><td>

[TPCB\_LayersOfFill](../types/TPCB_LayersOfFill.md)

</td><td>

_(Optional)_ Layer

</td></tr>
<tr><td>

net

</td><td>

string

</td><td>

_(Optional)_ Net name

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

Array of fill primitive IDs

### modify

# PCB\_PrimitiveFill.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify the fill

## Signature

```typescript
function modify(
	primitiveId: string | IPCB_PrimitiveFill,
	property: {
		layer?: TPCB_LayersOfFill;
		complexPolygon?: IPCB_Polygon;
		net?: string;
		fillMode?: EPCB_PrimitiveFillMode;
		lineWidth?: number;
		primitiveLock?: boolean;
	},
): Promise<IPCB_PrimitiveFill | undefined>;
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

string \| [IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)

</td><td>

Primitive ID

</td></tr>
<tr><td>

property

</td><td>

{ layer?: [TPCB\_LayersOfFill](../types/TPCB_LayersOfFill.md)<!-- -->; complexPolygon?: [IPCB\_Polygon](./IPCB_Polygon.md)<!-- -->; net?: string; fillMode?: [EPCB\_PrimitiveFillMode](../enums/EPCB_PrimitiveFillMode.md)<!-- -->; lineWidth?: number; primitiveLock?: boolean }

</td><td>

Modify Parameter

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md) \| undefined&gt;

Fill primitive object, `undefined` indicates that the modification failed

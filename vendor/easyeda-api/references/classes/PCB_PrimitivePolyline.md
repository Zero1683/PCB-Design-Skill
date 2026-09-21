# PCB\_PrimitivePolyline class

PCB &amp; footprint / polyline primitive class

## Signature

```typescript
class PCB_PrimitivePolyline implements IPCB_PrimitiveAPI
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

[create(net, layer, polygon, lineWidth, primitiveLock)](./PCB_PrimitivePolyline.md)

</td><td>

</td><td>

Create a polyline

</td></tr>
<tr><td>

[delete(primitiveIds)](./PCB_PrimitivePolyline.md)

</td><td>

</td><td>

**_(BETA)_** Delete the polyline

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitivePolyline.md)

</td><td>

</td><td>

**_(BETA)_** Get the polyline

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitivePolyline.md)

</td><td>

</td><td>

**_(BETA)_** Get the polyline

</td></tr>
<tr><td>

[getAll(net, layer, primitiveLock)](./PCB_PrimitivePolyline.md)

</td><td>

</td><td>

**_(BETA)_** Get all polylines

</td></tr>
<tr><td>

[getAllPrimitiveId(net, layer, primitiveLock)](./PCB_PrimitivePolyline.md)

</td><td>

</td><td>

**_(BETA)_** Get the primitive IDs of all polylines

</td></tr>
<tr><td>

[modify(primitiveId, property)](./PCB_PrimitivePolyline.md)

</td><td>

</td><td>

**_(BETA)_** Modify the polyline

</td></tr>
</tbody></table>

---

## 方法详情

### create

# PCB\_PrimitivePolyline.create() method

Create a polyline

## Signature

```typescript
function create(
	net: string,
	layer: TPCB_LayersOfLine,
	polygon: IPCB_Polygon,
	lineWidth?: number,
	primitiveLock?: boolean,
): Promise<IPCB_PrimitivePolyline | undefined>;
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

polygon

</td><td>

[IPCB\_Polygon](./IPCB_Polygon.md)

</td><td>

Single polygon object

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

Promise&lt;[IPCB\_PrimitivePolyline](./IPCB_PrimitivePolyline.md) \| undefined&gt;

Polyline primitive object

### delete

# PCB\_PrimitivePolyline.delete() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete the polyline

## Signature

```typescript
function delete(primitiveIds: string | IPCB_PrimitivePolyline | Array<string> | Array<IPCB_PrimitivePolyline>): Promise<boolean>;
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

string \| [IPCB\_PrimitivePolyline](./IPCB_PrimitivePolyline.md) \| Array&lt;string&gt; \| Array&lt;[IPCB\_PrimitivePolyline](./IPCB_PrimitivePolyline.md)<!-- -->&gt;

</td><td>

Primitive ID of the polyline or the polyline primitive object

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Delete Whether the operation is successful

### get

# PCB\_PrimitivePolyline.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the polyline

## Signature

```typescript
function get(primitiveIds: string): Promise<IPCB_PrimitivePolyline | undefined>;
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

Primitive ID of the polyline, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitivePolyline](./IPCB_PrimitivePolyline.md) \| undefined&gt;

Polyline primitive object, `undefined` indicates that the retrieval failed

### get_1

# PCB\_PrimitivePolyline.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the polyline

## Signature

```typescript
function get(primitiveIds: Array<string>): Promise<Array<IPCB_PrimitivePolyline>>;
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

Primitive ID of the polyline, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitivePolyline](./IPCB_PrimitivePolyline.md)<!-- -->&gt;&gt;

Polyline primitive object; an empty array indicates that the retrieval failed

## Remarks

If multiple primitive IDs are passed in, a primitive ID that is not matched will not affect the return of other primitives; that is, fewer primitive objects than the number of primitive IDs passed in may be returned.

### getall

# PCB\_PrimitivePolyline.getAll() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all polylines

## Signature

```typescript
function getAll(
	net?: string,
	layer?: TPCB_LayersOfLine,
	primitiveLock?: boolean,
): Promise<Array<IPCB_PrimitivePolyline>>;
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

Promise&lt;Array&lt;[IPCB\_PrimitivePolyline](./IPCB_PrimitivePolyline.md)<!-- -->&gt;&gt;

Polyline primitive object array

### getallprimitiveid

# PCB\_PrimitivePolyline.getAllPrimitiveId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the primitive IDs of all polylines

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

# PCB\_PrimitivePolyline.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify the polyline

## Signature

```typescript
function modify(
	primitiveId: string | IPCB_PrimitivePolyline,
	property: {
		net?: string;
		layer?: TPCB_LayersOfLine;
		polygon?: IPCB_Polygon;
		lineWidth?: number;
		primitiveLock?: boolean;
	},
): Promise<IPCB_PrimitivePolyline | undefined>;
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

string \| [IPCB\_PrimitivePolyline](./IPCB_PrimitivePolyline.md)

</td><td>

Primitive ID

</td></tr>
<tr><td>

property

</td><td>

{ net?: string; layer?: [TPCB\_LayersOfLine](../types/TPCB_LayersOfLine.md)<!-- -->; polygon?: [IPCB\_Polygon](./IPCB_Polygon.md)<!-- -->; lineWidth?: number; primitiveLock?: boolean }

</td><td>

Modify Parameter

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitivePolyline](./IPCB_PrimitivePolyline.md) \| undefined&gt;

Polyline primitive object

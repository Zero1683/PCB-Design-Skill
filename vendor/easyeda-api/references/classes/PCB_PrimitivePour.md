# PCB\_PrimitivePour class

PCB &amp; footprint / copper border primitive class

## Signature

```typescript
class PCB_PrimitivePour implements IPCB_PrimitiveAPI
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

[create(net, layer, complexPolygon, pourFillMethod, preserveSilos, pourName, pourPriority, lineWidth, primitiveLock)](./PCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Create Copper border

</td></tr>
<tr><td>

[delete(primitiveIds)](./PCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Delete Copper border

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Get Copper border

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Get Copper border

</td></tr>
<tr><td>

[getAll(net, layer, primitiveLock)](./PCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Get all Copper border primitive

</td></tr>
<tr><td>

[getAllPrimitiveId(net, layer, primitiveLock)](./PCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Get all Copper border primitive IDs

</td></tr>
<tr><td>

[modify(primitiveId, property)](./PCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Modify Copper border

</td></tr>
</tbody></table>

---

## 方法详情

### create

# PCB\_PrimitivePour.create() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create Copper border

## Signature

```typescript
function create(
	net: string,
	layer: TPCB_LayersOfCopper,
	complexPolygon: IPCB_Polygon,
	pourFillMethod?: EPCB_PrimitivePourFillMethod,
	preserveSilos?: boolean,
	pourName?: string,
	pourPriority?: number,
	lineWidth?: number,
	primitiveLock?: boolean,
): Promise<IPCB_PrimitivePour | undefined>;
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

[TPCB\_LayersOfCopper](../types/TPCB_LayersOfCopper.md)

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

pourFillMethod

</td><td>

[EPCB\_PrimitivePourFillMethod](../enums/EPCB_PrimitivePourFillMethod.md)

</td><td>

_(Optional)_ Copper fill method

</td></tr>
<tr><td>

preserveSilos

</td><td>

boolean

</td><td>

_(Optional)_ Whether to keep islands

</td></tr>
<tr><td>

pourName

</td><td>

string

</td><td>

_(Optional)_ Copper name

</td></tr>
<tr><td>

pourPriority

</td><td>

number

</td><td>

_(Optional)_ Copper priority

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

Promise&lt;[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md) \| undefined&gt;

Copper border primitive object

### delete

# PCB\_PrimitivePour.delete() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete Copper border

## Signature

```typescript
function delete(primitiveIds: string | IPCB_PrimitivePour | Array<string> | Array<IPCB_PrimitivePour>): Promise<boolean>;
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

string \| [IPCB\_PrimitivePour](./IPCB_PrimitivePour.md) \| Array&lt;string&gt; \| Array&lt;[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)<!-- -->&gt;

</td><td>

Copper border primitive ID or Copper border primitive object

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Delete Whether the operation is successful

### get

# PCB\_PrimitivePour.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Copper border

## Signature

```typescript
function get(primitiveIds: string): Promise<IPCB_PrimitivePour | undefined>;
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

Copper border primitive ID, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md) \| undefined&gt;

Copper border primitive object, `undefined` indicates that the retrieval failed

### get_1

# PCB\_PrimitivePour.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Copper border

## Signature

```typescript
function get(primitiveIds: Array<string>): Promise<Array<IPCB_PrimitivePour>>;
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

Copper border primitive ID, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)<!-- -->&gt;&gt;

Copper border primitive object; an empty array indicates that the retrieval failed

## Remarks

If multiple primitive IDs are passed in, a primitive ID that is not matched will not affect the return of other primitives; that is, fewer primitive objects than the number of primitive IDs passed in may be returned.

### getall

# PCB\_PrimitivePour.getAll() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all Copper border primitive

## Signature

```typescript
function getAll(
	net?: string,
	layer?: TPCB_LayersOfCopper,
	primitiveLock?: boolean,
): Promise<Array<IPCB_PrimitivePour>>;
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

[TPCB\_LayersOfCopper](../types/TPCB_LayersOfCopper.md)

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

Promise&lt;Array&lt;[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)<!-- -->&gt;&gt;

Array of Copper border primitive objects

### getallprimitiveid

# PCB\_PrimitivePour.getAllPrimitiveId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all Copper border primitive IDs

## Signature

```typescript
function getAllPrimitiveId(
	net?: string,
	layer?: TPCB_LayersOfCopper,
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

[TPCB\_LayersOfCopper](../types/TPCB_LayersOfCopper.md)

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

Array of Copper border primitive IDs

### modify

# PCB\_PrimitivePour.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Copper border

## Signature

```typescript
function modify(
	primitiveId: string | IPCB_PrimitivePour,
	property: {
		net?: string;
		layer?: TPCB_LayersOfCopper;
		complexPolygon?: IPCB_Polygon;
		pourFillMethod?: EPCB_PrimitivePourFillMethod;
		preserveSilos?: boolean;
		pourName?: string;
		pourPriority?: number;
		lineWidth?: number;
		primitiveLock?: boolean;
	},
): Promise<IPCB_PrimitivePour | undefined>;
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

string \| [IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)

</td><td>

Primitive ID

</td></tr>
<tr><td>

property

</td><td>

{ net?: string; layer?: [TPCB\_LayersOfCopper](../types/TPCB_LayersOfCopper.md)<!-- -->; complexPolygon?: [IPCB\_Polygon](./IPCB_Polygon.md)<!-- -->; pourFillMethod?: [EPCB\_PrimitivePourFillMethod](../enums/EPCB_PrimitivePourFillMethod.md)<!-- -->; preserveSilos?: boolean; pourName?: string; pourPriority?: number; lineWidth?: number; primitiveLock?: boolean }

</td><td>

Modify Parameter

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md) \| undefined&gt;

Copper border primitive object, `undefined` indicates that the modification failed

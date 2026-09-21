# PCB\_PrimitiveRegion class

PCB &amp; footprint / forbidden region and constrained region primitive class

## Signature

```typescript
class PCB_PrimitiveRegion implements IPCB_PrimitiveAPI
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

[create(layer, complexPolygon, ruleType, regionName, lineWidth, primitiveLock)](./PCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Create Region

</td></tr>
<tr><td>

[delete(primitiveIds)](./PCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Delete Region

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Get Region

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Get Region

</td></tr>
<tr><td>

[getAll(layer, ruleType, primitiveLock)](./PCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Get all Region

</td></tr>
<tr><td>

[getAllPrimitiveId(layer, ruleType, primitiveLock)](./PCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Get all Region primitive IDs

</td></tr>
<tr><td>

[modify(primitiveId, property)](./PCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Modify Region

</td></tr>
</tbody></table>

---

## 方法详情

### create

# PCB\_PrimitiveRegion.create() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create Region

## Signature

```typescript
function create(
	layer: TPCB_LayersOfRegion,
	complexPolygon: IPCB_Polygon,
	ruleType?: Array<EPCB_PrimitiveRegionRuleType>,
	regionName?: string,
	lineWidth?: number,
	primitiveLock?: boolean,
): Promise<IPCB_PrimitiveRegion | undefined>;
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

[TPCB\_LayersOfRegion](../types/TPCB_LayersOfRegion.md)

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

ruleType

</td><td>

Array&lt;[EPCB\_PrimitiveRegionRuleType](../enums/EPCB_PrimitiveRegionRuleType.md)<!-- -->&gt;

</td><td>

_(Optional)_ Region rule type

</td></tr>
<tr><td>

regionName

</td><td>

string

</td><td>

_(Optional)_ Region name

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

Promise&lt;[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md) \| undefined&gt;

Region primitive object

### delete

# PCB\_PrimitiveRegion.delete() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete Region

## Signature

```typescript
function delete(primitiveIds: string | IPCB_PrimitiveRegion | Array<string> | Array<IPCB_PrimitiveRegion>): Promise<boolean>;
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

string \| [IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md) \| Array&lt;string&gt; \| Array&lt;[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md)<!-- -->&gt;

</td><td>

Region primitive ID or Region primitive object

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Delete Whether the operation is successful

### get

# PCB\_PrimitiveRegion.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Region

## Signature

```typescript
function get(primitiveIds: string): Promise<IPCB_PrimitiveRegion | undefined>;
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

Region primitive ID, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md) \| undefined&gt;

Region primitive object, `undefined` indicates that the retrieval failed

### get_1

# PCB\_PrimitiveRegion.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Region

## Signature

```typescript
function get(primitiveIds: Array<string>): Promise<Array<IPCB_PrimitiveRegion>>;
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

Region primitive ID, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md)<!-- -->&gt;&gt;

Region primitive object; an empty array indicates that the retrieval failed

## Remarks

If multiple primitive IDs are passed in, a primitive ID that is not matched will not affect the return of other primitives; that is, fewer primitive objects than the number of primitive IDs passed in may be returned.

### getall

# PCB\_PrimitiveRegion.getAll() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all Region

## Signature

```typescript
function getAll(
	layer?: TPCB_LayersOfRegion,
	ruleType?: Array<EPCB_PrimitiveRegionRuleType>,
	primitiveLock?: boolean,
): Promise<Array<IPCB_PrimitiveRegion>>;
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

[TPCB\_LayersOfRegion](../types/TPCB_LayersOfRegion.md)

</td><td>

_(Optional)_ Layer

</td></tr>
<tr><td>

ruleType

</td><td>

Array&lt;[EPCB\_PrimitiveRegionRuleType](../enums/EPCB_PrimitiveRegionRuleType.md)<!-- -->&gt;

</td><td>

_(Optional)_ Region rule type. Only primitives whose rule types are all consistent will be matched

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

Promise&lt;Array&lt;[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md)<!-- -->&gt;&gt;

Array of Region primitive objects

### getallprimitiveid

# PCB\_PrimitiveRegion.getAllPrimitiveId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all Region primitive IDs

## Signature

```typescript
function getAllPrimitiveId(
	layer?: TPCB_LayersOfRegion,
	ruleType?: Array<EPCB_PrimitiveRegionRuleType>,
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

[TPCB\_LayersOfRegion](../types/TPCB_LayersOfRegion.md)

</td><td>

_(Optional)_ Layer

</td></tr>
<tr><td>

ruleType

</td><td>

Array&lt;[EPCB\_PrimitiveRegionRuleType](../enums/EPCB_PrimitiveRegionRuleType.md)<!-- -->&gt;

</td><td>

_(Optional)_ Region rule type. Only primitives whose rule types are all consistent will be matched

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

Array of Region primitive IDs

### modify

# PCB\_PrimitiveRegion.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Region

## Signature

```typescript
function modify(
	primitiveId: string | IPCB_PrimitiveRegion,
	property: {
		layer?: TPCB_LayersOfRegion;
		complexPolygon?: IPCB_Polygon;
		ruleType?: Array<EPCB_PrimitiveRegionRuleType>;
		regionName?: string;
		lineWidth?: number;
		primitiveLock?: boolean;
	},
): Promise<IPCB_PrimitiveRegion | undefined>;
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

string \| [IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md)

</td><td>

Primitive ID

</td></tr>
<tr><td>

property

</td><td>

{ layer?: [TPCB\_LayersOfRegion](../types/TPCB_LayersOfRegion.md)<!-- -->; complexPolygon?: [IPCB\_Polygon](./IPCB_Polygon.md)<!-- -->; ruleType?: Array&lt;[EPCB\_PrimitiveRegionRuleType](../enums/EPCB_PrimitiveRegionRuleType.md)<!-- -->&gt;; regionName?: string; lineWidth?: number; primitiveLock?: boolean }

</td><td>

Modify Parameter

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md) \| undefined&gt;

Region primitive object, `undefined` indicates that the modification failed

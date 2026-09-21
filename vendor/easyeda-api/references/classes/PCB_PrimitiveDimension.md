# PCB\_PrimitiveDimension class

PCB &amp; footprint / dimension primitive class

## Signature

```typescript
class PCB_PrimitiveDimension implements IPCB_PrimitiveAPI
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

[create(dimensionType, coordinateSet, layer, unit, lineWidth, precision, primitiveLock)](./PCB_PrimitiveDimension.md)

</td><td>

</td><td>

Create a dimension

</td></tr>
<tr><td>

[delete(primitiveIds)](./PCB_PrimitiveDimension.md)

</td><td>

</td><td>

**_(BETA)_** Delete the dimension

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitiveDimension.md)

</td><td>

</td><td>

**_(BETA)_** Get the dimension

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitiveDimension.md)

</td><td>

</td><td>

**_(BETA)_** Get the dimension

</td></tr>
<tr><td>

[getAll(layer, primitiveLock)](./PCB_PrimitiveDimension.md)

</td><td>

</td><td>

**_(BETA)_** Get all dimensions

</td></tr>
<tr><td>

[getAllPrimitiveId(layer, primitiveLock)](./PCB_PrimitiveDimension.md)

</td><td>

</td><td>

**_(BETA)_** Get the primitive IDs of all dimensions

</td></tr>
<tr><td>

[modify(primitiveId, property)](./PCB_PrimitiveDimension.md)

</td><td>

</td><td>

**_(BETA)_** Modify the dimension

</td></tr>
</tbody></table>

---

## 方法详情

### create

# PCB\_PrimitiveDimension.create() method

Create a dimension

## Signature

```typescript
function create(
	dimensionType: EPCB_PrimitiveDimensionType,
	coordinateSet: TPCB_PrimitiveDimensionCoordinateSet,
	layer?: TPCB_LayersOfDimension,
	unit?: ESYS_Unit.MILLIMETER | ESYS_Unit.CENTIMETER | ESYS_Unit.INCH | ESYS_Unit.MIL,
	lineWidth?: number,
	precision?: number,
	primitiveLock?: boolean,
): Promise<IPCB_PrimitiveDimension | undefined>;
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

dimensionType

</td><td>

[EPCB\_PrimitiveDimensionType](../enums/EPCB_PrimitiveDimensionType.md)

</td><td>

Dimension type

</td></tr>
<tr><td>

coordinateSet

</td><td>

[TPCB\_PrimitiveDimensionCoordinateSet](../types/TPCB_PrimitiveDimensionCoordinateSet.md)

</td><td>

Dimension coordinate set

</td></tr>
<tr><td>

layer

</td><td>

[TPCB\_LayersOfDimension](../types/TPCB_LayersOfDimension.md)

</td><td>

_(Optional)_ Layer

</td></tr>
<tr><td>

unit

</td><td>

[ESYS\_Unit.MILLIMETER](../enums/ESYS_Unit.md) \| [ESYS\_Unit.CENTIMETER](../enums/ESYS_Unit.md) \| [ESYS\_Unit.INCH](../enums/ESYS_Unit.md) \| [ESYS\_Unit.MIL](../enums/ESYS_Unit.md)

</td><td>

_(Optional)_ Unit

</td></tr>
<tr><td>

lineWidth

</td><td>

number

</td><td>

_(Optional)_ Line width

</td></tr>
<tr><td>

precision

</td><td>

number

</td><td>

_(Optional)_ Precision, value range `0`<!-- -->-`4`

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

Promise&lt;[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md) \| undefined&gt;

Dimension primitive object

### delete

# PCB\_PrimitiveDimension.delete() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete the dimension

## Signature

```typescript
function delete(primitiveIds: string | IPCB_PrimitiveDimension | Array<string> | Array<IPCB_PrimitiveDimension>): Promise<boolean>;
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

string \| [IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md) \| Array&lt;string&gt; \| Array&lt;[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md)<!-- -->&gt;

</td><td>

Primitive ID of the dimension or the dimension primitive object

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Delete Whether the operation is successful

### get

# PCB\_PrimitiveDimension.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the dimension

## Signature

```typescript
function get(primitiveIds: string): Promise<IPCB_PrimitiveDimension | undefined>;
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

Primitive ID of the dimension, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md) \| undefined&gt;

Dimension primitive object, `undefined` indicates that the retrieval failed

### get_1

# PCB\_PrimitiveDimension.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the dimension

## Signature

```typescript
function get(primitiveIds: Array<string>): Promise<Array<IPCB_PrimitiveDimension>>;
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

Primitive ID of the dimension, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md)<!-- -->&gt;&gt;

Dimension primitive object; an empty array indicates that the retrieval failed

## Remarks

If multiple primitive IDs are passed in, a primitive ID that is not matched will not affect the return of other primitives; that is, fewer primitive objects than the number of primitive IDs passed in may be returned.

### getall

# PCB\_PrimitiveDimension.getAll() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all dimensions

## Signature

```typescript
function getAll(
	layer?: TPCB_LayersOfDimension,
	primitiveLock?: boolean,
): Promise<Array<IPCB_PrimitiveDimension>>;
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

[TPCB\_LayersOfDimension](../types/TPCB_LayersOfDimension.md)

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

Promise&lt;Array&lt;[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md)<!-- -->&gt;&gt;

Dimension primitive object array

### getallprimitiveid

# PCB\_PrimitiveDimension.getAllPrimitiveId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the primitive IDs of all dimensions

## Signature

```typescript
function getAllPrimitiveId(
	layer?: TPCB_LayersOfDimension,
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

[TPCB\_LayersOfDimension](../types/TPCB_LayersOfDimension.md)

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

Array of dimension primitive IDs

### modify

# PCB\_PrimitiveDimension.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify the dimension

## Signature

```typescript
function modify(
	primitiveId: string | IPCB_PrimitiveDimension,
	property: {
		dimensionType?: EPCB_PrimitiveDimensionType;
		coordinateSet?: TPCB_PrimitiveDimensionCoordinateSet;
		layer?: TPCB_LayersOfDimension;
		unit?: ESYS_Unit.MILLIMETER | ESYS_Unit.CENTIMETER | ESYS_Unit.INCH | ESYS_Unit.MIL;
		lineWidth?: number;
		precision?: number;
		primitiveLock?: boolean;
	},
): Promise<IPCB_PrimitiveDimension | undefined>;
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

string \| [IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md)

</td><td>

Primitive ID

</td></tr>
<tr><td>

property

</td><td>

{ dimensionType?: [EPCB\_PrimitiveDimensionType](../enums/EPCB_PrimitiveDimensionType.md)<!-- -->; coordinateSet?: [TPCB\_PrimitiveDimensionCoordinateSet](../types/TPCB_PrimitiveDimensionCoordinateSet.md)<!-- -->; layer?: [TPCB\_LayersOfDimension](../types/TPCB_LayersOfDimension.md)<!-- -->; unit?: [ESYS\_Unit.MILLIMETER](../enums/ESYS_Unit.md) \| [ESYS\_Unit.CENTIMETER](../enums/ESYS_Unit.md) \| [ESYS\_Unit.INCH](../enums/ESYS_Unit.md) \| [ESYS\_Unit.MIL](../enums/ESYS_Unit.md)<!-- -->; lineWidth?: number; precision?: number; primitiveLock?: boolean }

</td><td>

Modify Parameter

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md) \| undefined&gt;

Dimension primitive object

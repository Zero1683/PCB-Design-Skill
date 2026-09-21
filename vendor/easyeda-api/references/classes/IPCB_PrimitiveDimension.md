# IPCB\_PrimitiveDimension class

Dimension primitive

## Signature

```typescript
class IPCB_PrimitiveDimension implements IPCB_Primitive
```
**Implements:** [IPCB\_Primitive](../interfaces/IPCB_Primitive.md)

## Remarks

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[done()](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getState\_CoordinateSet()](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

Get the property state: coordinate set

</td></tr>
<tr><td>

[getState\_DimensionType()](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

Get the property state: dimension type

</td></tr>
<tr><td>

[getState\_Layer()](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

Get the property state: Layer

</td></tr>
<tr><td>

[getState\_LineWidth()](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

Get the property state: Line width

</td></tr>
<tr><td>

[getState\_Precision()](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

Get the property state: precision

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveLock()](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

Get the property state: whether it is locked

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[getState\_TextFollow()](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

Get the property state: text follows

</td></tr>
<tr><td>

[getState\_Unit()](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

Get the property state: unit

</td></tr>
<tr><td>

[isAsync()](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_CoordinateSet(coordinateSet)](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: coordinate set

</td></tr>
<tr><td>

[setState\_DimensionType(dimensionType)](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: dimension type

</td></tr>
<tr><td>

[setState\_Layer(layer)](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Layer

</td></tr>
<tr><td>

[setState\_LineWidth(lineWidth)](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Line width

</td></tr>
<tr><td>

[setState\_Precision(precision)](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: precision

</td></tr>
<tr><td>

[setState\_PrimitiveLock(primitiveLock)](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is locked

</td></tr>
<tr><td>

[setState\_Unit(unit)](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: unit

</td></tr>
<tr><td>

[toAsync()](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./IPCB_PrimitiveDimension.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 方法详情

### done

# IPCB\_PrimitiveDimension.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<IPCB_PrimitiveDimension>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md)<!-- -->&gt;

Dimension primitive object

### getstate_coordinateset

# IPCB\_PrimitiveDimension.getState\_CoordinateSet() method

Get the property state: coordinate set

## Signature

```typescript
function getState_CoordinateSet(): TPCB_PrimitiveDimensionCoordinateSet;
```

## Returns

[TPCB\_PrimitiveDimensionCoordinateSet](../types/TPCB_PrimitiveDimensionCoordinateSet.md)

Coordinate set

### getstate_dimensiontype

# IPCB\_PrimitiveDimension.getState\_DimensionType() method

Get the property state: dimension type

## Signature

```typescript
function getState_DimensionType(): EPCB_PrimitiveDimensionType;
```

## Returns

[EPCB\_PrimitiveDimensionType](../enums/EPCB_PrimitiveDimensionType.md)

Dimension type

### getstate_layer

# IPCB\_PrimitiveDimension.getState\_Layer() method

Get the property state: Layer

## Signature

```typescript
function getState_Layer(): TPCB_LayersOfDimension;
```

## Returns

[TPCB\_LayersOfDimension](../types/TPCB_LayersOfDimension.md)

Layer

### getstate_linewidth

# IPCB\_PrimitiveDimension.getState\_LineWidth() method

Get the property state: Line width

## Signature

```typescript
function getState_LineWidth(): number;
```

## Returns

number

Line width

### getstate_precision

# IPCB\_PrimitiveDimension.getState\_Precision() method

Get the property state: precision

## Signature

```typescript
function getState_Precision(): number;
```

## Returns

number

Precision

### getstate_primitiveid

# IPCB\_PrimitiveDimension.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivelock

# IPCB\_PrimitiveDimension.getState\_PrimitiveLock() method

Get the property state: whether it is locked

## Signature

```typescript
function getState_PrimitiveLock(): boolean;
```

## Returns

boolean

Whether it is locked

### getstate_primitivetype

# IPCB\_PrimitiveDimension.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): EPCB_PrimitiveType;
```

## Returns

[EPCB\_PrimitiveType](../enums/EPCB_PrimitiveType.md)

Primitive type

### getstate_textfollow

# IPCB\_PrimitiveDimension.getState\_TextFollow() method

Get the property state: text follows

## Signature

```typescript
function getState_TextFollow(): 0 | 1;
```

## Returns

0 \| 1

Text follows

### getstate_unit

# IPCB\_PrimitiveDimension.getState\_Unit() method

Get the property state: unit

## Signature

```typescript
function getState_Unit():
	ESYS_Unit.MILLIMETER | ESYS_Unit.CENTIMETER | ESYS_Unit.INCH | ESYS_Unit.MIL;
```

## Returns

[ESYS\_Unit.MILLIMETER](../enums/ESYS_Unit.md) \| [ESYS\_Unit.CENTIMETER](../enums/ESYS_Unit.md) \| [ESYS\_Unit.INCH](../enums/ESYS_Unit.md) \| [ESYS\_Unit.MIL](../enums/ESYS_Unit.md)

Unit

### isasync

# IPCB\_PrimitiveDimension.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# IPCB\_PrimitiveDimension.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<IPCB_PrimitiveDimension>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md)<!-- -->&gt;

Dimension primitive object

### setstate_coordinateset

# IPCB\_PrimitiveDimension.setState\_CoordinateSet() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: coordinate set

## Signature

```typescript
function setState_CoordinateSet(
	coordinateSet: TPCB_PrimitiveDimensionCoordinateSet,
): IPCB_PrimitiveDimension;
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

coordinateSet

</td><td>

[TPCB\_PrimitiveDimensionCoordinateSet](../types/TPCB_PrimitiveDimensionCoordinateSet.md)

</td><td>

Coordinate set

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md)

Dimension primitive object

### setstate_dimensiontype

# IPCB\_PrimitiveDimension.setState\_DimensionType() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: dimension type

## Signature

```typescript
function setState_DimensionType(
	dimensionType: EPCB_PrimitiveDimensionType,
): IPCB_PrimitiveDimension;
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
</tbody></table>

## Returns

[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md)

Dimension primitive object

### setstate_layer

# IPCB\_PrimitiveDimension.setState\_Layer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Layer

## Signature

```typescript
function setState_Layer(layer: TPCB_LayersOfDimension): IPCB_PrimitiveDimension;
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

Layer

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md)

Dimension primitive object

### setstate_linewidth

# IPCB\_PrimitiveDimension.setState\_LineWidth() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Line width

## Signature

```typescript
function setState_LineWidth(lineWidth: number): IPCB_PrimitiveDimension;
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

lineWidth

</td><td>

number

</td><td>

Line width

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md)

Dimension primitive object

### setstate_precision

# IPCB\_PrimitiveDimension.setState\_Precision() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: precision

## Signature

```typescript
function setState_Precision(precision: number): IPCB_PrimitiveDimension;
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

precision

</td><td>

number

</td><td>

Precision

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md)

Dimension primitive object

### setstate_primitivelock

# IPCB\_PrimitiveDimension.setState\_PrimitiveLock() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is locked

## Signature

```typescript
function setState_PrimitiveLock(primitiveLock: boolean): IPCB_PrimitiveDimension;
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

primitiveLock

</td><td>

boolean

</td><td>

Whether it is locked

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md)

Dimension primitive object

### setstate_unit

# IPCB\_PrimitiveDimension.setState\_Unit() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: unit

## Signature

```typescript
function setState_Unit(
	unit: ESYS_Unit.MILLIMETER | ESYS_Unit.CENTIMETER | ESYS_Unit.INCH | ESYS_Unit.MIL,
): IPCB_PrimitiveDimension;
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

unit

</td><td>

[ESYS\_Unit.MILLIMETER](../enums/ESYS_Unit.md) \| [ESYS\_Unit.CENTIMETER](../enums/ESYS_Unit.md) \| [ESYS\_Unit.INCH](../enums/ESYS_Unit.md) \| [ESYS\_Unit.MIL](../enums/ESYS_Unit.md)

</td><td>

Unit

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md)

Dimension primitive object

### toasync

# IPCB\_PrimitiveDimension.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): IPCB_PrimitiveDimension;
```

## Returns

[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md)

Dimension primitive object

### tosync

# IPCB\_PrimitiveDimension.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): IPCB_PrimitiveDimension;
```

## Returns

[IPCB\_PrimitiveDimension](./IPCB_PrimitiveDimension.md)

Dimension primitive object

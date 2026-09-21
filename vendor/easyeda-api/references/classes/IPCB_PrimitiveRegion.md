# IPCB\_PrimitiveRegion class

Region primitive

## Signature

```typescript
class IPCB_PrimitiveRegion implements IPCB_Primitive
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

[convertToFill()](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Convert to: fill primitive

</td></tr>
<tr><td>

[convertToPolyline()](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Convert to: polyline primitive

</td></tr>
<tr><td>

[convertToPour()](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Convert to: Copper border primitive

</td></tr>
<tr><td>

[done()](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getState\_ComplexPolygon()](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

Get the property state: complex polygon

</td></tr>
<tr><td>

[getState\_Layer()](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

Get the property state: Layer

</td></tr>
<tr><td>

[getState\_LineWidth()](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

Get the property state: Line width

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveLock()](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

Get the property state: whether it is locked

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[getState\_RegionName()](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

Get the property state: region name

</td></tr>
<tr><td>

[getState\_RuleType()](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

Get the property state: region rule type

</td></tr>
<tr><td>

[isAsync()](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_ComplexPolygon(complexPolygon)](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: complex polygon

</td></tr>
<tr><td>

[setState\_Layer(layer)](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Layer

</td></tr>
<tr><td>

[setState\_LineWidth(lineWidth)](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Line width

</td></tr>
<tr><td>

[setState\_PrimitiveLock(primitiveLock)](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is locked

</td></tr>
<tr><td>

[setState\_RegionName(regionName)](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: region name

</td></tr>
<tr><td>

[setState\_RuleType(ruleType)](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: region rule type

</td></tr>
<tr><td>

[toAsync()](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./IPCB_PrimitiveRegion.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 方法详情

### converttofill

# IPCB\_PrimitiveRegion.convertToFill() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Convert to: fill primitive

## Signature

```typescript
function convertToFill(): Promise<IPCB_PrimitiveFill>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)<!-- -->&gt;

Fill primitive object

### converttopolyline

# IPCB\_PrimitiveRegion.convertToPolyline() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Convert to: polyline primitive

## Signature

```typescript
function convertToPolyline(): Promise<IPCB_PrimitivePolyline>;
```

## Returns

Promise&lt;[IPCB\_PrimitivePolyline](./IPCB_PrimitivePolyline.md)<!-- -->&gt;

Polyline primitive object

### converttopour

# IPCB\_PrimitiveRegion.convertToPour() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Convert to: Copper border primitive

## Signature

```typescript
function convertToPour(): Promise<IPCB_PrimitivePour>;
```

## Returns

Promise&lt;[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)<!-- -->&gt;

Copper border primitive object

### done

# IPCB\_PrimitiveRegion.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<IPCB_PrimitiveRegion>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md)<!-- -->&gt;

Region primitive object

### getstate_complexpolygon

# IPCB\_PrimitiveRegion.getState\_ComplexPolygon() method

Get the property state: complex polygon

## Signature

```typescript
function getState_ComplexPolygon(): IPCB_Polygon;
```

## Returns

[IPCB\_Polygon](./IPCB_Polygon.md)

Complex polygon

### getstate_layer

# IPCB\_PrimitiveRegion.getState\_Layer() method

Get the property state: Layer

## Signature

```typescript
function getState_Layer(): TPCB_LayersOfRegion;
```

## Returns

[TPCB\_LayersOfRegion](../types/TPCB_LayersOfRegion.md)

Layer

### getstate_linewidth

# IPCB\_PrimitiveRegion.getState\_LineWidth() method

Get the property state: Line width

## Signature

```typescript
function getState_LineWidth(): number;
```

## Returns

number

Line width

### getstate_primitiveid

# IPCB\_PrimitiveRegion.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivelock

# IPCB\_PrimitiveRegion.getState\_PrimitiveLock() method

Get the property state: whether it is locked

## Signature

```typescript
function getState_PrimitiveLock(): boolean;
```

## Returns

boolean

Whether it is locked

### getstate_primitivetype

# IPCB\_PrimitiveRegion.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): EPCB_PrimitiveType;
```

## Returns

[EPCB\_PrimitiveType](../enums/EPCB_PrimitiveType.md)

Primitive type

### getstate_regionname

# IPCB\_PrimitiveRegion.getState\_RegionName() method

Get the property state: region name

## Signature

```typescript
function getState_RegionName(): string | undefined;
```

## Returns

string \| undefined

Region name

### getstate_ruletype

# IPCB\_PrimitiveRegion.getState\_RuleType() method

Get the property state: region rule type

## Signature

```typescript
function getState_RuleType(): Array<EPCB_PrimitiveRegionRuleType>;
```

## Returns

Array&lt;[EPCB\_PrimitiveRegionRuleType](../enums/EPCB_PrimitiveRegionRuleType.md)<!-- -->&gt;

Region rule type

### isasync

# IPCB\_PrimitiveRegion.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# IPCB\_PrimitiveRegion.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<IPCB_PrimitiveRegion>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md)<!-- -->&gt;

Region primitive object

### setstate_complexpolygon

# IPCB\_PrimitiveRegion.setState\_ComplexPolygon() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: complex polygon

## Signature

```typescript
function setState_ComplexPolygon(complexPolygon: IPCB_Polygon): IPCB_PrimitiveRegion;
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

complexPolygon

</td><td>

[IPCB\_Polygon](./IPCB_Polygon.md)

</td><td>

Complex polygon

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md)

Region primitive object

### setstate_layer

# IPCB\_PrimitiveRegion.setState\_Layer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Layer

## Signature

```typescript
function setState_Layer(layer: TPCB_LayersOfRegion): IPCB_PrimitiveRegion;
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
</tbody></table>

## Returns

[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md)

Region primitive object

### setstate_linewidth

# IPCB\_PrimitiveRegion.setState\_LineWidth() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Line width

## Signature

```typescript
function setState_LineWidth(lineWidth: number): IPCB_PrimitiveRegion;
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

[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md)

Region primitive object

### setstate_primitivelock

# IPCB\_PrimitiveRegion.setState\_PrimitiveLock() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is locked

## Signature

```typescript
function setState_PrimitiveLock(primitiveLock: boolean): IPCB_PrimitiveRegion;
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

[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md)

Region primitive object

### setstate_regionname

# IPCB\_PrimitiveRegion.setState\_RegionName() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: region name

## Signature

```typescript
function setState_RegionName(regionName?: string): IPCB_PrimitiveRegion;
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

regionName

</td><td>

string

</td><td>

_(Optional)_ Region name

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md)

Region primitive object

## Remarks

Only valid when `ruleType` is [EPCB\_PrimitiveRegionRuleType.FOLLOW\_REGION\_RULE](../enums/EPCB_PrimitiveRegionRuleType.md)<!-- -->, used to match region DRC rules

If `ruleType` is [EPCB\_PrimitiveRegionRuleType.FOLLOW\_REGION\_RULE](../enums/EPCB_PrimitiveRegionRuleType.md) but `regionName` is empty, the system will automatically assign a name

### setstate_ruletype

# IPCB\_PrimitiveRegion.setState\_RuleType() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: region rule type

## Signature

```typescript
function setState_RuleType(ruleType: Array<EPCB_PrimitiveRegionRuleType>): IPCB_PrimitiveRegion;
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

ruleType

</td><td>

Array&lt;[EPCB\_PrimitiveRegionRuleType](../enums/EPCB_PrimitiveRegionRuleType.md)<!-- -->&gt;

</td><td>

Region rule type

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md)

Region primitive object

### toasync

# IPCB\_PrimitiveRegion.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): IPCB_PrimitiveRegion;
```

## Returns

[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md)

Region primitive object

### tosync

# IPCB\_PrimitiveRegion.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): IPCB_PrimitiveRegion;
```

## Returns

[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md)

Region primitive object

# IPCB\_PrimitivePour class

Copper border primitive

## Signature

```typescript
class IPCB_PrimitivePour implements IPCB_Primitive
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

[convertToFill()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Convert to: fill primitive (default is the fill region)

</td></tr>
<tr><td>

[convertToPolyline()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Convert to: polyline primitive (default is the line)

</td></tr>
<tr><td>

[convertToRegion()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Convert to: region primitive (default is the forbidden region)

</td></tr>
<tr><td>

[done()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getCopperRegion()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Get the copper fill primitive of the copper region

</td></tr>
<tr><td>

[getState\_ComplexPolygon()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

Get the property state: complex polygon

</td></tr>
<tr><td>

[getState\_Layer()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

Get the property state: Layer

</td></tr>
<tr><td>

[getState\_LineWidth()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

Get the property state: Line width

</td></tr>
<tr><td>

[getState\_Net()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

Get the property state: net name

</td></tr>
<tr><td>

[getState\_PourFillMethod()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

Get the property state: copper fill method

</td></tr>
<tr><td>

[getState\_PourName()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

Get the property state: copper border name

</td></tr>
<tr><td>

[getState\_PourPriority()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

Get the property state: copper priority

</td></tr>
<tr><td>

[getState\_PreserveSilos()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

Get the property state: whether to keep islands

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveLock()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

Get the property state: whether it is locked

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[isAsync()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[rebuildCopperRegion()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Rebuild the copper fill of the copper region

</td></tr>
<tr><td>

[reset()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_ComplexPolygon(complexPolygon)](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: complex polygon

</td></tr>
<tr><td>

[setState\_Layer(layer)](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Layer

</td></tr>
<tr><td>

[setState\_LineWidth(lineWidth)](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Line width

</td></tr>
<tr><td>

[setState\_Net(net)](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: net name

</td></tr>
<tr><td>

[setState\_PourFillMethod(pourFillMethod)](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: copper fill method

</td></tr>
<tr><td>

[setState\_PourName(pourName)](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: copper border name

</td></tr>
<tr><td>

[setState\_PourPriority(pourPriority)](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: copper priority

</td></tr>
<tr><td>

[setState\_PreserveSilos(preserveSilos)](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether to keep islands

</td></tr>
<tr><td>

[setState\_PrimitiveLock(primitiveLock)](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is locked

</td></tr>
<tr><td>

[toAsync()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./IPCB_PrimitivePour.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 方法详情

### converttofill

# IPCB\_PrimitivePour.convertToFill() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Convert to: fill primitive (default is the fill region)

## Signature

```typescript
function convertToFill(): Promise<IPCB_PrimitiveFill>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)<!-- -->&gt;

Fill primitive object

### converttopolyline

# IPCB\_PrimitivePour.convertToPolyline() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Convert to: polyline primitive (default is the line)

## Signature

```typescript
function convertToPolyline(): Promise<IPCB_PrimitivePolyline>;
```

## Returns

Promise&lt;[IPCB\_PrimitivePolyline](./IPCB_PrimitivePolyline.md)<!-- -->&gt;

Polyline primitive object

### converttoregion

# IPCB\_PrimitivePour.convertToRegion() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Convert to: region primitive (default is the forbidden region)

## Signature

```typescript
function convertToRegion(): Promise<IPCB_PrimitiveRegion>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveRegion](./IPCB_PrimitiveRegion.md)<!-- -->&gt;

Region primitive object

### done

# IPCB\_PrimitivePour.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<IPCB_PrimitivePour>;
```

## Returns

Promise&lt;[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)<!-- -->&gt;

Copper border primitive object

### getcopperregion

# IPCB\_PrimitivePour.getCopperRegion() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the copper fill primitive of the copper region

## Signature

```typescript
function getCopperRegion(): Promise<IPCB_PrimitivePoured | undefined>;
```

## Returns

Promise&lt;[IPCB\_PrimitivePoured](./IPCB_PrimitivePoured.md) \| undefined&gt;

The copper fill primitive. If no associated copper fill primitive exists, `undefined` is returned

### getstate_complexpolygon

# IPCB\_PrimitivePour.getState\_ComplexPolygon() method

Get the property state: complex polygon

## Signature

```typescript
function getState_ComplexPolygon(): IPCB_Polygon;
```

## Returns

[IPCB\_Polygon](./IPCB_Polygon.md)

Complex polygon

### getstate_layer

# IPCB\_PrimitivePour.getState\_Layer() method

Get the property state: Layer

## Signature

```typescript
function getState_Layer(): TPCB_LayersOfCopper;
```

## Returns

[TPCB\_LayersOfCopper](../types/TPCB_LayersOfCopper.md)

Layer

### getstate_linewidth

# IPCB\_PrimitivePour.getState\_LineWidth() method

Get the property state: Line width

## Signature

```typescript
function getState_LineWidth(): number;
```

## Returns

number

Line width

### getstate_net

# IPCB\_PrimitivePour.getState\_Net() method

Get the property state: net name

## Signature

```typescript
function getState_Net(): string;
```

## Returns

string

Net name

### getstate_pourfillmethod

# IPCB\_PrimitivePour.getState\_PourFillMethod() method

Get the property state: copper fill method

## Signature

```typescript
function getState_PourFillMethod(): any;
```

## Returns

any

Copper fill method

### getstate_pourname

# IPCB\_PrimitivePour.getState\_PourName() method

Get the property state: copper border name

## Signature

```typescript
function getState_PourName(): string;
```

## Returns

string

Copper border name

### getstate_pourpriority

# IPCB\_PrimitivePour.getState\_PourPriority() method

Get the property state: copper priority

## Signature

```typescript
function getState_PourPriority(): number;
```

## Returns

number

Copper priority

### getstate_preservesilos

# IPCB\_PrimitivePour.getState\_PreserveSilos() method

Get the property state: whether to keep islands

## Signature

```typescript
function getState_PreserveSilos(): boolean;
```

## Returns

boolean

Whether to keep islands

### getstate_primitiveid

# IPCB\_PrimitivePour.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivelock

# IPCB\_PrimitivePour.getState\_PrimitiveLock() method

Get the property state: whether it is locked

## Signature

```typescript
function getState_PrimitiveLock(): boolean;
```

## Returns

boolean

Whether it is locked

### getstate_primitivetype

# IPCB\_PrimitivePour.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): EPCB_PrimitiveType;
```

## Returns

[EPCB\_PrimitiveType](../enums/EPCB_PrimitiveType.md)

Primitive type

### isasync

# IPCB\_PrimitivePour.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### rebuildcopperregion

# IPCB\_PrimitivePour.rebuildCopperRegion() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Rebuild the copper fill of the copper region

## Signature

```typescript
function rebuildCopperRegion(): Promise<IPCB_PrimitivePoured | undefined>;
```

## Returns

Promise&lt;[IPCB\_PrimitivePoured](./IPCB_PrimitivePoured.md) \| undefined&gt;

The copper fill primitive. If no copper fill primitive is rebuilt, `undefined` is returned

### reset

# IPCB\_PrimitivePour.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<IPCB_PrimitivePour>;
```

## Returns

Promise&lt;[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)<!-- -->&gt;

Copper border primitive object

### setstate_complexpolygon

# IPCB\_PrimitivePour.setState\_ComplexPolygon() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: complex polygon

## Signature

```typescript
function setState_ComplexPolygon(complexPolygon: IPCB_Polygon): IPCB_PrimitivePour;
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

[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)

Copper border primitive object

### setstate_layer

# IPCB\_PrimitivePour.setState\_Layer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Layer

## Signature

```typescript
function setState_Layer(layer: TPCB_LayersOfCopper): IPCB_PrimitivePour;
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

[TPCB\_LayersOfCopper](../types/TPCB_LayersOfCopper.md)

</td><td>

Layer

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)

Copper border primitive object

### setstate_linewidth

# IPCB\_PrimitivePour.setState\_LineWidth() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Line width

## Signature

```typescript
function setState_LineWidth(lineWidth: number): IPCB_PrimitivePour;
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

[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)

Copper border primitive object

### setstate_net

# IPCB\_PrimitivePour.setState\_Net() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: net name

## Signature

```typescript
function setState_Net(net: string): IPCB_PrimitivePour;
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
</tbody></table>

## Returns

[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)

Copper border primitive object

### setstate_pourfillmethod

# IPCB\_PrimitivePour.setState\_PourFillMethod() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: copper fill method

## Signature

```typescript
function setState_PourFillMethod(pourFillMethod: EPCB_PrimitivePourFillMethod): IPCB_PrimitivePour;
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

pourFillMethod

</td><td>

[EPCB\_PrimitivePourFillMethod](../enums/EPCB_PrimitivePourFillMethod.md)

</td><td>

Copper fill method

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)

Copper border primitive object

### setstate_pourname

# IPCB\_PrimitivePour.setState\_PourName() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: copper border name

## Signature

```typescript
function setState_PourName(pourName: string): IPCB_PrimitivePour;
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

pourName

</td><td>

string

</td><td>

Copper border name

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)

Copper border primitive object

### setstate_pourpriority

# IPCB\_PrimitivePour.setState\_PourPriority() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: copper priority

## Signature

```typescript
function setState_PourPriority(pourPriority: number): IPCB_PrimitivePour;
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

pourPriority

</td><td>

number

</td><td>

Copper priority

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)

Copper border primitive object

### setstate_preservesilos

# IPCB\_PrimitivePour.setState\_PreserveSilos() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether to keep islands

## Signature

```typescript
function setState_PreserveSilos(preserveSilos: boolean): IPCB_PrimitivePour;
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

preserveSilos

</td><td>

boolean

</td><td>

Whether to keep islands

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)

Copper border primitive object

### setstate_primitivelock

# IPCB\_PrimitivePour.setState\_PrimitiveLock() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is locked

## Signature

```typescript
function setState_PrimitiveLock(primitiveLock: boolean): IPCB_PrimitivePour;
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

[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)

Copper border primitive object

### toasync

# IPCB\_PrimitivePour.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): IPCB_PrimitivePour;
```

## Returns

[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)

Copper border primitive object

### tosync

# IPCB\_PrimitivePour.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): IPCB_PrimitivePour;
```

## Returns

[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)

Copper border primitive object

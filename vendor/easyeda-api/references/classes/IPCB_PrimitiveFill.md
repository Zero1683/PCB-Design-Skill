# IPCB\_PrimitiveFill class

Fill primitive

## Signature

```typescript
class IPCB_PrimitiveFill implements IPCB_Primitive
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

[convertToPolyline()](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Convert to: polyline primitive

</td></tr>
<tr><td>

[convertToPour()](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Convert to: Copper border primitive

</td></tr>
<tr><td>

[convertToRegion()](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Convert to: region primitive (default is the forbidden region)

</td></tr>
<tr><td>

[done()](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getState\_ComplexPolygon()](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

Get the property state: complex polygon

</td></tr>
<tr><td>

[getState\_FillMode()](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

Get the property state: fill mode

</td></tr>
<tr><td>

[getState\_Layer()](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

Get the property state: Layer

</td></tr>
<tr><td>

[getState\_LineWidth()](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

Get the property state: Line width

</td></tr>
<tr><td>

[getState\_Net()](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

Get the property state: net name

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveLock()](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

Get the property state: whether it is locked

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[isAsync()](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_ComplexPolygon(complexPolygon)](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: complex polygon

</td></tr>
<tr><td>

[setState\_FillMode(fillMode)](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: fill mode

</td></tr>
<tr><td>

[setState\_Layer(layer)](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Layer

</td></tr>
<tr><td>

[setState\_LineWidth(lineWidth)](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Line width

</td></tr>
<tr><td>

[setState\_Net(net)](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: net name

</td></tr>
<tr><td>

[setState\_PrimitiveLock(primitiveLock)](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is locked

</td></tr>
<tr><td>

[toAsync()](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./IPCB_PrimitiveFill.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 方法详情

### converttopolyline

# IPCB\_PrimitiveFill.convertToPolyline() method

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

# IPCB\_PrimitiveFill.convertToPour() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Convert to: Copper border primitive

## Signature

```typescript
function convertToPour(): Promise<IPCB_PrimitivePour>;
```

## Returns

Promise&lt;[IPCB\_PrimitivePour](./IPCB_PrimitivePour.md)<!-- -->&gt;

Copper border primitive object

### converttoregion

# IPCB\_PrimitiveFill.convertToRegion() method

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

# IPCB\_PrimitiveFill.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<IPCB_PrimitiveFill>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)<!-- -->&gt;

Fill primitive object

### getstate_complexpolygon

# IPCB\_PrimitiveFill.getState\_ComplexPolygon() method

Get the property state: complex polygon

## Signature

```typescript
function getState_ComplexPolygon(): IPCB_Polygon;
```

## Returns

[IPCB\_Polygon](./IPCB_Polygon.md)

Complex polygon

### getstate_fillmode

# IPCB\_PrimitiveFill.getState\_FillMode() method

Get the property state: fill mode

## Signature

```typescript
function getState_FillMode(): EPCB_PrimitiveFillMode | undefined;
```

## Returns

[EPCB\_PrimitiveFillMode](../enums/EPCB_PrimitiveFillMode.md) \| undefined

Fill mode

### getstate_layer

# IPCB\_PrimitiveFill.getState\_Layer() method

Get the property state: Layer

## Signature

```typescript
function getState_Layer(): TPCB_LayersOfFill;
```

## Returns

[TPCB\_LayersOfFill](../types/TPCB_LayersOfFill.md)

Layer

### getstate_linewidth

# IPCB\_PrimitiveFill.getState\_LineWidth() method

Get the property state: Line width

## Signature

```typescript
function getState_LineWidth(): number;
```

## Returns

number

Line width

### getstate_net

# IPCB\_PrimitiveFill.getState\_Net() method

Get the property state: net name

## Signature

```typescript
function getState_Net(): string | undefined;
```

## Returns

string \| undefined

Net name

### getstate_primitiveid

# IPCB\_PrimitiveFill.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivelock

# IPCB\_PrimitiveFill.getState\_PrimitiveLock() method

Get the property state: whether it is locked

## Signature

```typescript
function getState_PrimitiveLock(): boolean;
```

## Returns

boolean

Whether it is locked

### getstate_primitivetype

# IPCB\_PrimitiveFill.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): EPCB_PrimitiveType;
```

## Returns

[EPCB\_PrimitiveType](../enums/EPCB_PrimitiveType.md)

Primitive type

### isasync

# IPCB\_PrimitiveFill.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# IPCB\_PrimitiveFill.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<IPCB_PrimitiveFill>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)<!-- -->&gt;

Fill primitive object

### setstate_complexpolygon

# IPCB\_PrimitiveFill.setState\_ComplexPolygon() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: complex polygon

## Signature

```typescript
function setState_ComplexPolygon(complexPolygon: IPCB_Polygon): IPCB_PrimitiveFill;
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

[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)

Fill primitive object

### setstate_fillmode

# IPCB\_PrimitiveFill.setState\_FillMode() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: fill mode

## Signature

```typescript
function setState_FillMode(fillMode: EPCB_PrimitiveFillMode): IPCB_PrimitiveFill;
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

fillMode

</td><td>

[EPCB\_PrimitiveFillMode](../enums/EPCB_PrimitiveFillMode.md)

</td><td>

Fill mode

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)

Fill primitive object

### setstate_layer

# IPCB\_PrimitiveFill.setState\_Layer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Layer

## Signature

```typescript
function setState_Layer(layer: TPCB_LayersOfFill): IPCB_PrimitiveFill;
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
</tbody></table>

## Returns

[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)

Fill primitive object

### setstate_linewidth

# IPCB\_PrimitiveFill.setState\_LineWidth() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Line width

## Signature

```typescript
function setState_LineWidth(lineWidth: number): IPCB_PrimitiveFill;
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

[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)

Fill primitive object

### setstate_net

# IPCB\_PrimitiveFill.setState\_Net() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: net name

## Signature

```typescript
function setState_Net(net: string): IPCB_PrimitiveFill;
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

[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)

Fill primitive object

### setstate_primitivelock

# IPCB\_PrimitiveFill.setState\_PrimitiveLock() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is locked

## Signature

```typescript
function setState_PrimitiveLock(primitiveLock: boolean): IPCB_PrimitiveFill;
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

[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)

Fill primitive object

### toasync

# IPCB\_PrimitiveFill.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): IPCB_PrimitiveFill;
```

## Returns

[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)

Fill primitive object

### tosync

# IPCB\_PrimitiveFill.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): IPCB_PrimitiveFill;
```

## Returns

[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)

Fill primitive object

# IPCB\_PrimitiveArc class

Arc line primitive

## Signature

```typescript
class IPCB_PrimitiveArc implements IPCB_Primitive
```
**Implements:** [IPCB\_Primitive](../interfaces/IPCB_Primitive.md)

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

[done()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getAdjacentPrimitives()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Get Adjacent primitive objects

</td></tr>
<tr><td>

[getEntireTrack(includeVias)](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Get the entire wire

</td></tr>
<tr><td>

[getEntireTrack(includeVias)](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Get the entire wire

</td></tr>
<tr><td>

[getState\_ArcAngle()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: arc angle

</td></tr>
<tr><td>

[getState\_EndX()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: end position X

</td></tr>
<tr><td>

[getState\_EndY()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: end position Y

</td></tr>
<tr><td>

[getState\_InteractiveMode()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: interaction mode

</td></tr>
<tr><td>

[getState\_Layer()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: Layer

</td></tr>
<tr><td>

[getState\_LineWidth()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: Line width

</td></tr>
<tr><td>

[getState\_Net()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: net name

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveLock()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: whether it is locked

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[getState\_StartX()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: start position X

</td></tr>
<tr><td>

[getState\_StartY()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: start position Y

</td></tr>
<tr><td>

[isAsync()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_ArcAngle(arcAngle)](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: arc angle

</td></tr>
<tr><td>

[setState\_EndX(endX)](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: end position X

</td></tr>
<tr><td>

[setState\_EndY(endY)](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: end position Y

</td></tr>
<tr><td>

[setState\_InteractiveMode(interactiveMode)](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: interaction mode

</td></tr>
<tr><td>

[setState\_Layer(layer)](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Layer

</td></tr>
<tr><td>

[setState\_LineWidth(lineWidth)](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Line width

</td></tr>
<tr><td>

[setState\_Net(net)](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: net name

</td></tr>
<tr><td>

[setState\_PrimitiveLock(primitiveLock)](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is locked

</td></tr>
<tr><td>

[setState\_StartX(startX)](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: start position X

</td></tr>
<tr><td>

[setState\_StartY(startY)](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: start position Y

</td></tr>
<tr><td>

[toAsync()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./IPCB_PrimitiveArc.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 方法详情

### done

# IPCB\_PrimitiveArc.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<IPCB_PrimitiveArc>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)<!-- -->&gt;

Arc line primitive object

### getadjacentprimitives

# IPCB\_PrimitiveArc.getAdjacentPrimitives() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Adjacent primitive objects

## Signature

```typescript
function getAdjacentPrimitives(): Promise<
	Array<IPCB_PrimitiveLine | IPCB_PrimitiveVia | IPCB_PrimitiveArc>
>;
```

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveLine](./IPCB_PrimitiveLine.md) \| [IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md) \| [IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)<!-- -->&gt;&gt;

Adjacent line, via, and arc-line primitive objects

## Remarks

It will get the line, via, and arc-line primitive objects directly connected to the arc line

### getentiretrack

# IPCB\_PrimitiveArc.getEntireTrack() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the entire wire

## Signature

```typescript
function getEntireTrack(includeVias: false): Promise<Array<IPCB_PrimitiveLine | IPCB_PrimitiveArc>>;
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

includeVias

</td><td>

false

</td><td>

Whether to include the vias at both ends of the wire

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveLine](./IPCB_PrimitiveLine.md) \| [IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)<!-- -->&gt;&gt;

All lines and arc lines in the entire wire

### getentiretrack_1

# IPCB\_PrimitiveArc.getEntireTrack() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the entire wire

## Signature

```typescript
function getEntireTrack(
	includeVias: true,
): Promise<Array<IPCB_PrimitiveLine | IPCB_PrimitiveArc | IPCB_PrimitiveVia>>;
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

includeVias

</td><td>

true

</td><td>

Whether to include the vias at both ends of the wire

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveLine](./IPCB_PrimitiveLine.md) \| [IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md) \| [IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md)<!-- -->&gt;&gt;

All lines and arc lines in the entire wire, as well as the vias connected at both ends (if any)

### getstate_arcangle

# IPCB\_PrimitiveArc.getState\_ArcAngle() method

Get the property state: arc angle

## Signature

```typescript
function getState_ArcAngle(): number;
```

## Returns

number

Arc angle

### getstate_endx

# IPCB\_PrimitiveArc.getState\_EndX() method

Get the property state: end position X

## Signature

```typescript
function getState_EndX(): number;
```

## Returns

number

End position X

### getstate_endy

# IPCB\_PrimitiveArc.getState\_EndY() method

Get the property state: end position Y

## Signature

```typescript
function getState_EndY(): number;
```

## Returns

number

End position Y

### getstate_interactivemode

# IPCB\_PrimitiveArc.getState\_InteractiveMode() method

Get the property state: interaction mode

## Signature

```typescript
function getState_InteractiveMode(): EPCB_PrimitiveArcInteractiveMode;
```

## Returns

[EPCB\_PrimitiveArcInteractiveMode](../enums/EPCB_PrimitiveArcInteractiveMode.md)

Interaction mode

### getstate_layer

# IPCB\_PrimitiveArc.getState\_Layer() method

Get the property state: Layer

## Signature

```typescript
function getState_Layer(): TPCB_LayersOfLine;
```

## Returns

[TPCB\_LayersOfLine](../types/TPCB_LayersOfLine.md)

Layer

### getstate_linewidth

# IPCB\_PrimitiveArc.getState\_LineWidth() method

Get the property state: Line width

## Signature

```typescript
function getState_LineWidth(): number;
```

## Returns

number

Line width

### getstate_net

# IPCB\_PrimitiveArc.getState\_Net() method

Get the property state: net name

## Signature

```typescript
function getState_Net(): string;
```

## Returns

string

Net name

### getstate_primitiveid

# IPCB\_PrimitiveArc.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivelock

# IPCB\_PrimitiveArc.getState\_PrimitiveLock() method

Get the property state: whether it is locked

## Signature

```typescript
function getState_PrimitiveLock(): boolean;
```

## Returns

boolean

Whether it is locked

### getstate_primitivetype

# IPCB\_PrimitiveArc.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): EPCB_PrimitiveType;
```

## Returns

[EPCB\_PrimitiveType](../enums/EPCB_PrimitiveType.md)

Primitive type

### getstate_startx

# IPCB\_PrimitiveArc.getState\_StartX() method

Get the property state: start position X

## Signature

```typescript
function getState_StartX(): number;
```

## Returns

number

Start position X

### getstate_starty

# IPCB\_PrimitiveArc.getState\_StartY() method

Get the property state: start position Y

## Signature

```typescript
function getState_StartY(): number;
```

## Returns

number

Start position Y

### isasync

# IPCB\_PrimitiveArc.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# IPCB\_PrimitiveArc.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<IPCB_PrimitiveArc>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)<!-- -->&gt;

Arc line primitive object

### setstate_arcangle

# IPCB\_PrimitiveArc.setState\_ArcAngle() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: arc angle

## Signature

```typescript
function setState_ArcAngle(arcAngle: number): IPCB_PrimitiveArc;
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

arcAngle

</td><td>

number

</td><td>

Arc angle

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)

Arc line primitive object

### setstate_endx

# IPCB\_PrimitiveArc.setState\_EndX() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: end position X

## Signature

```typescript
function setState_EndX(endX: number): IPCB_PrimitiveArc;
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

endX

</td><td>

number

</td><td>

End position X

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)

Arc line primitive object

### setstate_endy

# IPCB\_PrimitiveArc.setState\_EndY() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: end position Y

## Signature

```typescript
function setState_EndY(endY: number): IPCB_PrimitiveArc;
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

endY

</td><td>

number

</td><td>

End position Y

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)

Arc line primitive object

### setstate_interactivemode

# IPCB\_PrimitiveArc.setState\_InteractiveMode() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: interaction mode

## Signature

```typescript
function setState_InteractiveMode(
	interactiveMode: EPCB_PrimitiveArcInteractiveMode,
): IPCB_PrimitiveArc;
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

interactiveMode

</td><td>

[EPCB\_PrimitiveArcInteractiveMode](../enums/EPCB_PrimitiveArcInteractiveMode.md)

</td><td>

Interaction mode

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)

Arc line primitive object

### setstate_layer

# IPCB\_PrimitiveArc.setState\_Layer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Layer

## Signature

```typescript
function setState_Layer(layer: TPCB_LayersOfLine): IPCB_PrimitiveArc;
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

[TPCB\_LayersOfLine](../types/TPCB_LayersOfLine.md)

</td><td>

Layer

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)

Arc line primitive object

### setstate_linewidth

# IPCB\_PrimitiveArc.setState\_LineWidth() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Line width

## Signature

```typescript
function setState_LineWidth(lineWidth: number): IPCB_PrimitiveArc;
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

[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)

Arc line primitive object

### setstate_net

# IPCB\_PrimitiveArc.setState\_Net() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: net name

## Signature

```typescript
function setState_Net(net: string): IPCB_PrimitiveArc;
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

[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)

Arc line primitive object

### setstate_primitivelock

# IPCB\_PrimitiveArc.setState\_PrimitiveLock() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is locked

## Signature

```typescript
function setState_PrimitiveLock(primitiveLock: boolean): IPCB_PrimitiveArc;
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

[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)

Arc line primitive object

### setstate_startx

# IPCB\_PrimitiveArc.setState\_StartX() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: start position X

## Signature

```typescript
function setState_StartX(startX: number): IPCB_PrimitiveArc;
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

startX

</td><td>

number

</td><td>

Start position X

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)

Arc line primitive object

### setstate_starty

# IPCB\_PrimitiveArc.setState\_StartY() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: start position Y

## Signature

```typescript
function setState_StartY(startY: number): IPCB_PrimitiveArc;
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

startY

</td><td>

number

</td><td>

Start position Y

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)

Arc line primitive object

### toasync

# IPCB\_PrimitiveArc.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): IPCB_PrimitiveArc;
```

## Returns

[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)

Arc line primitive object

### tosync

# IPCB\_PrimitiveArc.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): IPCB_PrimitiveArc;
```

## Returns

[IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)

Arc line primitive object

# ISCH\_PrimitiveArc class

Arc primitive

## Signature

```typescript
class ISCH_PrimitiveArc implements ISCH_Primitive
```
**Implements:** [ISCH\_Primitive](../interfaces/ISCH_Primitive.md)

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

[done()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getState\_Color()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: color

</td></tr>
<tr><td>

[getState\_EndX()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: end point X

</td></tr>
<tr><td>

[getState\_EndY()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: end point Y

</td></tr>
<tr><td>

[getState\_FillColor()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: fill color

</td></tr>
<tr><td>

[getState\_LineType()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: line type

</td></tr>
<tr><td>

[getState\_LineWidth()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: Line width

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[getState\_ReferenceX()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: reference point X

</td></tr>
<tr><td>

[getState\_ReferenceY()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: reference point Y

</td></tr>
<tr><td>

[getState\_StartX()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: start point X

</td></tr>
<tr><td>

[getState\_StartY()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

Get the property state: start point Y

</td></tr>
<tr><td>

[isAsync()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_Color(color)](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: color

</td></tr>
<tr><td>

[setState\_EndX(endX)](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: end point X

</td></tr>
<tr><td>

[setState\_EndY(endY)](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: end point Y

</td></tr>
<tr><td>

[setState\_FillColor(fillColor)](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: fill color

</td></tr>
<tr><td>

[setState\_LineType(lineType)](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: line type

</td></tr>
<tr><td>

[setState\_LineWidth(lineWidth)](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Line width

</td></tr>
<tr><td>

[setState\_ReferenceX(referenceX)](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: reference point X

</td></tr>
<tr><td>

[setState\_ReferenceY(referenceY)](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: reference point Y

</td></tr>
<tr><td>

[setState\_StartX(startX)](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: start point X

</td></tr>
<tr><td>

[setState\_StartY(startY)](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: start point Y

</td></tr>
<tr><td>

[toAsync()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./ISCH_PrimitiveArc.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 方法详情

### done

# ISCH\_PrimitiveArc.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<ISCH_PrimitiveArc>;
```

## Returns

Promise&lt;[ISCH\_PrimitiveArc](./ISCH_PrimitiveArc.md)<!-- -->&gt;

Arc primitive object

### getstate_color

# ISCH\_PrimitiveArc.getState\_Color() method

Get the property state: color

## Signature

```typescript
function getState_Color(): string | null;
```

## Returns

string \| null

Color

### getstate_endx

# ISCH\_PrimitiveArc.getState\_EndX() method

Get the property state: end point X

## Signature

```typescript
function getState_EndX(): number;
```

## Returns

number

End point X

### getstate_endy

# ISCH\_PrimitiveArc.getState\_EndY() method

Get the property state: end point Y

## Signature

```typescript
function getState_EndY(): number;
```

## Returns

number

End point Y

### getstate_fillcolor

# ISCH\_PrimitiveArc.getState\_FillColor() method

Get the property state: fill color

## Signature

```typescript
function getState_FillColor(): string | null;
```

## Returns

string \| null

Fill color

### getstate_linetype

# ISCH\_PrimitiveArc.getState\_LineType() method

Get the property state: line type

## Signature

```typescript
function getState_LineType(): ESCH_PrimitiveLineType | null;
```

## Returns

[ESCH\_PrimitiveLineType](../enums/ESCH_PrimitiveLineType.md) \| null

Line type

### getstate_linewidth

# ISCH\_PrimitiveArc.getState\_LineWidth() method

Get the property state: Line width

## Signature

```typescript
function getState_LineWidth(): number | null;
```

## Returns

number \| null

Line width

### getstate_primitiveid

# ISCH\_PrimitiveArc.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivetype

# ISCH\_PrimitiveArc.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): ESCH_PrimitiveType;
```

## Returns

[ESCH\_PrimitiveType](../enums/ESCH_PrimitiveType.md)

Primitive type

### getstate_referencex

# ISCH\_PrimitiveArc.getState\_ReferenceX() method

Get the property state: reference point X

## Signature

```typescript
function getState_ReferenceX(): number;
```

## Returns

number

Reference point X

### getstate_referencey

# ISCH\_PrimitiveArc.getState\_ReferenceY() method

Get the property state: reference point Y

## Signature

```typescript
function getState_ReferenceY(): number;
```

## Returns

number

Reference point Y

### getstate_startx

# ISCH\_PrimitiveArc.getState\_StartX() method

Get the property state: start point X

## Signature

```typescript
function getState_StartX(): number;
```

## Returns

number

Start point X

### getstate_starty

# ISCH\_PrimitiveArc.getState\_StartY() method

Get the property state: start point Y

## Signature

```typescript
function getState_StartY(): number;
```

## Returns

number

Start point Y

### isasync

# ISCH\_PrimitiveArc.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# ISCH\_PrimitiveArc.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<ISCH_PrimitiveArc>;
```

## Returns

Promise&lt;[ISCH\_PrimitiveArc](./ISCH_PrimitiveArc.md)<!-- -->&gt;

Arc primitive object

### setstate_color

# ISCH\_PrimitiveArc.setState\_Color() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: color

## Signature

```typescript
function setState_Color(color: string | null): ISCH_PrimitiveArc;
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

color

</td><td>

string \| null

</td><td>

Color

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveArc](./ISCH_PrimitiveArc.md)

Arc primitive object

### setstate_endx

# ISCH\_PrimitiveArc.setState\_EndX() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: end point X

## Signature

```typescript
function setState_EndX(endX: number): ISCH_PrimitiveArc;
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

End point X

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveArc](./ISCH_PrimitiveArc.md)

Arc primitive object

### setstate_endy

# ISCH\_PrimitiveArc.setState\_EndY() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: end point Y

## Signature

```typescript
function setState_EndY(endY: number): ISCH_PrimitiveArc;
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

End point Y

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveArc](./ISCH_PrimitiveArc.md)

Arc primitive object

### setstate_fillcolor

# ISCH\_PrimitiveArc.setState\_FillColor() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: fill color

## Signature

```typescript
function setState_FillColor(fillColor: string | null): ISCH_PrimitiveArc;
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

fillColor

</td><td>

string \| null

</td><td>

Fill color

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveArc](./ISCH_PrimitiveArc.md)

Arc primitive object

### setstate_linetype

# ISCH\_PrimitiveArc.setState\_LineType() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: line type

## Signature

```typescript
function setState_LineType(lineType: ESCH_PrimitiveLineType | null): ISCH_PrimitiveArc;
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

lineType

</td><td>

[ESCH\_PrimitiveLineType](../enums/ESCH_PrimitiveLineType.md) \| null

</td><td>

Line type

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveArc](./ISCH_PrimitiveArc.md)

Arc primitive object

### setstate_linewidth

# ISCH\_PrimitiveArc.setState\_LineWidth() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Line width

## Signature

```typescript
function setState_LineWidth(lineWidth: number | null): ISCH_PrimitiveArc;
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

number \| null

</td><td>

Line width

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveArc](./ISCH_PrimitiveArc.md)

Arc primitive object

### setstate_referencex

# ISCH\_PrimitiveArc.setState\_ReferenceX() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: reference point X

## Signature

```typescript
function setState_ReferenceX(referenceX: number): ISCH_PrimitiveArc;
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

referenceX

</td><td>

number

</td><td>

Reference point X

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveArc](./ISCH_PrimitiveArc.md)

Arc primitive object

### setstate_referencey

# ISCH\_PrimitiveArc.setState\_ReferenceY() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: reference point Y

## Signature

```typescript
function setState_ReferenceY(referenceY: number): ISCH_PrimitiveArc;
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

referenceY

</td><td>

number

</td><td>

Reference point Y

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveArc](./ISCH_PrimitiveArc.md)

Arc primitive object

### setstate_startx

# ISCH\_PrimitiveArc.setState\_StartX() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: start point X

## Signature

```typescript
function setState_StartX(startX: number): ISCH_PrimitiveArc;
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

Start point X

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveArc](./ISCH_PrimitiveArc.md)

Arc primitive object

### setstate_starty

# ISCH\_PrimitiveArc.setState\_StartY() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: start point Y

## Signature

```typescript
function setState_StartY(startY: number): ISCH_PrimitiveArc;
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

Start point Y

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveArc](./ISCH_PrimitiveArc.md)

Arc primitive object

### toasync

# ISCH\_PrimitiveArc.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): ISCH_PrimitiveArc;
```

## Returns

[ISCH\_PrimitiveArc](./ISCH_PrimitiveArc.md)

Arc primitive object

### tosync

# ISCH\_PrimitiveArc.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): ISCH_PrimitiveArc;
```

## Returns

[ISCH\_PrimitiveArc](./ISCH_PrimitiveArc.md)

Arc primitive object

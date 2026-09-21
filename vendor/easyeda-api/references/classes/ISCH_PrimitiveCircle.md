# ISCH\_PrimitiveCircle class

Circle primitive

## Signature

```typescript
class ISCH_PrimitiveCircle implements ISCH_Primitive
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

[done()](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getState\_CenterX()](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

Get the property state: center of the circle X

</td></tr>
<tr><td>

[getState\_CenterY()](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

Get the property state: center of the circle Y

</td></tr>
<tr><td>

[getState\_Color()](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

Get the property state: color

</td></tr>
<tr><td>

[getState\_FillColor()](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

Get the property state: fill color

</td></tr>
<tr><td>

[getState\_FillStyle()](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

Get the property state: fill style

</td></tr>
<tr><td>

[getState\_LineType()](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

Get the property state: line type

</td></tr>
<tr><td>

[getState\_LineWidth()](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

Get the property state: Line width

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[getState\_Radius()](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

Get the property state: radius

</td></tr>
<tr><td>

[isAsync()](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_CenterX(centerX)](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: center of the circle X

</td></tr>
<tr><td>

[setState\_CenterY(centerY)](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: center of the circle Y

</td></tr>
<tr><td>

[setState\_Color(color)](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: color

</td></tr>
<tr><td>

[setState\_FillColor(fillColor)](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: fill color

</td></tr>
<tr><td>

[setState\_FillStyle(fillStyle)](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: fill style

</td></tr>
<tr><td>

[setState\_LineType(lineType)](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: line type

</td></tr>
<tr><td>

[setState\_LineWidth(lineWidth)](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Line width

</td></tr>
<tr><td>

[setState\_Radius(radius)](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: radius

</td></tr>
<tr><td>

[toAsync()](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./ISCH_PrimitiveCircle.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 方法详情

### done

# ISCH\_PrimitiveCircle.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<ISCH_PrimitiveCircle>;
```

## Returns

Promise&lt;[ISCH\_PrimitiveCircle](./ISCH_PrimitiveCircle.md)<!-- -->&gt;

Circle primitive object

### getstate_centerx

# ISCH\_PrimitiveCircle.getState\_CenterX() method

Get the property state: center of the circle X

## Signature

```typescript
function getState_CenterX(): number;
```

## Returns

number

Center of the circle X

### getstate_centery

# ISCH\_PrimitiveCircle.getState\_CenterY() method

Get the property state: center of the circle Y

## Signature

```typescript
function getState_CenterY(): number;
```

## Returns

number

Center of the circle Y

### getstate_color

# ISCH\_PrimitiveCircle.getState\_Color() method

Get the property state: color

## Signature

```typescript
function getState_Color(): string | null;
```

## Returns

string \| null

Color

### getstate_fillcolor

# ISCH\_PrimitiveCircle.getState\_FillColor() method

Get the property state: fill color

## Signature

```typescript
function getState_FillColor(): string | null;
```

## Returns

string \| null

Fill color

### getstate_fillstyle

# ISCH\_PrimitiveCircle.getState\_FillStyle() method

Get the property state: fill style

## Signature

```typescript
function getState_FillStyle(): ESCH_PrimitiveFillStyle | null;
```

## Returns

[ESCH\_PrimitiveFillStyle](../enums/ESCH_PrimitiveFillStyle.md) \| null

Fill style

### getstate_linetype

# ISCH\_PrimitiveCircle.getState\_LineType() method

Get the property state: line type

## Signature

```typescript
function getState_LineType(): ESCH_PrimitiveLineType | null;
```

## Returns

[ESCH\_PrimitiveLineType](../enums/ESCH_PrimitiveLineType.md) \| null

Line type

### getstate_linewidth

# ISCH\_PrimitiveCircle.getState\_LineWidth() method

Get the property state: Line width

## Signature

```typescript
function getState_LineWidth(): number | null;
```

## Returns

number \| null

Line width

### getstate_primitiveid

# ISCH\_PrimitiveCircle.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivetype

# ISCH\_PrimitiveCircle.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): ESCH_PrimitiveType;
```

## Returns

[ESCH\_PrimitiveType](../enums/ESCH_PrimitiveType.md)

Primitive type

### getstate_radius

# ISCH\_PrimitiveCircle.getState\_Radius() method

Get the property state: radius

## Signature

```typescript
function getState_Radius(): number;
```

## Returns

number

Radius

### isasync

# ISCH\_PrimitiveCircle.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# ISCH\_PrimitiveCircle.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<ISCH_PrimitiveCircle>;
```

## Returns

Promise&lt;[ISCH\_PrimitiveCircle](./ISCH_PrimitiveCircle.md)<!-- -->&gt;

Circle primitive object

### setstate_centerx

# ISCH\_PrimitiveCircle.setState\_CenterX() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: center of the circle X

## Signature

```typescript
function setState_CenterX(centerX: number): ISCH_PrimitiveCircle;
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

centerX

</td><td>

number

</td><td>

Center of the circle X

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveCircle](./ISCH_PrimitiveCircle.md)

Circle primitive object

### setstate_centery

# ISCH\_PrimitiveCircle.setState\_CenterY() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: center of the circle Y

## Signature

```typescript
function setState_CenterY(centerY: number): ISCH_PrimitiveCircle;
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

centerY

</td><td>

number

</td><td>

Center of the circle Y

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveCircle](./ISCH_PrimitiveCircle.md)

Circle primitive object

### setstate_color

# ISCH\_PrimitiveCircle.setState\_Color() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: color

## Signature

```typescript
function setState_Color(color: string | null): ISCH_PrimitiveCircle;
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

[ISCH\_PrimitiveCircle](./ISCH_PrimitiveCircle.md)

Circle primitive object

### setstate_fillcolor

# ISCH\_PrimitiveCircle.setState\_FillColor() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: fill color

## Signature

```typescript
function setState_FillColor(fillColor: string | null): ISCH_PrimitiveCircle;
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

[ISCH\_PrimitiveCircle](./ISCH_PrimitiveCircle.md)

Circle primitive object

### setstate_fillstyle

# ISCH\_PrimitiveCircle.setState\_FillStyle() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: fill style

## Signature

```typescript
function setState_FillStyle(fillStyle: ESCH_PrimitiveFillStyle | null): ISCH_PrimitiveCircle;
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

fillStyle

</td><td>

[ESCH\_PrimitiveFillStyle](../enums/ESCH_PrimitiveFillStyle.md) \| null

</td><td>

Fill style

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveCircle](./ISCH_PrimitiveCircle.md)

Circle primitive object

### setstate_linetype

# ISCH\_PrimitiveCircle.setState\_LineType() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: line type

## Signature

```typescript
function setState_LineType(lineType: ESCH_PrimitiveLineType | null): ISCH_PrimitiveCircle;
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

[ISCH\_PrimitiveCircle](./ISCH_PrimitiveCircle.md)

Circle primitive object

### setstate_linewidth

# ISCH\_PrimitiveCircle.setState\_LineWidth() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Line width

## Signature

```typescript
function setState_LineWidth(lineWidth: number | null): ISCH_PrimitiveCircle;
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

[ISCH\_PrimitiveCircle](./ISCH_PrimitiveCircle.md)

Circle primitive object

### setstate_radius

# ISCH\_PrimitiveCircle.setState\_Radius() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: radius

## Signature

```typescript
function setState_Radius(radius: number): ISCH_PrimitiveCircle;
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

radius

</td><td>

number

</td><td>

Radius

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveCircle](./ISCH_PrimitiveCircle.md)

Circle primitive object

### toasync

# ISCH\_PrimitiveCircle.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): ISCH_PrimitiveCircle;
```

## Returns

[ISCH\_PrimitiveCircle](./ISCH_PrimitiveCircle.md)

Circle primitive object

### tosync

# ISCH\_PrimitiveCircle.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): ISCH_PrimitiveCircle;
```

## Returns

[ISCH\_PrimitiveCircle](./ISCH_PrimitiveCircle.md)

Circle primitive object

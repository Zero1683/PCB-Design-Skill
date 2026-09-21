# ISCH\_PrimitiveRectangle class

Rectangle primitive

## Signature

```typescript
class ISCH_PrimitiveRectangle implements ISCH_Primitive
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

[done()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getState\_Color()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Get the property state: border color

</td></tr>
<tr><td>

[getState\_CornerRadius()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Get the property state: corner radius

</td></tr>
<tr><td>

[getState\_FillColor()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Get the property state: fill color

</td></tr>
<tr><td>

[getState\_FillStyle()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Get the property state: fill style

</td></tr>
<tr><td>

[getState\_Height()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Get the property state: height

</td></tr>
<tr><td>

[getState\_LineType()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Get the property state: line type

</td></tr>
<tr><td>

[getState\_LineWidth()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Get the property state: Line width

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[getState\_Rotation()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Get the property state: rotation angle

</td></tr>
<tr><td>

[getState\_TopLeftX()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Get the property state: top-left point X

</td></tr>
<tr><td>

[getState\_TopLeftY()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Get the property state: top-left point Y

</td></tr>
<tr><td>

[getState\_Width()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Get the property state: width

</td></tr>
<tr><td>

[isAsync()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_Color(color)](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: border color

</td></tr>
<tr><td>

[setState\_CornerRadius(cornerRadius)](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: corner radius

</td></tr>
<tr><td>

[setState\_FillColor(fillColor)](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: fill color

</td></tr>
<tr><td>

[setState\_FillStyle(fillStyle)](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: fill style

</td></tr>
<tr><td>

[setState\_Height(height)](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: height

</td></tr>
<tr><td>

[setState\_LineType(lineType)](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: line type

</td></tr>
<tr><td>

[setState\_LineWidth(lineWidth)](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Line width

</td></tr>
<tr><td>

[setState\_Rotation(rotation)](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: rotation angle

</td></tr>
<tr><td>

[setState\_TopLeftX(topLeftX)](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: top-left point X

</td></tr>
<tr><td>

[setState\_TopLeftY(topLeftY)](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: top-left point Y

</td></tr>
<tr><td>

[setState\_Width(width)](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: width

</td></tr>
<tr><td>

[toAsync()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./ISCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 方法详情

### done

# ISCH\_PrimitiveRectangle.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<ISCH_PrimitiveRectangle>;
```

## Returns

Promise&lt;[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)<!-- -->&gt;

Rectangle primitive object

### getstate_color

# ISCH\_PrimitiveRectangle.getState\_Color() method

Get the property state: border color

## Signature

```typescript
function getState_Color(): string | null;
```

## Returns

string \| null

Border color

### getstate_cornerradius

# ISCH\_PrimitiveRectangle.getState\_CornerRadius() method

Get the property state: corner radius

## Signature

```typescript
function getState_CornerRadius(): number;
```

## Returns

number

Corner radius

### getstate_fillcolor

# ISCH\_PrimitiveRectangle.getState\_FillColor() method

Get the property state: fill color

## Signature

```typescript
function getState_FillColor(): string | null;
```

## Returns

string \| null

Fill color

### getstate_fillstyle

# ISCH\_PrimitiveRectangle.getState\_FillStyle() method

Get the property state: fill style

## Signature

```typescript
function getState_FillStyle(): ESCH_PrimitiveFillStyle | null;
```

## Returns

[ESCH\_PrimitiveFillStyle](../enums/ESCH_PrimitiveFillStyle.md) \| null

Fill style

### getstate_height

# ISCH\_PrimitiveRectangle.getState\_Height() method

Get the property state: height

## Signature

```typescript
function getState_Height(): number;
```

## Returns

number

Height

### getstate_linetype

# ISCH\_PrimitiveRectangle.getState\_LineType() method

Get the property state: line type

## Signature

```typescript
function getState_LineType(): ESCH_PrimitiveLineType | null;
```

## Returns

[ESCH\_PrimitiveLineType](../enums/ESCH_PrimitiveLineType.md) \| null

Line type

### getstate_linewidth

# ISCH\_PrimitiveRectangle.getState\_LineWidth() method

Get the property state: Line width

## Signature

```typescript
function getState_LineWidth(): number | null;
```

## Returns

number \| null

Line width

### getstate_primitiveid

# ISCH\_PrimitiveRectangle.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivetype

# ISCH\_PrimitiveRectangle.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): ESCH_PrimitiveType;
```

## Returns

[ESCH\_PrimitiveType](../enums/ESCH_PrimitiveType.md)

Primitive type

### getstate_rotation

# ISCH\_PrimitiveRectangle.getState\_Rotation() method

Get the property state: rotation angle

## Signature

```typescript
function getState_Rotation(): number;
```

## Returns

number

Rotation angle

### getstate_topleftx

# ISCH\_PrimitiveRectangle.getState\_TopLeftX() method

Get the property state: top-left point X

## Signature

```typescript
function getState_TopLeftX(): number;
```

## Returns

number

Top-left point X

### getstate_toplefty

# ISCH\_PrimitiveRectangle.getState\_TopLeftY() method

Get the property state: top-left point Y

## Signature

```typescript
function getState_TopLeftY(): number;
```

## Returns

number

Top-left point Y

### getstate_width

# ISCH\_PrimitiveRectangle.getState\_Width() method

Get the property state: width

## Signature

```typescript
function getState_Width(): number;
```

## Returns

number

Width

### isasync

# ISCH\_PrimitiveRectangle.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# ISCH\_PrimitiveRectangle.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<ISCH_PrimitiveRectangle>;
```

## Returns

Promise&lt;[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)<!-- -->&gt;

Rectangle primitive object

### setstate_color

# ISCH\_PrimitiveRectangle.setState\_Color() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: border color

## Signature

```typescript
function setState_Color(color: string | null): ISCH_PrimitiveRectangle;
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

Border color

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)

Rectangle primitive object

### setstate_cornerradius

# ISCH\_PrimitiveRectangle.setState\_CornerRadius() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: corner radius

## Signature

```typescript
function setState_CornerRadius(cornerRadius: number): ISCH_PrimitiveRectangle;
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

cornerRadius

</td><td>

number

</td><td>

Corner radius

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)

Rectangle primitive object

### setstate_fillcolor

# ISCH\_PrimitiveRectangle.setState\_FillColor() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: fill color

## Signature

```typescript
function setState_FillColor(fillColor: string | null): ISCH_PrimitiveRectangle;
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

[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)

Rectangle primitive object

### setstate_fillstyle

# ISCH\_PrimitiveRectangle.setState\_FillStyle() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: fill style

## Signature

```typescript
function setState_FillStyle(fillStyle: ESCH_PrimitiveFillStyle | null): ISCH_PrimitiveRectangle;
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

[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)

Rectangle primitive object

### setstate_height

# ISCH\_PrimitiveRectangle.setState\_Height() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: height

## Signature

```typescript
function setState_Height(height: number): ISCH_PrimitiveRectangle;
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

height

</td><td>

number

</td><td>

Height

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)

Rectangle primitive object

### setstate_linetype

# ISCH\_PrimitiveRectangle.setState\_LineType() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: line type

## Signature

```typescript
function setState_LineType(lineType: ESCH_PrimitiveLineType | null): ISCH_PrimitiveRectangle;
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

[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)

Rectangle primitive object

### setstate_linewidth

# ISCH\_PrimitiveRectangle.setState\_LineWidth() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Line width

## Signature

```typescript
function setState_LineWidth(lineWidth: number | null): ISCH_PrimitiveRectangle;
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

[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)

Rectangle primitive object

### setstate_rotation

# ISCH\_PrimitiveRectangle.setState\_Rotation() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: rotation angle

## Signature

```typescript
function setState_Rotation(rotation: number): ISCH_PrimitiveRectangle;
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

rotation

</td><td>

number

</td><td>

Rotation angle

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)

Rectangle primitive object

### setstate_topleftx

# ISCH\_PrimitiveRectangle.setState\_TopLeftX() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: top-left point X

## Signature

```typescript
function setState_TopLeftX(topLeftX: number): ISCH_PrimitiveRectangle;
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

topLeftX

</td><td>

number

</td><td>

Top-left point X

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)

Rectangle primitive object

### setstate_toplefty

# ISCH\_PrimitiveRectangle.setState\_TopLeftY() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: top-left point Y

## Signature

```typescript
function setState_TopLeftY(topLeftY: number): ISCH_PrimitiveRectangle;
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

topLeftY

</td><td>

number

</td><td>

Top-left point Y

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)

Rectangle primitive object

### setstate_width

# ISCH\_PrimitiveRectangle.setState\_Width() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: width

## Signature

```typescript
function setState_Width(width: number): ISCH_PrimitiveRectangle;
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

width

</td><td>

number

</td><td>

Width

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)

Rectangle primitive object

### toasync

# ISCH\_PrimitiveRectangle.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): ISCH_PrimitiveRectangle;
```

## Returns

[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)

Rectangle primitive object

### tosync

# ISCH\_PrimitiveRectangle.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): ISCH_PrimitiveRectangle;
```

## Returns

[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)

Rectangle primitive object

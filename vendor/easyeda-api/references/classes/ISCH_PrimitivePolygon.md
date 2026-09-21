# ISCH\_PrimitivePolygon class

Polygon (polyline) primitive

## Signature

```typescript
class ISCH_PrimitivePolygon implements ISCH_Primitive
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

[done()](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getState\_Color()](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

Get the property state: color

</td></tr>
<tr><td>

[getState\_FillColor()](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

Get the property state: fill color

</td></tr>
<tr><td>

[getState\_Line()](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

Get the property state: coordinate group

</td></tr>
<tr><td>

[getState\_LineType()](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

Get the property state: line type

</td></tr>
<tr><td>

[getState\_LineWidth()](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

Get the property state: Line width

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[isAsync()](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_Color(color)](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: color

</td></tr>
<tr><td>

[setState\_FillColor(fillColor)](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: fill color

</td></tr>
<tr><td>

[setState\_Line(line)](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: coordinate group

</td></tr>
<tr><td>

[setState\_LineType(lineType)](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: line type

</td></tr>
<tr><td>

[setState\_LineWidth(lineWidth)](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Line width

</td></tr>
<tr><td>

[toAsync()](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./ISCH_PrimitivePolygon.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 方法详情

### done

# ISCH\_PrimitivePolygon.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<ISCH_PrimitivePolygon>;
```

## Returns

Promise&lt;[ISCH\_PrimitivePolygon](./ISCH_PrimitivePolygon.md)<!-- -->&gt;

Polygon primitive object

### getstate_color

# ISCH\_PrimitivePolygon.getState\_Color() method

Get the property state: color

## Signature

```typescript
function getState_Color(): string | null;
```

## Returns

string \| null

Color

### getstate_fillcolor

# ISCH\_PrimitivePolygon.getState\_FillColor() method

Get the property state: fill color

## Signature

```typescript
function getState_FillColor(): string | null;
```

## Returns

string \| null

Fill color

### getstate_line

# ISCH\_PrimitivePolygon.getState\_Line() method

Get the property state: coordinate group

## Signature

```typescript
function getState_Line(): Array<number>;
```

## Returns

Array&lt;number&gt;

Coordinate group

### getstate_linetype

# ISCH\_PrimitivePolygon.getState\_LineType() method

Get the property state: line type

## Signature

```typescript
function getState_LineType(): ESCH_PrimitiveLineType | null;
```

## Returns

[ESCH\_PrimitiveLineType](../enums/ESCH_PrimitiveLineType.md) \| null

Line type

### getstate_linewidth

# ISCH\_PrimitivePolygon.getState\_LineWidth() method

Get the property state: Line width

## Signature

```typescript
function getState_LineWidth(): number | null;
```

## Returns

number \| null

Line width

### getstate_primitiveid

# ISCH\_PrimitivePolygon.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivetype

# ISCH\_PrimitivePolygon.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): ESCH_PrimitiveType;
```

## Returns

[ESCH\_PrimitiveType](../enums/ESCH_PrimitiveType.md)

Primitive type

### isasync

# ISCH\_PrimitivePolygon.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# ISCH\_PrimitivePolygon.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<ISCH_PrimitivePolygon>;
```

## Returns

Promise&lt;[ISCH\_PrimitivePolygon](./ISCH_PrimitivePolygon.md)<!-- -->&gt;

Polygon primitive object

### setstate_color

# ISCH\_PrimitivePolygon.setState\_Color() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: color

## Signature

```typescript
function setState_Color(color: string | null): ISCH_PrimitivePolygon;
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

[ISCH\_PrimitivePolygon](./ISCH_PrimitivePolygon.md)

Polygon primitive object

### setstate_fillcolor

# ISCH\_PrimitivePolygon.setState\_FillColor() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: fill color

## Signature

```typescript
function setState_FillColor(fillColor: string | null): ISCH_PrimitivePolygon;
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

[ISCH\_PrimitivePolygon](./ISCH_PrimitivePolygon.md)

Polygon primitive object

### setstate_line

# ISCH\_PrimitivePolygon.setState\_Line() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: coordinate group

## Signature

```typescript
function setState_Line(line: Array<number>): ISCH_PrimitivePolygon;
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

line

</td><td>

Array&lt;number&gt;

</td><td>

Coordinate group

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitivePolygon](./ISCH_PrimitivePolygon.md)

Polygon primitive object

### setstate_linetype

# ISCH\_PrimitivePolygon.setState\_LineType() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: line type

## Signature

```typescript
function setState_LineType(lineType: ESCH_PrimitiveLineType | null): ISCH_PrimitivePolygon;
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

[ISCH\_PrimitivePolygon](./ISCH_PrimitivePolygon.md)

Polygon primitive object

### setstate_linewidth

# ISCH\_PrimitivePolygon.setState\_LineWidth() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Line width

## Signature

```typescript
function setState_LineWidth(lineWidth: number | null): ISCH_PrimitivePolygon;
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

[ISCH\_PrimitivePolygon](./ISCH_PrimitivePolygon.md)

Polygon primitive object

### toasync

# ISCH\_PrimitivePolygon.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): ISCH_PrimitivePolygon;
```

## Returns

[ISCH\_PrimitivePolygon](./ISCH_PrimitivePolygon.md)

Polygon primitive object

### tosync

# ISCH\_PrimitivePolygon.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): ISCH_PrimitivePolygon;
```

## Returns

[ISCH\_PrimitivePolygon](./ISCH_PrimitivePolygon.md)

Polygon primitive object

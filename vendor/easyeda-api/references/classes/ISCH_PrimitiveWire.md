# ISCH\_PrimitiveWire class

Wire primitive

## Signature

```typescript
class ISCH_PrimitiveWire implements ISCH_Primitive
```
**Implements:** [ISCH\_Primitive](../interfaces/ISCH_Primitive.md)

## Remarks

Unresolved issues:

The `ISCH_PrimitiveWire.net` global net name property involves multi-sheet refresh, so the currently obtained value may be \*\*incorrect\*\*. When you try to set multiple names for a wire or bus (by placing multiple net labels), the obtained `net` property may not be the latest. You need to wait for the canvas event to asynchronously refresh the global nets before reading it again.

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[done()](./ISCH_PrimitiveWire.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getState\_Color()](./ISCH_PrimitiveWire.md)

</td><td>

</td><td>

Get the property state: bus color

</td></tr>
<tr><td>

[getState\_Line()](./ISCH_PrimitiveWire.md)

</td><td>

</td><td>

Get the property state: polyline coordinate group

</td></tr>
<tr><td>

[getState\_LineType()](./ISCH_PrimitiveWire.md)

</td><td>

</td><td>

Get the property state: line type

</td></tr>
<tr><td>

[getState\_LineWidth()](./ISCH_PrimitiveWire.md)

</td><td>

</td><td>

Get the property state: Line width

</td></tr>
<tr><td>

[getState\_Net()](./ISCH_PrimitiveWire.md)

</td><td>

</td><td>

Get the property state: net name

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./ISCH_PrimitiveWire.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./ISCH_PrimitiveWire.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[isAsync()](./ISCH_PrimitiveWire.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[setState\_Color(color)](./ISCH_PrimitiveWire.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: wire color

</td></tr>
<tr><td>

[setState\_Line(line)](./ISCH_PrimitiveWire.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: polyline coordinate group

</td></tr>
<tr><td>

[setState\_LineType(lineType)](./ISCH_PrimitiveWire.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: line type

</td></tr>
<tr><td>

[setState\_LineWidth(lineWidth)](./ISCH_PrimitiveWire.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Line width

</td></tr>
<tr><td>

[setState\_Net(net)](./ISCH_PrimitiveWire.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: net name

</td></tr>
<tr><td>

[toAsync()](./ISCH_PrimitiveWire.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./ISCH_PrimitiveWire.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 方法详情

### done

# ISCH\_PrimitiveWire.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<ISCH_PrimitiveWire>;
```

## Returns

Promise&lt;[ISCH\_PrimitiveWire](./ISCH_PrimitiveWire.md)<!-- -->&gt;

Wire primitive object

### getstate_color

# ISCH\_PrimitiveWire.getState\_Color() method

Get the property state: bus color

## Signature

```typescript
function getState_Color(): string | null;
```

## Returns

string \| null

Bus color

### getstate_line

# ISCH\_PrimitiveWire.getState\_Line() method

Get the property state: polyline coordinate group

## Signature

```typescript
function getState_Line(): Array<number> | Array<Array<number>>;
```

## Returns

Array&lt;number&gt; \| Array&lt;Array&lt;number&gt;&gt;

Polyline coordinate group

### getstate_linetype

# ISCH\_PrimitiveWire.getState\_LineType() method

Get the property state: line type

## Signature

```typescript
function getState_LineType(): ESCH_PrimitiveLineType | null;
```

## Returns

[ESCH\_PrimitiveLineType](../enums/ESCH_PrimitiveLineType.md) \| null

Line type

### getstate_linewidth

# ISCH\_PrimitiveWire.getState\_LineWidth() method

Get the property state: Line width

## Signature

```typescript
function getState_LineWidth(): number | null;
```

## Returns

number \| null

Line width

### getstate_net

# ISCH\_PrimitiveWire.getState\_Net() method

Get the property state: net name

## Signature

```typescript
function getState_Net(): string;
```

## Returns

string

Net name

### getstate_primitiveid

# ISCH\_PrimitiveWire.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivetype

# ISCH\_PrimitiveWire.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): ESCH_PrimitiveType;
```

## Returns

[ESCH\_PrimitiveType](../enums/ESCH_PrimitiveType.md)

Primitive type

### isasync

# ISCH\_PrimitiveWire.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### setstate_color

# ISCH\_PrimitiveWire.setState\_Color() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: wire color

## Signature

```typescript
function setState_Color(color: string | null): ISCH_PrimitiveWire;
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

Wire color

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveWire](./ISCH_PrimitiveWire.md)

Wire primitive object

### setstate_line

# ISCH\_PrimitiveWire.setState\_Line() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: polyline coordinate group

## Signature

```typescript
function setState_Line(line: Array<number> | Array<Array<number>>): ISCH_PrimitiveWire;
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

Array&lt;number&gt; \| Array&lt;Array&lt;number&gt;&gt;

</td><td>

Polyline coordinate group

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveWire](./ISCH_PrimitiveWire.md)

Wire primitive object

### setstate_linetype

# ISCH\_PrimitiveWire.setState\_LineType() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: line type

## Signature

```typescript
function setState_LineType(lineType: ESCH_PrimitiveLineType | null): ISCH_PrimitiveWire;
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

[ISCH\_PrimitiveWire](./ISCH_PrimitiveWire.md)

Wire primitive object

### setstate_linewidth

# ISCH\_PrimitiveWire.setState\_LineWidth() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Line width

## Signature

```typescript
function setState_LineWidth(lineWidth: number | null): ISCH_PrimitiveWire;
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

[ISCH\_PrimitiveWire](./ISCH_PrimitiveWire.md)

Wire primitive object

### setstate_net

# ISCH\_PrimitiveWire.setState\_Net() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: net name

## Signature

```typescript
function setState_Net(net: string): ISCH_PrimitiveWire;
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

[ISCH\_PrimitiveWire](./ISCH_PrimitiveWire.md)

Wire primitive object

### toasync

# ISCH\_PrimitiveWire.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): ISCH_PrimitiveWire;
```

## Returns

[ISCH\_PrimitiveWire](./ISCH_PrimitiveWire.md)

Wire primitive object

### tosync

# ISCH\_PrimitiveWire.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): ISCH_PrimitiveWire;
```

## Returns

[ISCH\_PrimitiveWire](./ISCH_PrimitiveWire.md)

Wire primitive object

# IPCB\_PrimitiveString class

Text primitive

## Signature

```typescript
class IPCB_PrimitiveString implements IPCB_Primitive
```
**Implements:** [IPCB\_Primitive](../interfaces/IPCB_Primitive.md)

## Constructors

<table><thead><tr><th>

Constructor

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[(constructor)(layer, x, y, text, fontFamily, fontSize, lineWidth, alignMode, rotation, reverse, expansion, mirror, primitiveLock, primitiveId)](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Constructs a new instance of the `IPCB_PrimitiveString` class

</td></tr>
</tbody></table>

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[done()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getState\_AlignMode()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Get the property state: alignment mode

</td></tr>
<tr><td>

[getState\_Expansion()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Get the property state: inverted expansion

</td></tr>
<tr><td>

[getState\_FontFamily()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Get the property state: font

</td></tr>
<tr><td>

[getState\_FontSize()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Get the property state: font size

</td></tr>
<tr><td>

[getState\_Layer()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Get the property state: Layer

</td></tr>
<tr><td>

[getState\_LineWidth()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Get the property state: Line width

</td></tr>
<tr><td>

[getState\_Mirror()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Get the property state: whether it is mirrored

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveLock()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Get the property state: whether it is locked

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[getState\_Reverse()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Get the property state: whether it is inverted

</td></tr>
<tr><td>

[getState\_Rotation()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Get the property state: rotation angle

</td></tr>
<tr><td>

[getState\_Text()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Get the property state: text content

</td></tr>
<tr><td>

[getState\_X()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Get the property state: X coordinate

</td></tr>
<tr><td>

[getState\_Y()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Get the property state: Y coordinate

</td></tr>
<tr><td>

[isAsync()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_AlignMode(alignMode)](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: alignment mode

</td></tr>
<tr><td>

[setState\_Expansion(expansion)](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: inverted expansion

</td></tr>
<tr><td>

[setState\_FontFamily(fontFamily)](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: font

</td></tr>
<tr><td>

[setState\_FontSize(fontSize)](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: font size

</td></tr>
<tr><td>

[setState\_Layer(layer)](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Layer

</td></tr>
<tr><td>

[setState\_LineWidth(lineWidth)](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Line width

</td></tr>
<tr><td>

[setState\_Mirror(mirror)](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is mirrored

</td></tr>
<tr><td>

[setState\_PrimitiveLock(primitiveLock)](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is locked

</td></tr>
<tr><td>

[setState\_Reverse(reverse)](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is inverted

</td></tr>
<tr><td>

[setState\_Rotation(rotation)](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: rotation angle

</td></tr>
<tr><td>

[setState\_Text(text)](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: text content

</td></tr>
<tr><td>

[setState\_X(x)](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: X coordinate

</td></tr>
<tr><td>

[setState\_Y(y)](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Y coordinate

</td></tr>
<tr><td>

[toAsync()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./IPCB_PrimitiveString.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 构造函数详情

### _constructor_

# IPCB\_PrimitiveString.(constructor)

Constructs a new instance of the `IPCB_PrimitiveString` class

## Signature

```typescript
function constructor(
	layer: TPCB_LayersOfImage,
	x: number,
	y: number,
	text: string,
	fontFamily?: string,
	fontSize?: number,
	lineWidth?: number,
	alignMode?: EPCB_PrimitiveStringAlignMode,
	rotation?: number,
	reverse?: boolean,
	expansion?: number,
	mirror?: boolean,
	primitiveLock?: boolean,
	primitiveId?: string,
);
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

[TPCB\_LayersOfImage](../types/TPCB_LayersOfImage.md)

</td><td>

</td></tr>
<tr><td>

x

</td><td>

number

</td><td>

</td></tr>
<tr><td>

y

</td><td>

number

</td><td>

</td></tr>
<tr><td>

text

</td><td>

string

</td><td>

</td></tr>
<tr><td>

fontFamily

</td><td>

string

</td><td>

_(Optional)_

</td></tr>
<tr><td>

fontSize

</td><td>

number

</td><td>

_(Optional)_

</td></tr>
<tr><td>

lineWidth

</td><td>

number

</td><td>

_(Optional)_

</td></tr>
<tr><td>

alignMode

</td><td>

[EPCB\_PrimitiveStringAlignMode](../enums/EPCB_PrimitiveStringAlignMode.md)

</td><td>

_(Optional)_

</td></tr>
<tr><td>

rotation

</td><td>

number

</td><td>

_(Optional)_

</td></tr>
<tr><td>

reverse

</td><td>

boolean

</td><td>

_(Optional)_

</td></tr>
<tr><td>

expansion

</td><td>

number

</td><td>

_(Optional)_

</td></tr>
<tr><td>

mirror

</td><td>

boolean

</td><td>

_(Optional)_

</td></tr>
<tr><td>

primitiveLock

</td><td>

boolean

</td><td>

_(Optional)_

</td></tr>
<tr><td>

primitiveId

</td><td>

string

</td><td>

_(Optional)_

</td></tr>
</tbody></table>


---

## 方法详情

### done

# IPCB\_PrimitiveString.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<IPCB_PrimitiveString>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)<!-- -->&gt;

Text primitive object

### getstate_alignmode

# IPCB\_PrimitiveString.getState\_AlignMode() method

Get the property state: alignment mode

## Signature

```typescript
function getState_AlignMode(): EPCB_PrimitiveStringAlignMode;
```

## Returns

[EPCB\_PrimitiveStringAlignMode](../enums/EPCB_PrimitiveStringAlignMode.md)

Alignment mode

### getstate_expansion

# IPCB\_PrimitiveString.getState\_Expansion() method

Get the property state: inverted expansion

## Signature

```typescript
function getState_Expansion(): number;
```

## Returns

number

Inverted expansion

### getstate_fontfamily

# IPCB\_PrimitiveString.getState\_FontFamily() method

Get the property state: font

## Signature

```typescript
function getState_FontFamily(): string;
```

## Returns

string

Font

### getstate_fontsize

# IPCB\_PrimitiveString.getState\_FontSize() method

Get the property state: font size

## Signature

```typescript
function getState_FontSize(): number;
```

## Returns

number

Font size

### getstate_layer

# IPCB\_PrimitiveString.getState\_Layer() method

Get the property state: Layer

## Signature

```typescript
function getState_Layer(): TPCB_LayersOfImage;
```

## Returns

[TPCB\_LayersOfImage](../types/TPCB_LayersOfImage.md)

Layer

### getstate_linewidth

# IPCB\_PrimitiveString.getState\_LineWidth() method

Get the property state: Line width

## Signature

```typescript
function getState_LineWidth(): number;
```

## Returns

number

Line width

### getstate_mirror

# IPCB\_PrimitiveString.getState\_Mirror() method

Get the property state: whether it is mirrored

## Signature

```typescript
function getState_Mirror(): boolean;
```

## Returns

boolean

Whether it is mirrored

### getstate_primitiveid

# IPCB\_PrimitiveString.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivelock

# IPCB\_PrimitiveString.getState\_PrimitiveLock() method

Get the property state: whether it is locked

## Signature

```typescript
function getState_PrimitiveLock(): boolean;
```

## Returns

boolean

Whether it is locked

### getstate_primitivetype

# IPCB\_PrimitiveString.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): EPCB_PrimitiveType;
```

## Returns

[EPCB\_PrimitiveType](../enums/EPCB_PrimitiveType.md)

Primitive type

### getstate_reverse

# IPCB\_PrimitiveString.getState\_Reverse() method

Get the property state: whether it is inverted

## Signature

```typescript
function getState_Reverse(): boolean;
```

## Returns

boolean

Whether it is inverted

### getstate_rotation

# IPCB\_PrimitiveString.getState\_Rotation() method

Get the property state: rotation angle

## Signature

```typescript
function getState_Rotation(): number;
```

## Returns

number

Rotation angle

### getstate_text

# IPCB\_PrimitiveString.getState\_Text() method

Get the property state: text content

## Signature

```typescript
function getState_Text(): string;
```

## Returns

string

Text content

### getstate_x

# IPCB\_PrimitiveString.getState\_X() method

Get the property state: X coordinate

## Signature

```typescript
function getState_X(): number;
```

## Returns

number

X coordinate

### getstate_y

# IPCB\_PrimitiveString.getState\_Y() method

Get the property state: Y coordinate

## Signature

```typescript
function getState_Y(): number;
```

## Returns

number

Y coordinate

### isasync

# IPCB\_PrimitiveString.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# IPCB\_PrimitiveString.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<IPCB_PrimitiveString>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)<!-- -->&gt;

This primitive object

### setstate_alignmode

# IPCB\_PrimitiveString.setState\_AlignMode() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: alignment mode

## Signature

```typescript
function setState_AlignMode(alignMode: EPCB_PrimitiveStringAlignMode): IPCB_PrimitiveString;
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

alignMode

</td><td>

[EPCB\_PrimitiveStringAlignMode](../enums/EPCB_PrimitiveStringAlignMode.md)

</td><td>

Alignment mode

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)

Text primitive object

### setstate_expansion

# IPCB\_PrimitiveString.setState\_Expansion() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: inverted expansion

## Signature

```typescript
function setState_Expansion(expansion: number): IPCB_PrimitiveString;
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

expansion

</td><td>

number

</td><td>

Inverted expansion

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)

Text primitive object

### setstate_fontfamily

# IPCB\_PrimitiveString.setState\_FontFamily() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: font

## Signature

```typescript
function setState_FontFamily(fontFamily: string): IPCB_PrimitiveString;
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

fontFamily

</td><td>

string

</td><td>

Font

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)

Text primitive object

### setstate_fontsize

# IPCB\_PrimitiveString.setState\_FontSize() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: font size

## Signature

```typescript
function setState_FontSize(fontSize: number): IPCB_PrimitiveString;
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

fontSize

</td><td>

number

</td><td>

Font size

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)

Text primitive object

### setstate_layer

# IPCB\_PrimitiveString.setState\_Layer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Layer

## Signature

```typescript
function setState_Layer(layer: TPCB_LayersOfImage): IPCB_PrimitiveString;
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

[TPCB\_LayersOfImage](../types/TPCB_LayersOfImage.md)

</td><td>

Layer

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)

Text primitive object

### setstate_linewidth

# IPCB\_PrimitiveString.setState\_LineWidth() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Line width

## Signature

```typescript
function setState_LineWidth(lineWidth: number): IPCB_PrimitiveString;
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

[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)

Text primitive object

### setstate_mirror

# IPCB\_PrimitiveString.setState\_Mirror() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is mirrored

## Signature

```typescript
function setState_Mirror(mirror: boolean): IPCB_PrimitiveString;
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

mirror

</td><td>

boolean

</td><td>

Whether it is mirrored

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)

Text primitive object

### setstate_primitivelock

# IPCB\_PrimitiveString.setState\_PrimitiveLock() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is locked

## Signature

```typescript
function setState_PrimitiveLock(primitiveLock: boolean): IPCB_PrimitiveString;
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

[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)

Text primitive object

### setstate_reverse

# IPCB\_PrimitiveString.setState\_Reverse() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is inverted

## Signature

```typescript
function setState_Reverse(reverse: boolean): IPCB_PrimitiveString;
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

reverse

</td><td>

boolean

</td><td>

Whether it is inverted

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)

Text primitive object

## Remarks

The default font does not support inversion

### setstate_rotation

# IPCB\_PrimitiveString.setState\_Rotation() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: rotation angle

## Signature

```typescript
function setState_Rotation(rotation: number): IPCB_PrimitiveString;
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

[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)

Text primitive object

### setstate_text

# IPCB\_PrimitiveString.setState\_Text() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: text content

## Signature

```typescript
function setState_Text(text: string): IPCB_PrimitiveString;
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

text

</td><td>

string

</td><td>

Text content

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)

Text primitive object

### setstate_x

# IPCB\_PrimitiveString.setState\_X() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: X coordinate

## Signature

```typescript
function setState_X(x: number): IPCB_PrimitiveString;
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

x

</td><td>

number

</td><td>

X coordinate

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)

Text primitive object

### setstate_y

# IPCB\_PrimitiveString.setState\_Y() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Y coordinate

## Signature

```typescript
function setState_Y(y: number): IPCB_PrimitiveString;
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

y

</td><td>

number

</td><td>

Y coordinate

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)

Text primitive object

### toasync

# IPCB\_PrimitiveString.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): IPCB_PrimitiveString;
```

## Returns

[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)

Text primitive object

### tosync

# IPCB\_PrimitiveString.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): IPCB_PrimitiveString;
```

## Returns

[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)

Text primitive object

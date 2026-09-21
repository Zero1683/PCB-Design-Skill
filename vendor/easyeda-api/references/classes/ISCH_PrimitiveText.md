# ISCH\_PrimitiveText class

Text primitive

## Signature

```typescript
class ISCH_PrimitiveText implements ISCH_Primitive
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

[done()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getState\_AlignMode()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

Get the property state: alignment mode

</td></tr>
<tr><td>

[getState\_Bold()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

Get the property state: whether it is bold

</td></tr>
<tr><td>

[getState\_Content()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

Get the property state: text content

</td></tr>
<tr><td>

[getState\_FontName()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

Get the property state: font name

</td></tr>
<tr><td>

[getState\_FontSize()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

Get the property state: font size

</td></tr>
<tr><td>

[getState\_Italic()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

Get the property state: whether it is italic

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[getState\_Rotation()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

Get the property state: rotation angle

</td></tr>
<tr><td>

[getState\_TextColor()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

Get the property state: text color

</td></tr>
<tr><td>

[getState\_UnderLine()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

Get the property state: whether it is underlined

</td></tr>
<tr><td>

[getState\_X()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

Get the property state: X coordinate

</td></tr>
<tr><td>

[getState\_Y()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

Get the property state: Y coordinate

</td></tr>
<tr><td>

[isAsync()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_AlignMode(alignMode)](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: alignment mode

</td></tr>
<tr><td>

[setState\_Bold(bold)](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is bold

</td></tr>
<tr><td>

[setState\_Content(content)](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: text content

</td></tr>
<tr><td>

[setState\_FontName(fontName)](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: font name

</td></tr>
<tr><td>

[setState\_FontSize(fontSize)](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: font size

</td></tr>
<tr><td>

[setState\_Italic(italic)](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is italic

</td></tr>
<tr><td>

[setState\_Rotation(rotation)](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: rotation angle

</td></tr>
<tr><td>

[setState\_TextColor(textColor)](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: text color

</td></tr>
<tr><td>

[setState\_UnderLine(underLine)](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is underlined

</td></tr>
<tr><td>

[setState\_X(x)](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: X coordinate

</td></tr>
<tr><td>

[setState\_Y(y)](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Y coordinate

</td></tr>
<tr><td>

[toAsync()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./ISCH_PrimitiveText.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 方法详情

### done

# ISCH\_PrimitiveText.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<ISCH_PrimitiveText>;
```

## Returns

Promise&lt;[ISCH\_PrimitiveText](./ISCH_PrimitiveText.md)<!-- -->&gt;

Text primitive object

### getstate_alignmode

# ISCH\_PrimitiveText.getState\_AlignMode() method

Get the property state: alignment mode

## Signature

```typescript
function getState_AlignMode(): ESCH_PrimitiveTextAlignMode;
```

## Returns

[ESCH\_PrimitiveTextAlignMode](../enums/ESCH_PrimitiveTextAlignMode.md)

Alignment mode

### getstate_bold

# ISCH\_PrimitiveText.getState\_Bold() method

Get the property state: whether it is bold

## Signature

```typescript
function getState_Bold(): boolean;
```

## Returns

boolean

Whether it is bold

### getstate_content

# ISCH\_PrimitiveText.getState\_Content() method

Get the property state: text content

## Signature

```typescript
function getState_Content(): string;
```

## Returns

string

Text content

### getstate_fontname

# ISCH\_PrimitiveText.getState\_FontName() method

Get the property state: font name

## Signature

```typescript
function getState_FontName(): string | null;
```

## Returns

string \| null

Font name

### getstate_fontsize

# ISCH\_PrimitiveText.getState\_FontSize() method

Get the property state: font size

## Signature

```typescript
function getState_FontSize(): number | null;
```

## Returns

number \| null

Font size

### getstate_italic

# ISCH\_PrimitiveText.getState\_Italic() method

Get the property state: whether it is italic

## Signature

```typescript
function getState_Italic(): boolean;
```

## Returns

boolean

Whether it is italic

### getstate_primitiveid

# ISCH\_PrimitiveText.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivetype

# ISCH\_PrimitiveText.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): ESCH_PrimitiveType;
```

## Returns

[ESCH\_PrimitiveType](../enums/ESCH_PrimitiveType.md)

Primitive type

### getstate_rotation

# ISCH\_PrimitiveText.getState\_Rotation() method

Get the property state: rotation angle

## Signature

```typescript
function getState_Rotation(): number;
```

## Returns

number

Rotation angle

### getstate_textcolor

# ISCH\_PrimitiveText.getState\_TextColor() method

Get the property state: text color

## Signature

```typescript
function getState_TextColor(): string | null;
```

## Returns

string \| null

Text color

### getstate_underline

# ISCH\_PrimitiveText.getState\_UnderLine() method

Get the property state: whether it is underlined

## Signature

```typescript
function getState_UnderLine(): boolean;
```

## Returns

boolean

Whether it is underlined

### getstate_x

# ISCH\_PrimitiveText.getState\_X() method

Get the property state: X coordinate

## Signature

```typescript
function getState_X(): number;
```

## Returns

number

X coordinate

### getstate_y

# ISCH\_PrimitiveText.getState\_Y() method

Get the property state: Y coordinate

## Signature

```typescript
function getState_Y(): number;
```

## Returns

number

Y coordinate

### isasync

# ISCH\_PrimitiveText.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# ISCH\_PrimitiveText.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<ISCH_PrimitiveText>;
```

## Returns

Promise&lt;[ISCH\_PrimitiveText](./ISCH_PrimitiveText.md)<!-- -->&gt;

Text primitive object

### setstate_alignmode

# ISCH\_PrimitiveText.setState\_AlignMode() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: alignment mode

## Signature

```typescript
function setState_AlignMode(alignMode: ESCH_PrimitiveTextAlignMode): ISCH_PrimitiveText;
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

[ESCH\_PrimitiveTextAlignMode](../enums/ESCH_PrimitiveTextAlignMode.md)

</td><td>

Alignment mode

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveText](./ISCH_PrimitiveText.md)

Text primitive object

### setstate_bold

# ISCH\_PrimitiveText.setState\_Bold() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is bold

## Signature

```typescript
function setState_Bold(bold: boolean): ISCH_PrimitiveText;
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

bold

</td><td>

boolean

</td><td>

Whether it is bold

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveText](./ISCH_PrimitiveText.md)

Text primitive object

### setstate_content

# ISCH\_PrimitiveText.setState\_Content() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: text content

## Signature

```typescript
function setState_Content(content: string): ISCH_PrimitiveText;
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

content

</td><td>

string

</td><td>

Text content

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveText](./ISCH_PrimitiveText.md)

Text primitive object

### setstate_fontname

# ISCH\_PrimitiveText.setState\_FontName() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: font name

## Signature

```typescript
function setState_FontName(fontName: string | null): ISCH_PrimitiveText;
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

fontName

</td><td>

string \| null

</td><td>

Font name

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveText](./ISCH_PrimitiveText.md)

Text primitive object

### setstate_fontsize

# ISCH\_PrimitiveText.setState\_FontSize() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: font size

## Signature

```typescript
function setState_FontSize(fontSize: number | null): ISCH_PrimitiveText;
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

number \| null

</td><td>

Font size

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveText](./ISCH_PrimitiveText.md)

Text primitive object

### setstate_italic

# ISCH\_PrimitiveText.setState\_Italic() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is italic

## Signature

```typescript
function setState_Italic(italic: boolean): ISCH_PrimitiveText;
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

italic

</td><td>

boolean

</td><td>

Whether it is italic

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveText](./ISCH_PrimitiveText.md)

Text primitive object

### setstate_rotation

# ISCH\_PrimitiveText.setState\_Rotation() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: rotation angle

## Signature

```typescript
function setState_Rotation(rotation: number): ISCH_PrimitiveText;
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

[ISCH\_PrimitiveText](./ISCH_PrimitiveText.md)

Text primitive object

### setstate_textcolor

# ISCH\_PrimitiveText.setState\_TextColor() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: text color

## Signature

```typescript
function setState_TextColor(textColor: string | null): ISCH_PrimitiveText;
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

textColor

</td><td>

string \| null

</td><td>

Text color

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveText](./ISCH_PrimitiveText.md)

Text primitive object

### setstate_underline

# ISCH\_PrimitiveText.setState\_UnderLine() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is underlined

## Signature

```typescript
function setState_UnderLine(underLine: boolean): ISCH_PrimitiveText;
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

underLine

</td><td>

boolean

</td><td>

Whether it is underlined

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveText](./ISCH_PrimitiveText.md)

Text primitive object

### setstate_x

# ISCH\_PrimitiveText.setState\_X() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: X coordinate

## Signature

```typescript
function setState_X(x: number): ISCH_PrimitiveText;
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

[ISCH\_PrimitiveText](./ISCH_PrimitiveText.md)

Text primitive object

### setstate_y

# ISCH\_PrimitiveText.setState\_Y() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Y coordinate

## Signature

```typescript
function setState_Y(y: number): ISCH_PrimitiveText;
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

[ISCH\_PrimitiveText](./ISCH_PrimitiveText.md)

Text primitive object

### toasync

# ISCH\_PrimitiveText.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): ISCH_PrimitiveText;
```

## Returns

[ISCH\_PrimitiveText](./ISCH_PrimitiveText.md)

Text primitive object

### tosync

# ISCH\_PrimitiveText.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): ISCH_PrimitiveText;
```

## Returns

[ISCH\_PrimitiveText](./ISCH_PrimitiveText.md)

Text primitive object

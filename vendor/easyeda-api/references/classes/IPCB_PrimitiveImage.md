# IPCB\_PrimitiveImage class

Image primitive

## Signature

```typescript
class IPCB_PrimitiveImage implements IPCB_Primitive
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

[done()](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getState\_ComplexPolygon()](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

Get the property state: image source data ( complex polygon)

</td></tr>
<tr><td>

[getState\_Height()](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

Get the property state: height

</td></tr>
<tr><td>

[getState\_HorizonMirror()](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

Get the property state: whether it is horizontally mirrored

</td></tr>
<tr><td>

[getState\_Layer()](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

Get the property state: Layer

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveLock()](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

Get the property state: whether it is locked

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[getState\_Rotation()](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

Get the property state: rotation angle

</td></tr>
<tr><td>

[getState\_Width()](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

Get the property state: width

</td></tr>
<tr><td>

[getState\_X()](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

Get the property state: BBox top-left point coordinates X

</td></tr>
<tr><td>

[getState\_Y()](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

Get the property state: BBox top-left point coordinates Y

</td></tr>
<tr><td>

[isAsync()](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_Height(height)](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: height

</td></tr>
<tr><td>

[setState\_HorizonMirror(horizonMirror)](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is horizontally mirrored

</td></tr>
<tr><td>

[setState\_Layer(layer)](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Layer

</td></tr>
<tr><td>

[setState\_PrimitiveLock(primitiveLock)](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is locked

</td></tr>
<tr><td>

[setState\_Rotation(rotation)](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: rotation angle

</td></tr>
<tr><td>

[setState\_Width(width)](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: width

</td></tr>
<tr><td>

[setState\_X(x)](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: BBox top-left point coordinates X

</td></tr>
<tr><td>

[setState\_Y(y)](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: BBox top-left point coordinates Y

</td></tr>
<tr><td>

[toAsync()](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./IPCB_PrimitiveImage.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 方法详情

### done

# IPCB\_PrimitiveImage.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<IPCB_PrimitiveImage>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md)<!-- -->&gt;

Image primitive object

### getstate_complexpolygon

# IPCB\_PrimitiveImage.getState\_ComplexPolygon() method

Get the property state: image source data ( complex polygon)

## Signature

```typescript
function getState_ComplexPolygon(): TPCB_PolygonSourceArray | Array<TPCB_PolygonSourceArray>;
```

## Returns

[TPCB\_PolygonSourceArray](../types/TPCB_PolygonSourceArray.md) \| Array&lt;[TPCB\_PolygonSourceArray](../types/TPCB_PolygonSourceArray.md)<!-- -->&gt;

Image source data ( complex polygon)

### getstate_height

# IPCB\_PrimitiveImage.getState\_Height() method

Get the property state: height

## Signature

```typescript
function getState_Height(): number;
```

## Returns

number

Height

### getstate_horizonmirror

# IPCB\_PrimitiveImage.getState\_HorizonMirror() method

Get the property state: whether it is horizontally mirrored

## Signature

```typescript
function getState_HorizonMirror(): boolean;
```

## Returns

boolean

Whether it is horizontally mirrored

### getstate_layer

# IPCB\_PrimitiveImage.getState\_Layer() method

Get the property state: Layer

## Signature

```typescript
function getState_Layer(): TPCB_LayersOfImage;
```

## Returns

[TPCB\_LayersOfImage](../types/TPCB_LayersOfImage.md)

Layer

### getstate_primitiveid

# IPCB\_PrimitiveImage.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivelock

# IPCB\_PrimitiveImage.getState\_PrimitiveLock() method

Get the property state: whether it is locked

## Signature

```typescript
function getState_PrimitiveLock(): boolean;
```

## Returns

boolean

Whether it is locked

### getstate_primitivetype

# IPCB\_PrimitiveImage.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): EPCB_PrimitiveType;
```

## Returns

[EPCB\_PrimitiveType](../enums/EPCB_PrimitiveType.md)

Primitive type

### getstate_rotation

# IPCB\_PrimitiveImage.getState\_Rotation() method

Get the property state: rotation angle

## Signature

```typescript
function getState_Rotation(): number;
```

## Returns

number

Rotation angle

### getstate_width

# IPCB\_PrimitiveImage.getState\_Width() method

Get the property state: width

## Signature

```typescript
function getState_Width(): number;
```

## Returns

number

Width

### getstate_x

# IPCB\_PrimitiveImage.getState\_X() method

Get the property state: BBox top-left point coordinates X

## Signature

```typescript
function getState_X(): number;
```

## Returns

number

BBox top-left point coordinates X

### getstate_y

# IPCB\_PrimitiveImage.getState\_Y() method

Get the property state: BBox top-left point coordinates Y

## Signature

```typescript
function getState_Y(): number;
```

## Returns

number

BBox top-left point coordinates Y

### isasync

# IPCB\_PrimitiveImage.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# IPCB\_PrimitiveImage.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<IPCB_PrimitiveImage>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md)<!-- -->&gt;

Image primitive object

### setstate_height

# IPCB\_PrimitiveImage.setState\_Height() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: height

## Signature

```typescript
function setState_Height(height: number): IPCB_PrimitiveImage;
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

[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md)

Image primitive object

### setstate_horizonmirror

# IPCB\_PrimitiveImage.setState\_HorizonMirror() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is horizontally mirrored

## Signature

```typescript
function setState_HorizonMirror(horizonMirror: boolean): IPCB_PrimitiveImage;
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

horizonMirror

</td><td>

boolean

</td><td>

Whether it is horizontally mirrored

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md)

Image primitive object

### setstate_layer

# IPCB\_PrimitiveImage.setState\_Layer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Layer

## Signature

```typescript
function setState_Layer(layer: TPCB_LayersOfImage): IPCB_PrimitiveImage;
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

[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md)

Image primitive object

### setstate_primitivelock

# IPCB\_PrimitiveImage.setState\_PrimitiveLock() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is locked

## Signature

```typescript
function setState_PrimitiveLock(primitiveLock: boolean): IPCB_PrimitiveImage;
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

[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md)

Image primitive object

### setstate_rotation

# IPCB\_PrimitiveImage.setState\_Rotation() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: rotation angle

## Signature

```typescript
function setState_Rotation(rotation: number): IPCB_PrimitiveImage;
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

[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md)

Image primitive object

### setstate_width

# IPCB\_PrimitiveImage.setState\_Width() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: width

## Signature

```typescript
function setState_Width(width: number): IPCB_PrimitiveImage;
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

[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md)

Image primitive object

### setstate_x

# IPCB\_PrimitiveImage.setState\_X() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: BBox top-left point coordinates X

## Signature

```typescript
function setState_X(x: number): IPCB_PrimitiveImage;
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

BBox top-left point coordinates X

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md)

Image primitive object

### setstate_y

# IPCB\_PrimitiveImage.setState\_Y() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: BBox top-left point coordinates Y

## Signature

```typescript
function setState_Y(y: number): IPCB_PrimitiveImage;
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

BBox top-left point coordinates Y

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md)

Image primitive object

### toasync

# IPCB\_PrimitiveImage.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): IPCB_PrimitiveImage;
```

## Returns

[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md)

Image primitive object

### tosync

# IPCB\_PrimitiveImage.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): IPCB_PrimitiveImage;
```

## Returns

[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md)

Image primitive object

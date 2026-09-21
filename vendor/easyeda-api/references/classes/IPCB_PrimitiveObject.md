# IPCB\_PrimitiveObject class

Binary embedded object primitive

## Signature

```typescript
class IPCB_PrimitiveObject implements IPCB_Primitive
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

[done()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getState\_BinaryData()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Get the property state: binary data

</td></tr>
<tr><td>

[getState\_FileName()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Get the property state: file name

</td></tr>
<tr><td>

[getState\_Height()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Get the property state: height

</td></tr>
<tr><td>

[getState\_Layer()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Get the property state: Layer

</td></tr>
<tr><td>

[getState\_Mirror()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Get the property state: whether it is horizontally mirrored

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveLock()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Get the property state: whether it is locked

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[getState\_Rotation()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Get the property state: rotation angle

</td></tr>
<tr><td>

[getState\_TopLeftX()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Get the property state: top-left point X

</td></tr>
<tr><td>

[getState\_TopLeftY()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Get the property state: top-left point Y

</td></tr>
<tr><td>

[getState\_Width()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Get the property state: width

</td></tr>
<tr><td>

[isAsync()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_BinaryData(binaryData)](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Set the property state: binary data

</td></tr>
<tr><td>

[setState\_FileName(fileName)](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Set the property state: file name

</td></tr>
<tr><td>

[setState\_Height(height)](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Set the property state: height

</td></tr>
<tr><td>

[setState\_Layer(layer)](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Layer

</td></tr>
<tr><td>

[setState\_Mirror(mirror)](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Set the property state: whether it is horizontally mirrored

</td></tr>
<tr><td>

[setState\_PrimitiveLock(primitiveLock)](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is locked

</td></tr>
<tr><td>

[setState\_Rotation(rotation)](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Set the property state: rotation angle

</td></tr>
<tr><td>

[setState\_TopLeftX(topLeftX)](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Set the property state: top-left point X

</td></tr>
<tr><td>

[setState\_TopLeftY(topLeftY)](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Set the property state: top-left point Y

</td></tr>
<tr><td>

[setState\_Width(width)](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Set the property state: width

</td></tr>
<tr><td>

[toAsync()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./IPCB_PrimitiveObject.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 方法详情

### done

# IPCB\_PrimitiveObject.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<IPCB_PrimitiveObject>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveObject](./IPCB_PrimitiveObject.md)<!-- -->&gt;

Binary embedded object primitive object

### getstate_binarydata

# IPCB\_PrimitiveObject.getState\_BinaryData() method

Get the property state: binary data

## Signature

```typescript
function getState_BinaryData(): string;
```

## Returns

string

Binary data

## Remarks

The `binaryData` retrieved from the canvas may be a `hashId`<!-- -->, because our backend stores binary embedded object data in object storage,

The object storage uses `hashId` as the index. Fully retrieving the data will cause additional requests and consume performance

### getstate_filename

# IPCB\_PrimitiveObject.getState\_FileName() method

Get the property state: file name

## Signature

```typescript
function getState_FileName(): string;
```

## Returns

string

File name

### getstate_height

# IPCB\_PrimitiveObject.getState\_Height() method

Get the property state: height

## Signature

```typescript
function getState_Height(): number;
```

## Returns

number

Height

### getstate_layer

# IPCB\_PrimitiveObject.getState\_Layer() method

Get the property state: Layer

## Signature

```typescript
function getState_Layer(): TPCB_LayersOfObject | undefined;
```

## Returns

[TPCB\_LayersOfObject](../types/TPCB_LayersOfObject.md) \| undefined

Layer

### getstate_mirror

# IPCB\_PrimitiveObject.getState\_Mirror() method

Get the property state: whether it is horizontally mirrored

## Signature

```typescript
function getState_Mirror(): boolean;
```

## Returns

boolean

Whether it is horizontally mirrored

### getstate_primitiveid

# IPCB\_PrimitiveObject.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivelock

# IPCB\_PrimitiveObject.getState\_PrimitiveLock() method

Get the property state: whether it is locked

## Signature

```typescript
function getState_PrimitiveLock(): boolean;
```

## Returns

boolean

Whether it is locked

### getstate_primitivetype

# IPCB\_PrimitiveObject.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): EPCB_PrimitiveType;
```

## Returns

[EPCB\_PrimitiveType](../enums/EPCB_PrimitiveType.md)

Primitive type

### getstate_rotation

# IPCB\_PrimitiveObject.getState\_Rotation() method

Get the property state: rotation angle

## Signature

```typescript
function getState_Rotation(): number;
```

## Returns

number

Rotation angle

### getstate_topleftx

# IPCB\_PrimitiveObject.getState\_TopLeftX() method

Get the property state: top-left point X

## Signature

```typescript
function getState_TopLeftX(): number | undefined;
```

## Returns

number \| undefined

Top-left point X

### getstate_toplefty

# IPCB\_PrimitiveObject.getState\_TopLeftY() method

Get the property state: top-left point Y

## Signature

```typescript
function getState_TopLeftY(): number | undefined;
```

## Returns

number \| undefined

Top-left point Y

### getstate_width

# IPCB\_PrimitiveObject.getState\_Width() method

Get the property state: width

## Signature

```typescript
function getState_Width(): number;
```

## Returns

number

Width

### isasync

# IPCB\_PrimitiveObject.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# IPCB\_PrimitiveObject.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<IPCB_PrimitiveObject>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveObject](./IPCB_PrimitiveObject.md)<!-- -->&gt;

Binary embedded object primitive object

### setstate_binarydata

# IPCB\_PrimitiveObject.setState\_BinaryData() method

Set the property state: binary data

## Signature

```typescript
function setState_BinaryData(binaryData: string): IPCB_PrimitiveObject;
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

binaryData

</td><td>

string

</td><td>

Binary data

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveObject](./IPCB_PrimitiveObject.md)

Binary embedded object primitive object

## Remarks

The `binaryData` re-retrieved from the canvas may be a `hashId`<!-- -->, because our backend stores binary embedded object data in object storage,

The object storage uses `hashId` as the index. Fully retrieving the data will cause additional requests and consume performance

### setstate_filename

# IPCB\_PrimitiveObject.setState\_FileName() method

Set the property state: file name

## Signature

```typescript
function setState_FileName(fileName: string): IPCB_PrimitiveObject;
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

fileName

</td><td>

string

</td><td>

File name

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveObject](./IPCB_PrimitiveObject.md)

Binary embedded object primitive object

### setstate_height

# IPCB\_PrimitiveObject.setState\_Height() method

Set the property state: height

## Signature

```typescript
function setState_Height(height: number): IPCB_PrimitiveObject;
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

[IPCB\_PrimitiveObject](./IPCB_PrimitiveObject.md)

Binary embedded object primitive object

### setstate_layer

# IPCB\_PrimitiveObject.setState\_Layer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Layer

## Signature

```typescript
function setState_Layer(layer: TPCB_LayersOfObject): IPCB_PrimitiveObject;
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

[TPCB\_LayersOfObject](../types/TPCB_LayersOfObject.md)

</td><td>

Layer

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveObject](./IPCB_PrimitiveObject.md)

Binary embedded object primitive object

### setstate_mirror

# IPCB\_PrimitiveObject.setState\_Mirror() method

Set the property state: whether it is horizontally mirrored

## Signature

```typescript
function setState_Mirror(mirror: boolean): IPCB_PrimitiveObject;
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

Whether it is horizontally mirrored

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveObject](./IPCB_PrimitiveObject.md)

Binary embedded object primitive object

### setstate_primitivelock

# IPCB\_PrimitiveObject.setState\_PrimitiveLock() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is locked

## Signature

```typescript
function setState_PrimitiveLock(primitiveLock: boolean): IPCB_PrimitiveObject;
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

[IPCB\_PrimitiveObject](./IPCB_PrimitiveObject.md)

Binary embedded object primitive object

### setstate_rotation

# IPCB\_PrimitiveObject.setState\_Rotation() method

Set the property state: rotation angle

## Signature

```typescript
function setState_Rotation(rotation: number): IPCB_PrimitiveObject;
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

[IPCB\_PrimitiveObject](./IPCB_PrimitiveObject.md)

Binary embedded object primitive object

### setstate_topleftx

# IPCB\_PrimitiveObject.setState\_TopLeftX() method

Set the property state: top-left point X

## Signature

```typescript
function setState_TopLeftX(topLeftX: number): IPCB_PrimitiveObject;
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

[IPCB\_PrimitiveObject](./IPCB_PrimitiveObject.md)

Binary embedded object primitive object

### setstate_toplefty

# IPCB\_PrimitiveObject.setState\_TopLeftY() method

Set the property state: top-left point Y

## Signature

```typescript
function setState_TopLeftY(topLeftY: number): IPCB_PrimitiveObject;
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

[IPCB\_PrimitiveObject](./IPCB_PrimitiveObject.md)

Binary embedded object primitive object

### setstate_width

# IPCB\_PrimitiveObject.setState\_Width() method

Set the property state: width

## Signature

```typescript
function setState_Width(width: number): IPCB_PrimitiveObject;
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

[IPCB\_PrimitiveObject](./IPCB_PrimitiveObject.md)

Binary embedded object primitive object

### toasync

# IPCB\_PrimitiveObject.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): IPCB_PrimitiveObject;
```

## Returns

[IPCB\_PrimitiveObject](./IPCB_PrimitiveObject.md)

Binary embedded object primitive object

### tosync

# IPCB\_PrimitiveObject.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): IPCB_PrimitiveObject;
```

## Returns

[IPCB\_PrimitiveObject](./IPCB_PrimitiveObject.md)

Binary embedded object primitive object

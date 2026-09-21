# IPCB\_PrimitivePad class

Pad primitive

## Signature

```typescript
class IPCB_PrimitivePad implements IPCB_Primitive
```
**Implements:** [IPCB\_Primitive](../interfaces/IPCB_Primitive.md)

## Remarks

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[async](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

boolean

</td><td>

异步

</td></tr>
<tr><td>

[heatWelding](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

[IPCB\_PrimitivePadHeatWelding](../interfaces/IPCB_PrimitivePadHeatWelding.md) \| null

</td><td>

热焊优化参数

</td></tr>
<tr><td>

[hole](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

[TPCB\_PrimitivePadHole](../types/TPCB_PrimitivePadHole.md) \| null

</td><td>

孔

</td></tr>
<tr><td>

[holeOffsetX](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

number

</td><td>

孔偏移 X

</td></tr>
<tr><td>

[holeOffsetY](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

number

</td><td>

孔偏移 Y

</td></tr>
<tr><td>

[holeRotation](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

number

</td><td>

孔相对于焊盘的旋转角度

</td></tr>
<tr><td>

[layer](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

[TPCB\_LayersOfPad](../types/TPCB_LayersOfPad.md)

</td><td>

层

</td></tr>
<tr><td>

[metallization](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

boolean

</td><td>

是否金属化孔壁

</td></tr>
<tr><td>

[net?](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

string

</td><td>

_(Optional)_ 网络名称

</td></tr>
<tr><td>

[pad?](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

[TPCB\_PrimitivePadShape](../types/TPCB_PrimitivePadShape.md)

</td><td>

_(Optional)_ 焊盘外形

</td></tr>
<tr><td>

[padNumber](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

string

</td><td>

焊盘编号

</td></tr>
<tr><td>

[padType](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

[EPCB\_PrimitivePadType](../enums/EPCB_PrimitivePadType.md)

</td><td>

焊盘类型

</td></tr>
<tr><td>

[primitiveId?](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

string

</td><td>

_(Optional)_ 图元 ID

</td></tr>
<tr><td>

[primitiveLock](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

boolean

</td><td>

是否锁定

</td></tr>
<tr><td>

[primitiveType](./IPCB_PrimitivePad.md)

</td><td>

`protected`

`readonly`

</td><td>

[EPCB\_PrimitiveType](../enums/EPCB_PrimitiveType.md)

</td><td>

图元类型

</td></tr>
<tr><td>

[rotation](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

number

</td><td>

旋转角度

</td></tr>
<tr><td>

[solderMaskAndPasteMaskExpansion](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

[IPCB\_PrimitiveSolderMaskAndPasteMaskExpansion](../interfaces/IPCB_PrimitiveSolderMaskAndPasteMaskExpansion.md) \| null

</td><td>

阻焊/助焊扩展

</td></tr>
<tr><td>

[specialPad?](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

[TPCB\_PrimitiveSpecialPadShape](../types/TPCB_PrimitiveSpecialPadShape.md)

</td><td>

_(Optional)_ 特殊焊盘外形

</td></tr>
<tr><td>

[x](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

number

</td><td>

位置 X

</td></tr>
<tr><td>

[y](./IPCB_PrimitivePad.md)

</td><td>

`protected`

</td><td>

number

</td><td>

位置 Y

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

[create()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** In PCB canvas in create primitive

</td></tr>
<tr><td>

[done()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getState\_HeatWelding()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: thermal relief optimization parameters

</td></tr>
<tr><td>

[getState\_Hole()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: hole

</td></tr>
<tr><td>

[getState\_HoleOffsetX()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: hole offset X

</td></tr>
<tr><td>

[getState\_HoleOffsetY()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: hole offset Y

</td></tr>
<tr><td>

[getState\_HoleRotation()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: Rotation angle of the hole relative to the pad

</td></tr>
<tr><td>

[getState\_Layer()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: Layer

</td></tr>
<tr><td>

[getState\_Metallization()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: Whether the hole wall is plated

</td></tr>
<tr><td>

[getState\_Net()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: net name

</td></tr>
<tr><td>

[getState\_Pad()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: pad shape

</td></tr>
<tr><td>

[getState\_PadNumber()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: pad number

</td></tr>
<tr><td>

[getState\_PadType()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: pad type

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveLock()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: whether it is locked

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[getState\_Rotation()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: rotation angle

</td></tr>
<tr><td>

[getState\_SolderMaskAndPasteMaskExpansion()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: solder mask / paste mask expansion

</td></tr>
<tr><td>

[getState\_SpecialPad()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: special pad shape

</td></tr>
<tr><td>

[getState\_X()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: X position

</td></tr>
<tr><td>

[getState\_Y()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Get the property state: Y position

</td></tr>
<tr><td>

[isAsync()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_HeatWelding(heatWelding)](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: thermal relief optimization parameters

</td></tr>
<tr><td>

[setState\_Hole(hole)](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: hole

</td></tr>
<tr><td>

[setState\_HoleOffsetX(holeOffsetX)](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: hole offset X

</td></tr>
<tr><td>

[setState\_HoleOffsetY(holeOffsetY)](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: hole offset Y

</td></tr>
<tr><td>

[setState\_HoleRotation(holeRotation)](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Rotation angle of the hole relative to the pad

</td></tr>
<tr><td>

[setState\_Layer(layer)](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Layer

</td></tr>
<tr><td>

[setState\_Metallization(metallization)](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Whether the hole wall is plated

</td></tr>
<tr><td>

[setState\_Net(net)](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: net

</td></tr>
<tr><td>

[setState\_Pad(pad)](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: pad shape

</td></tr>
<tr><td>

[setState\_PadNumber(padNumber)](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: pad number

</td></tr>
<tr><td>

[setState\_PrimitiveLock(primitiveLock)](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is locked

</td></tr>
<tr><td>

[setState\_Rotation(rotation)](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: rotation angle

</td></tr>
<tr><td>

[setState\_SolderMaskAndPasteMaskExpansion(solderMaskAndPasteMaskExpansion)](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: solder mask / paste mask expansion

</td></tr>
<tr><td>

[setState\_SpecialPad(specialPad)](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: special pad shape

</td></tr>
<tr><td>

[setState\_X(x)](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: X position

</td></tr>
<tr><td>

[setState\_Y(y)](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Y position

</td></tr>
<tr><td>

[toAsync()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./IPCB_PrimitivePad.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 属性详情

### async

# IPCB\_PrimitivePad.async property

异步

## Signature

```typescript
function async: boolean;
```

### heatwelding

# IPCB\_PrimitivePad.heatWelding property

热焊优化参数

## Signature

```typescript
function heatWelding: IPCB_PrimitivePadHeatWelding | null;
```

### hole

# IPCB\_PrimitivePad.hole property

孔

## Signature

```typescript
function hole: TPCB_PrimitivePadHole | null;
```

### holeoffsetx

# IPCB\_PrimitivePad.holeOffsetX property

孔偏移 X

## Signature

```typescript
function holeOffsetX: number;
```

### holeoffsety

# IPCB\_PrimitivePad.holeOffsetY property

孔偏移 Y

## Signature

```typescript
function holeOffsetY: number;
```

### holerotation

# IPCB\_PrimitivePad.holeRotation property

孔相对于焊盘的旋转角度

## Signature

```typescript
function holeRotation: number;
```

### layer

# IPCB\_PrimitivePad.layer property

层

## Signature

```typescript
function layer: TPCB_LayersOfPad;
```

### metallization

# IPCB\_PrimitivePad.metallization property

是否金属化孔壁

## Signature

```typescript
function metallization: boolean;
```

### net

# IPCB\_PrimitivePad.net property

网络名称

## Signature

```typescript
function net?: string;
```

### pad

# IPCB\_PrimitivePad.pad property

焊盘外形

## Signature

```typescript
function pad?: TPCB_PrimitivePadShape;
```

### padnumber

# IPCB\_PrimitivePad.padNumber property

焊盘编号

## Signature

```typescript
function padNumber: string;
```

### padtype

# IPCB\_PrimitivePad.padType property

焊盘类型

## Signature

```typescript
function padType: EPCB_PrimitivePadType;
```

### primitiveid

# IPCB\_PrimitivePad.primitiveId property

图元 ID

## Signature

```typescript
function primitiveId?: string;
```

### primitivelock

# IPCB\_PrimitivePad.primitiveLock property

是否锁定

## Signature

```typescript
function primitiveLock: boolean;
```

### primitivetype

# IPCB\_PrimitivePad.primitiveType property

图元类型

## Signature

```typescript
function readonly primitiveType: EPCB_PrimitiveType;
```

### rotation

# IPCB\_PrimitivePad.rotation property

旋转角度

## Signature

```typescript
function rotation: number;
```

### soldermaskandpastemaskexpansion

# IPCB\_PrimitivePad.solderMaskAndPasteMaskExpansion property

阻焊/助焊扩展

## Signature

```typescript
function solderMaskAndPasteMaskExpansion: IPCB_PrimitiveSolderMaskAndPasteMaskExpansion | null;
```

### specialpad

# IPCB\_PrimitivePad.specialPad property

特殊焊盘外形

## Signature

```typescript
function specialPad?: TPCB_PrimitiveSpecialPadShape;
```

### x

# IPCB\_PrimitivePad.x property

位置 X

## Signature

```typescript
function x: number;
```

### y

# IPCB\_PrimitivePad.y property

位置 Y

## Signature

```typescript
function y: number;
```


---

## 方法详情

### create

# IPCB\_PrimitivePad.create() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

In PCB canvas in create primitive

## Signature

```typescript
function create(): Promise<IPCB_PrimitivePad>;
```

## Returns

Promise&lt;[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)<!-- -->&gt;

Pad primitive object

### done

# IPCB\_PrimitivePad.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<IPCB_PrimitivePad>;
```

## Returns

Promise&lt;[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)<!-- -->&gt;

Dimension primitive object

### getstate_heatwelding

# IPCB\_PrimitivePad.getState\_HeatWelding() method

Get the property state: thermal relief optimization parameters

## Signature

```typescript
function getState_HeatWelding(): IPCB_PrimitivePadHeatWelding | null;
```

## Returns

[IPCB\_PrimitivePadHeatWelding](../interfaces/IPCB_PrimitivePadHeatWelding.md) \| null

Thermal relief optimization parameters

### getstate_hole

# IPCB\_PrimitivePad.getState\_Hole() method

Get the property state: hole

## Signature

```typescript
function getState_Hole(): TPCB_PrimitivePadHole | null;
```

## Returns

[TPCB\_PrimitivePadHole](../types/TPCB_PrimitivePadHole.md) \| null

Hole

### getstate_holeoffsetx

# IPCB\_PrimitivePad.getState\_HoleOffsetX() method

Get the property state: hole offset X

## Signature

```typescript
function getState_HoleOffsetX(): number;
```

## Returns

number

Hole offset X

### getstate_holeoffsety

# IPCB\_PrimitivePad.getState\_HoleOffsetY() method

Get the property state: hole offset Y

## Signature

```typescript
function getState_HoleOffsetY(): number;
```

## Returns

number

Hole offset Y

### getstate_holerotation

# IPCB\_PrimitivePad.getState\_HoleRotation() method

Get the property state: Rotation angle of the hole relative to the pad

## Signature

```typescript
function getState_HoleRotation(): number;
```

## Returns

number

Rotation angle of the hole relative to the pad

### getstate_layer

# IPCB\_PrimitivePad.getState\_Layer() method

Get the property state: Layer

## Signature

```typescript
function getState_Layer(): TPCB_LayersOfPad;
```

## Returns

[TPCB\_LayersOfPad](../types/TPCB_LayersOfPad.md)

Layer

### getstate_metallization

# IPCB\_PrimitivePad.getState\_Metallization() method

Get the property state: Whether the hole wall is plated

## Signature

```typescript
function getState_Metallization(): boolean;
```

## Returns

boolean

Whether the hole wall is plated

### getstate_net

# IPCB\_PrimitivePad.getState\_Net() method

Get the property state: net name

## Signature

```typescript
function getState_Net(): string | undefined;
```

## Returns

string \| undefined

Net name

### getstate_pad

# IPCB\_PrimitivePad.getState\_Pad() method

Get the property state: pad shape

## Signature

```typescript
function getState_Pad(): TPCB_PrimitivePadShape | undefined;
```

## Returns

[TPCB\_PrimitivePadShape](../types/TPCB_PrimitivePadShape.md) \| undefined

Pad shape

### getstate_padnumber

# IPCB\_PrimitivePad.getState\_PadNumber() method

Get the property state: pad number

## Signature

```typescript
function getState_PadNumber(): string;
```

## Returns

string

Pad number

### getstate_padtype

# IPCB\_PrimitivePad.getState\_PadType() method

Get the property state: pad type

## Signature

```typescript
function getState_PadType(): EPCB_PrimitivePadType;
```

## Returns

[EPCB\_PrimitivePadType](../enums/EPCB_PrimitivePadType.md)

Pad type

### getstate_primitiveid

# IPCB\_PrimitivePad.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivelock

# IPCB\_PrimitivePad.getState\_PrimitiveLock() method

Get the property state: whether it is locked

## Signature

```typescript
function getState_PrimitiveLock(): boolean;
```

## Returns

boolean

Whether it is locked

### getstate_primitivetype

# IPCB\_PrimitivePad.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): EPCB_PrimitiveType;
```

## Returns

[EPCB\_PrimitiveType](../enums/EPCB_PrimitiveType.md)

Primitive type

### getstate_rotation

# IPCB\_PrimitivePad.getState\_Rotation() method

Get the property state: rotation angle

## Signature

```typescript
function getState_Rotation(): number;
```

## Returns

number

Rotation angle

### getstate_soldermaskandpastemaskexpansion

# IPCB\_PrimitivePad.getState\_SolderMaskAndPasteMaskExpansion() method

Get the property state: solder mask / paste mask expansion

## Signature

```typescript
function getState_SolderMaskAndPasteMaskExpansion(): IPCB_PrimitiveSolderMaskAndPasteMaskExpansion | null;
```

## Returns

[IPCB\_PrimitiveSolderMaskAndPasteMaskExpansion](../interfaces/IPCB_PrimitiveSolderMaskAndPasteMaskExpansion.md) \| null

Solder mask / paste mask expansion

### getstate_specialpad

# IPCB\_PrimitivePad.getState\_SpecialPad() method

Get the property state: special pad shape

## Signature

```typescript
function getState_SpecialPad(): TPCB_PrimitiveSpecialPadShape | undefined;
```

## Returns

[TPCB\_PrimitiveSpecialPadShape](../types/TPCB_PrimitiveSpecialPadShape.md) \| undefined

Special pad shape

### getstate_x

# IPCB\_PrimitivePad.getState\_X() method

Get the property state: X position

## Signature

```typescript
function getState_X(): number;
```

## Returns

number

X position

### getstate_y

# IPCB\_PrimitivePad.getState\_Y() method

Get the property state: Y position

## Signature

```typescript
function getState_Y(): number;
```

## Returns

number

Y position

### isasync

# IPCB\_PrimitivePad.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# IPCB\_PrimitivePad.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<IPCB_PrimitivePad>;
```

## Returns

Promise&lt;[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)<!-- -->&gt;

Pad primitive object

### setstate_heatwelding

# IPCB\_PrimitivePad.setState\_HeatWelding() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: thermal relief optimization parameters

## Signature

```typescript
function setState_HeatWelding(heatWelding: IPCB_PrimitivePadHeatWelding | null): IPCB_PrimitivePad;
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

heatWelding

</td><td>

[IPCB\_PrimitivePadHeatWelding](../interfaces/IPCB_PrimitivePadHeatWelding.md) \| null

</td><td>

Thermal relief optimization parameters

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

### setstate_hole

# IPCB\_PrimitivePad.setState\_Hole() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: hole

## Signature

```typescript
function setState_Hole(hole: TPCB_PrimitivePadHole): IPCB_PrimitivePad;
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

hole

</td><td>

[TPCB\_PrimitivePadHole](../types/TPCB_PrimitivePadHole.md)

</td><td>

Pad drilling

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

## Remarks

When setting the hole, some other property states will be set in conjunction:

1. The layer will be forcibly switched to multi-layer

This API cannot set the hole to `null`<!-- -->. If you want to remove the hole property, use the [setState\_Layer](./IPCB_PrimitivePad.md) method to switch the layer to the top or bottom layer

### setstate_holeoffsetx

# IPCB\_PrimitivePad.setState\_HoleOffsetX() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: hole offset X

## Signature

```typescript
function setState_HoleOffsetX(holeOffsetX: number): IPCB_PrimitivePad;
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

holeOffsetX

</td><td>

number

</td><td>

Hole offset X

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

## Remarks

If the hole does not exist, the property will not be modified

### setstate_holeoffsety

# IPCB\_PrimitivePad.setState\_HoleOffsetY() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: hole offset Y

## Signature

```typescript
function setState_HoleOffsetY(holeOffsetY: number): IPCB_PrimitivePad;
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

holeOffsetY

</td><td>

number

</td><td>

Hole offset Y

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

## Remarks

If the hole does not exist, the property will not be modified

### setstate_holerotation

# IPCB\_PrimitivePad.setState\_HoleRotation() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Rotation angle of the hole relative to the pad

## Signature

```typescript
function setState_HoleRotation(holeRotation: number): IPCB_PrimitivePad;
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

holeRotation

</td><td>

number

</td><td>

Rotation angle of the hole relative to the pad

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

## Remarks

If the hole does not exist, the property will not be modified

### setstate_layer

# IPCB\_PrimitivePad.setState\_Layer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Layer

## Signature

```typescript
function setState_Layer(layer: TPCB_LayersOfPad): IPCB_PrimitivePad;
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

[TPCB\_LayersOfPad](../types/TPCB_LayersOfPad.md)

</td><td>

Layer

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

## Remarks

When setting the layer, some other property states will be set in conjunction:

1. When switching between the top and bottom layers: the solder mask/paste mask expansion properties will switch accordingly, and the data values remain unchanged

2. When switching from multi-layer to single layer: it determines whether to switch to the top or bottom layer, and the solder mask/paste mask expansion properties will only keep the data corresponding to the specified layer. If a special pad exists, it will be converted to a normal pad property, and only the data corresponding to the specified layer will be kept. Hole-related properties will be reset to their default values

3. When switching from single layer to multi-layer: the solder mask/paste mask expansion properties will only keep the solder mask expansion, and the original data will be copied and applied to the top and bottom layers. The pad drilling property will be assigned a specified value: a rounded rectangle whose length and width are 60% of the pad diameter (for rounded or regular polygon pads) or the pad width (for rectangular pads). Data-wise it is a rounded rectangle, but actually it is a circle. If the pad is a polyline complex polygon, the data is calculated through a dedicated algorithm (usually abstract; it is recommended to modify it later)

### setstate_metallization

# IPCB\_PrimitivePad.setState\_Metallization() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Whether the hole wall is plated

## Signature

```typescript
function setState_Metallization(metallization: boolean): IPCB_PrimitivePad;
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

metallization

</td><td>

boolean

</td><td>

Whether the hole wall is plated

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

## Remarks

If the hole does not exist, the property will not be modified

### setstate_net

# IPCB\_PrimitivePad.setState\_Net() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: net

## Signature

```typescript
function setState_Net(net?: string): IPCB_PrimitivePad;
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

_(Optional)_ Net name

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

## Remarks

This API is only available in the PCB editor. Both an empty string and `undefined` are treated as an empty net

### setstate_pad

# IPCB\_PrimitivePad.setState\_Pad() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: pad shape

## Signature

```typescript
function setState_Pad(pad: TPCB_PrimitivePadShape): IPCB_PrimitivePad;
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

pad

</td><td>

[TPCB\_PrimitivePadShape](../types/TPCB_PrimitivePadShape.md)

</td><td>

Pad shape

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

## Remarks

When setting the pad shape, some other property states will be set in conjunction:

1. The special pad shape property will be cleared

### setstate_padnumber

# IPCB\_PrimitivePad.setState\_PadNumber() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: pad number

## Signature

```typescript
function setState_PadNumber(padNumber: string): IPCB_PrimitivePad;
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

padNumber

</td><td>

string

</td><td>

Pad number

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

### setstate_primitivelock

# IPCB\_PrimitivePad.setState\_PrimitiveLock() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is locked

## Signature

```typescript
function setState_PrimitiveLock(primitiveLock: boolean): IPCB_PrimitivePad;
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

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

### setstate_rotation

# IPCB\_PrimitivePad.setState\_Rotation() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: rotation angle

## Signature

```typescript
function setState_Rotation(rotation: number): IPCB_PrimitivePad;
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

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

### setstate_soldermaskandpastemaskexpansion

# IPCB\_PrimitivePad.setState\_SolderMaskAndPasteMaskExpansion() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: solder mask / paste mask expansion

## Signature

```typescript
function setState_SolderMaskAndPasteMaskExpansion(
	solderMaskAndPasteMaskExpansion: IPCB_PrimitiveSolderMaskAndPasteMaskExpansion | null,
): IPCB_PrimitivePad;
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

solderMaskAndPasteMaskExpansion

</td><td>

[IPCB\_PrimitiveSolderMaskAndPasteMaskExpansion](../interfaces/IPCB_PrimitiveSolderMaskAndPasteMaskExpansion.md) \| null

</td><td>

Solder mask / paste mask expansion

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

### setstate_specialpad

# IPCB\_PrimitivePad.setState\_SpecialPad() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: special pad shape

## Signature

```typescript
function setState_SpecialPad(specialPad: TPCB_PrimitiveSpecialPadShape): IPCB_PrimitivePad;
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

specialPad

</td><td>

[TPCB\_PrimitiveSpecialPadShape](../types/TPCB_PrimitiveSpecialPadShape.md)

</td><td>

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

## Remarks

When setting the special pad shape, some other property states will be set in conjunction:

1. The pad shape property will be cleared

### setstate_x

# IPCB\_PrimitivePad.setState\_X() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: X position

## Signature

```typescript
function setState_X(x: number): IPCB_PrimitivePad;
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

X position

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

### setstate_y

# IPCB\_PrimitivePad.setState\_Y() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Y position

## Signature

```typescript
function setState_Y(y: number): IPCB_PrimitivePad;
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

Y position

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

### toasync

# IPCB\_PrimitivePad.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): IPCB_PrimitivePad;
```

## Returns

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

### tosync

# IPCB\_PrimitivePad.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): IPCB_PrimitivePad;
```

## Returns

[IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

Pad primitive object

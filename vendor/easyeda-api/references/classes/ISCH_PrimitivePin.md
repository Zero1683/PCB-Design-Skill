# ISCH\_PrimitivePin class

Pin primitive

## Signature

```typescript
class ISCH_PrimitivePin implements ISCH_Primitive
```
**Implements:** [ISCH\_Primitive](../interfaces/ISCH_Primitive.md)

## Remarks

Pin primitives are only available in the symbol editor. In a schematic sheet, the pin associated with a symbol is called [a device pin primitive](./ISCH_PrimitiveComponentPin.md)

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

[async](./ISCH_PrimitivePin.md)

</td><td>

`protected`

</td><td>

boolean

</td><td>

异步

</td></tr>
<tr><td>

[noConnected?](./ISCH_PrimitivePin.md)

</td><td>

`protected`

</td><td>

boolean

</td><td>

_(Optional)_ 是否存在非连接标识

</td></tr>
<tr><td>

[otherProperty?](./ISCH_PrimitivePin.md)

</td><td>

`protected`

</td><td>

Record&lt;string, string \| number \| boolean&gt;

</td><td>

_(Optional)_ 其它参数

</td></tr>
<tr><td>

[pinColor](./ISCH_PrimitivePin.md)

</td><td>

`protected`

</td><td>

string \| null

</td><td>

引脚颜色

</td></tr>
<tr><td>

[pinLength](./ISCH_PrimitivePin.md)

</td><td>

`protected`

</td><td>

number

</td><td>

引脚长度

</td></tr>
<tr><td>

[pinName](./ISCH_PrimitivePin.md)

</td><td>

`protected`

</td><td>

string

</td><td>

引脚名称

</td></tr>
<tr><td>

[pinNumber](./ISCH_PrimitivePin.md)

</td><td>

`protected`

</td><td>

string

</td><td>

引脚编号

</td></tr>
<tr><td>

[pinShape](./ISCH_PrimitivePin.md)

</td><td>

`protected`

</td><td>

[ESCH\_PrimitivePinShape](../enums/ESCH_PrimitivePinShape.md)

</td><td>

引脚形状

</td></tr>
<tr><td>

[pinType](./ISCH_PrimitivePin.md)

</td><td>

`protected`

</td><td>

[ESCH\_PrimitivePinType](../enums/ESCH_PrimitivePinType.md)

</td><td>

引脚类型

</td></tr>
<tr><td>

[primitiveId?](./ISCH_PrimitivePin.md)

</td><td>

`protected`

</td><td>

string

</td><td>

_(Optional)_ 图元 ID

</td></tr>
<tr><td>

[primitiveType](./ISCH_PrimitivePin.md)

</td><td>

`protected`

`readonly`

</td><td>

[ESCH\_PrimitiveType](../enums/ESCH_PrimitiveType.md)

</td><td>

图元类型

</td></tr>
<tr><td>

[rotation](./ISCH_PrimitivePin.md)

</td><td>

`protected`

</td><td>

number

</td><td>

旋转角度

</td></tr>
<tr><td>

[x](./ISCH_PrimitivePin.md)

</td><td>

`protected`

</td><td>

number

</td><td>

坐标 X

</td></tr>
<tr><td>

[y](./ISCH_PrimitivePin.md)

</td><td>

`protected`

</td><td>

number

</td><td>

坐标 Y

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

[done()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getState\_NoConnected()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

Get the property state: whether there is a no-connect flag

</td></tr>
<tr><td>

[getState\_OtherProperty()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

Get the property state: other parameters

</td></tr>
<tr><td>

[getState\_PinColor()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

Get the property state: pin color

</td></tr>
<tr><td>

[getState\_PinLength()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

Get the property state: pin length

</td></tr>
<tr><td>

[getState\_PinName()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

Get the property state: pin name

</td></tr>
<tr><td>

[getState\_PinNumber()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

Get the property state: pin number

</td></tr>
<tr><td>

[getState\_PinShape()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

Get the property state: pin shape

</td></tr>
<tr><td>

[getState\_pinType()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

Get the property state: pin type

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[getState\_Rotation()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

Get the property state: rotation angle

</td></tr>
<tr><td>

[getState\_X()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

Get the property state: X coordinate

</td></tr>
<tr><td>

[getState\_Y()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

Get the property state: Y coordinate

</td></tr>
<tr><td>

[isAsync()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_NoConnected(noConnected)](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether there is a no-connect flag

</td></tr>
<tr><td>

[setState\_OtherProperty(otherProperty)](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: other parameters

</td></tr>
<tr><td>

[setState\_PinColor(pinColor)](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: pin color

</td></tr>
<tr><td>

[setState\_PinLength(pinLength)](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: pin length

</td></tr>
<tr><td>

[setState\_PinName(pinName)](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: pin name

</td></tr>
<tr><td>

[setState\_PinNumber(pinNumber)](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: pin number

</td></tr>
<tr><td>

[setState\_PinShape(pinShape)](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: pin shape

</td></tr>
<tr><td>

[setState\_PinType(pinType)](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: pin type

</td></tr>
<tr><td>

[setState\_Rotation(rotation)](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: rotation angle

</td></tr>
<tr><td>

[setState\_X(x)](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: X coordinate

</td></tr>
<tr><td>

[setState\_Y(y)](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Y coordinate

</td></tr>
<tr><td>

[toAsync()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./ISCH_PrimitivePin.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 属性详情

### async

# ISCH\_PrimitivePin.async property

异步

## Signature

```typescript
function async: boolean;
```

### noconnected

# ISCH\_PrimitivePin.noConnected property

是否存在非连接标识

## Signature

```typescript
function noConnected?: boolean;
```

### otherproperty

# ISCH\_PrimitivePin.otherProperty property

其它参数

## Signature

```typescript
function otherProperty?: Record<string, string | number | boolean>;
```

### pincolor

# ISCH\_PrimitivePin.pinColor property

引脚颜色

## Signature

```typescript
function pinColor: string | null;
```

### pinlength

# ISCH\_PrimitivePin.pinLength property

引脚长度

## Signature

```typescript
function pinLength: number;
```

### pinname

# ISCH\_PrimitivePin.pinName property

引脚名称

## Signature

```typescript
function pinName: string;
```

### pinnumber

# ISCH\_PrimitivePin.pinNumber property

引脚编号

## Signature

```typescript
function pinNumber: string;
```

### pinshape

# ISCH\_PrimitivePin.pinShape property

引脚形状

## Signature

```typescript
function pinShape: ESCH_PrimitivePinShape;
```

### pintype

# ISCH\_PrimitivePin.pinType property

引脚类型

## Signature

```typescript
function pinType: ESCH_PrimitivePinType;
```

### primitiveid

# ISCH\_PrimitivePin.primitiveId property

图元 ID

## Signature

```typescript
function primitiveId?: string;
```

### primitivetype

# ISCH\_PrimitivePin.primitiveType property

图元类型

## Signature

```typescript
function readonly primitiveType: ESCH_PrimitiveType;
```

### rotation

# ISCH\_PrimitivePin.rotation property

旋转角度

## Signature

```typescript
function rotation: number;
```

### x

# ISCH\_PrimitivePin.x property

坐标 X

## Signature

```typescript
function x: number;
```

### y

# ISCH\_PrimitivePin.y property

坐标 Y

## Signature

```typescript
function y: number;
```


---

## 方法详情

### done

# ISCH\_PrimitivePin.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<ISCH_PrimitivePin>;
```

## Returns

Promise&lt;[ISCH\_PrimitivePin](./ISCH_PrimitivePin.md)<!-- -->&gt;

Pin primitive object

### getstate_noconnected

# ISCH\_PrimitivePin.getState\_NoConnected() method

Get the property state: whether there is a no-connect flag

## Signature

```typescript
function getState_NoConnected(): boolean | undefined;
```

## Returns

boolean \| undefined

Whether there is a no-connect flag

### getstate_otherproperty

# ISCH\_PrimitivePin.getState\_OtherProperty() method

Get the property state: other parameters

## Signature

```typescript
function getState_OtherProperty(): Record<string, string | number | boolean> | undefined;
```

## Returns

Record&lt;string, string \| number \| boolean&gt; \| undefined

Other parameters

### getstate_pincolor

# ISCH\_PrimitivePin.getState\_PinColor() method

Get the property state: pin color

## Signature

```typescript
function getState_PinColor(): string | null;
```

## Returns

string \| null

Pin color

### getstate_pinlength

# ISCH\_PrimitivePin.getState\_PinLength() method

Get the property state: pin length

## Signature

```typescript
function getState_PinLength(): number;
```

## Returns

number

Pin length

### getstate_pinname

# ISCH\_PrimitivePin.getState\_PinName() method

Get the property state: pin name

## Signature

```typescript
function getState_PinName(): string;
```

## Returns

string

Pin name

### getstate_pinnumber

# ISCH\_PrimitivePin.getState\_PinNumber() method

Get the property state: pin number

## Signature

```typescript
function getState_PinNumber(): string;
```

## Returns

string

Pin number

### getstate_pinshape

# ISCH\_PrimitivePin.getState\_PinShape() method

Get the property state: pin shape

## Signature

```typescript
function getState_PinShape(): ESCH_PrimitivePinShape;
```

## Returns

[ESCH\_PrimitivePinShape](../enums/ESCH_PrimitivePinShape.md)

Pin shape

### getstate_pintype

# ISCH\_PrimitivePin.getState\_pinType() method

Get the property state: pin type

## Signature

```typescript
function getState_pinType(): ESCH_PrimitivePinType;
```

## Returns

[ESCH\_PrimitivePinType](../enums/ESCH_PrimitivePinType.md)

Pin type

### getstate_primitiveid

# ISCH\_PrimitivePin.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivetype

# ISCH\_PrimitivePin.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): ESCH_PrimitiveType;
```

## Returns

[ESCH\_PrimitiveType](../enums/ESCH_PrimitiveType.md)

Primitive type

### getstate_rotation

# ISCH\_PrimitivePin.getState\_Rotation() method

Get the property state: rotation angle

## Signature

```typescript
function getState_Rotation(): number;
```

## Returns

number

Rotation angle

### getstate_x

# ISCH\_PrimitivePin.getState\_X() method

Get the property state: X coordinate

## Signature

```typescript
function getState_X(): number;
```

## Returns

number

X coordinate

### getstate_y

# ISCH\_PrimitivePin.getState\_Y() method

Get the property state: Y coordinate

## Signature

```typescript
function getState_Y(): number;
```

## Returns

number

Y coordinate

### isasync

# ISCH\_PrimitivePin.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# ISCH\_PrimitivePin.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<ISCH_PrimitivePin>;
```

## Returns

Promise&lt;[ISCH\_PrimitivePin](./ISCH_PrimitivePin.md)<!-- -->&gt;

Pin primitive object

### setstate_noconnected

# ISCH\_PrimitivePin.setState\_NoConnected() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether there is a no-connect flag

## Signature

```typescript
function setState_NoConnected(noConnected: boolean): ISCH_PrimitivePin;
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

noConnected

</td><td>

boolean

</td><td>

Whether there is a no-connect flag

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitivePin](./ISCH_PrimitivePin.md)

Pin primitive object

### setstate_otherproperty

# ISCH\_PrimitivePin.setState\_OtherProperty() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: other parameters

## Signature

```typescript
function setState_OtherProperty(
	otherProperty: Record<string, string | number | boolean>,
): ISCH_PrimitivePin;
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

otherProperty

</td><td>

Record&lt;string, string \| number \| boolean&gt;

</td><td>

Other parameters

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitivePin](./ISCH_PrimitivePin.md)

Pin primitive object

### setstate_pincolor

# ISCH\_PrimitivePin.setState\_PinColor() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: pin color

## Signature

```typescript
function setState_PinColor(pinColor: string | null): ISCH_PrimitivePin;
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

pinColor

</td><td>

string \| null

</td><td>

Pin color

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitivePin](./ISCH_PrimitivePin.md)

Pin primitive object

### setstate_pinlength

# ISCH\_PrimitivePin.setState\_PinLength() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: pin length

## Signature

```typescript
function setState_PinLength(pinLength: number): ISCH_PrimitivePin;
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

pinLength

</td><td>

number

</td><td>

Pin length

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitivePin](./ISCH_PrimitivePin.md)

Pin primitive object

### setstate_pinname

# ISCH\_PrimitivePin.setState\_PinName() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: pin name

## Signature

```typescript
function setState_PinName(pinName: string): ISCH_PrimitivePin;
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

pinName

</td><td>

string

</td><td>

Pin name

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitivePin](./ISCH_PrimitivePin.md)

Pin primitive object

### setstate_pinnumber

# ISCH\_PrimitivePin.setState\_PinNumber() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: pin number

## Signature

```typescript
function setState_PinNumber(pinNumber: string): ISCH_PrimitivePin;
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

pinNumber

</td><td>

string

</td><td>

Pin number

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitivePin](./ISCH_PrimitivePin.md)

Pin primitive object

### setstate_pinshape

# ISCH\_PrimitivePin.setState\_PinShape() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: pin shape

## Signature

```typescript
function setState_PinShape(pinShape: ESCH_PrimitivePinShape): ISCH_PrimitivePin;
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

pinShape

</td><td>

[ESCH\_PrimitivePinShape](../enums/ESCH_PrimitivePinShape.md)

</td><td>

Pin shape

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitivePin](./ISCH_PrimitivePin.md)

Pin primitive object

### setstate_pintype

# ISCH\_PrimitivePin.setState\_PinType() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: pin type

## Signature

```typescript
function setState_PinType(pinType: ESCH_PrimitivePinType): ISCH_PrimitivePin;
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

pinType

</td><td>

[ESCH\_PrimitivePinType](../enums/ESCH_PrimitivePinType.md)

</td><td>

Pin type

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitivePin](./ISCH_PrimitivePin.md)

Pin primitive object

### setstate_rotation

# ISCH\_PrimitivePin.setState\_Rotation() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: rotation angle

## Signature

```typescript
function setState_Rotation(rotation: number): ISCH_PrimitivePin;
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

[ISCH\_PrimitivePin](./ISCH_PrimitivePin.md)

Pin primitive object

### setstate_x

# ISCH\_PrimitivePin.setState\_X() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: X coordinate

## Signature

```typescript
function setState_X(x: number): ISCH_PrimitivePin;
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

[ISCH\_PrimitivePin](./ISCH_PrimitivePin.md)

Pin primitive object

### setstate_y

# ISCH\_PrimitivePin.setState\_Y() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Y coordinate

## Signature

```typescript
function setState_Y(y: number): ISCH_PrimitivePin;
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

[ISCH\_PrimitivePin](./ISCH_PrimitivePin.md)

Pin primitive object

### toasync

# ISCH\_PrimitivePin.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): ISCH_PrimitivePin;
```

## Returns

[ISCH\_PrimitivePin](./ISCH_PrimitivePin.md)

Pin primitive object

### tosync

# ISCH\_PrimitivePin.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): ISCH_PrimitivePin;
```

## Returns

[ISCH\_PrimitivePin](./ISCH_PrimitivePin.md)

Pin primitive object

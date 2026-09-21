# ISCH\_PrimitiveComponent class

Device primitive

## Signature

```typescript
class ISCH_PrimitiveComponent implements ISCH_Primitive
```
**Implements:** [ISCH\_Primitive](../interfaces/ISCH_Primitive.md)

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

[async](./ISCH_PrimitiveComponent.md)

</td><td>

`protected`

</td><td>

boolean

</td><td>

异步

</td></tr>
<tr><td>

[designator?](./ISCH_PrimitiveComponent.md)

</td><td>

`protected`

</td><td>

string

</td><td>

_(Optional)_ Component 属性：位号

</td></tr>
<tr><td>

[mirror](./ISCH_PrimitiveComponent.md)

</td><td>

`protected`

</td><td>

boolean

</td><td>

是否镜像

</td></tr>
<tr><td>

[name?](./ISCH_PrimitiveComponent.md)

</td><td>

`protected`

</td><td>

string

</td><td>

_(Optional)_ Component 属性：名称

</td></tr>
<tr><td>

[otherProperty?](./ISCH_PrimitiveComponent.md)

</td><td>

`protected`

</td><td>

Record&lt;string, string \| number \| boolean&gt;

</td><td>

_(Optional)_ 其它参数

</td></tr>
<tr><td>

[primitiveId?](./ISCH_PrimitiveComponent.md)

</td><td>

`protected`

</td><td>

string

</td><td>

_(Optional)_ 图元 ID

</td></tr>
<tr><td>

[rotation](./ISCH_PrimitiveComponent.md)

</td><td>

`protected`

</td><td>

number

</td><td>

旋转角度

</td></tr>
<tr><td>

[x](./ISCH_PrimitiveComponent.md)

</td><td>

`protected`

</td><td>

number

</td><td>

坐标 X

</td></tr>
<tr><td>

[y](./ISCH_PrimitiveComponent.md)

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

[done()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getAllPins()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Get all pins associated with the device

</td></tr>
<tr><td>

[getState\_AddIntoBom()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: whether to add BOM

</td></tr>
<tr><td>

[getState\_AddIntoPcb()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: whether to switch to PCB

</td></tr>
<tr><td>

[getState\_Component()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: associate library device

</td></tr>
<tr><td>

[getState\_ComponentType()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: device type

</td></tr>
<tr><td>

[getState\_Designator()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: designator

</td></tr>
<tr><td>

[getState\_Footprint()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: associate library footprint

</td></tr>
<tr><td>

[getState\_Manufacturer()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: manufacturer

</td></tr>
<tr><td>

[getState\_ManufacturerId()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: manufacturer ID

</td></tr>
<tr><td>

[getState\_Mirror()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: whether it is mirrored

</td></tr>
<tr><td>

[getState\_Name()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: name

</td></tr>
<tr><td>

[getState\_Net()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: net name

</td></tr>
<tr><td>

[getState\_OtherProperty()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: other parameters

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[getState\_Rotation()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: rotation angle

</td></tr>
<tr><td>

[getState\_SubPartName()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: sub-part name

</td></tr>
<tr><td>

[getState\_Supplier()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: supplier

</td></tr>
<tr><td>

[getState\_SupplierId()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: supplier ID

</td></tr>
<tr><td>

[getState\_Symbol()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: associate library symbol

</td></tr>
<tr><td>

[getState\_UniqueId()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: unique ID

</td></tr>
<tr><td>

[getState\_X()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: X coordinate

</td></tr>
<tr><td>

[getState\_Y()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: Y coordinate

</td></tr>
<tr><td>

[isAsync()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_AddIntoBom(addIntoBom)](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether to add BOM

</td></tr>
<tr><td>

[setState\_AddIntoPcb(addIntoPcb)](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether to switch to PCB

</td></tr>
<tr><td>

[setState\_Designator(designator)](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: designator

</td></tr>
<tr><td>

[setState\_Manufacturer(manufacturer)](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: manufacturer

</td></tr>
<tr><td>

[setState\_ManufacturerId(manufacturerId)](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: manufacturer ID

</td></tr>
<tr><td>

[setState\_Mirror(mirror)](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is mirrored

</td></tr>
<tr><td>

[setState\_Name(name)](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: name

</td></tr>
<tr><td>

[setState\_Net(net)](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: net name

</td></tr>
<tr><td>

[setState\_OtherProperty(otherProperty)](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: other parameters

</td></tr>
<tr><td>

[setState\_Rotation(rotation)](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: rotation angle

</td></tr>
<tr><td>

[setState\_Supplier(supplier)](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: supplier

</td></tr>
<tr><td>

[setState\_SupplierId(supplierId)](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: supplier ID

</td></tr>
<tr><td>

[setState\_UniqueId(uniqueId)](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: unique ID

</td></tr>
<tr><td>

[setState\_X(x)](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: X coordinate

</td></tr>
<tr><td>

[setState\_Y(y)](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Y coordinate

</td></tr>
<tr><td>

[toAsync()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./ISCH_PrimitiveComponent.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 属性详情

### async

# ISCH\_PrimitiveComponent.async property

异步

## Signature

```typescript
function async: boolean;
```

### designator

# ISCH\_PrimitiveComponent.designator property

Component 属性：位号

## Signature

```typescript
function designator?: string;
```

### mirror

# ISCH\_PrimitiveComponent.mirror property

是否镜像

## Signature

```typescript
function mirror: boolean;
```

### name

# ISCH\_PrimitiveComponent.name property

Component 属性：名称

## Signature

```typescript
function name?: string;
```

### otherproperty

# ISCH\_PrimitiveComponent.otherProperty property

其它参数

## Signature

```typescript
function otherProperty?: Record<string, string | number | boolean>;
```

### primitiveid

# ISCH\_PrimitiveComponent.primitiveId property

图元 ID

## Signature

```typescript
function primitiveId?: string;
```

### rotation

# ISCH\_PrimitiveComponent.rotation property

旋转角度

## Signature

```typescript
function rotation: number;
```

### x

# ISCH\_PrimitiveComponent.x property

坐标 X

## Signature

```typescript
function x: number;
```

### y

# ISCH\_PrimitiveComponent.y property

坐标 Y

## Signature

```typescript
function y: number;
```


---

## 方法详情

### done

# ISCH\_PrimitiveComponent.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<ISCH_PrimitiveComponent>;
```

## Returns

Promise&lt;[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)<!-- -->&gt;

Device primitive object

### getallpins

# ISCH\_PrimitiveComponent.getAllPins() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all pins associated with the device

## Signature

```typescript
function getAllPins(): Promise<Array<ISCH_PrimitiveComponentPin> | undefined>;
```

## Returns

Promise&lt;Array&lt;[ISCH\_PrimitiveComponentPin](./ISCH_PrimitiveComponentPin.md)<!-- -->&gt; \| undefined&gt;

Device pin primitive array

### getstate_addintobom

# ISCH\_PrimitiveComponent.getState\_AddIntoBom() method

Get the property state: whether to add BOM

## Signature

```typescript
function getState_AddIntoBom(): boolean | undefined;
```

## Returns

boolean \| undefined

Whether Add to BOM

### getstate_addintopcb

# ISCH\_PrimitiveComponent.getState\_AddIntoPcb() method

Get the property state: whether to switch to PCB

## Signature

```typescript
function getState_AddIntoPcb(): boolean | undefined;
```

## Returns

boolean \| undefined

Whether Transfer to PCB

### getstate_component

# ISCH\_PrimitiveComponent.getState\_Component() method

Get the property state: associate library device

## Signature

```typescript
function getState_Component(): { libraryUuid: string; uuid: string; name?: string } | undefined;
```

## Returns

{ libraryUuid: string; uuid: string; name?: string } \| undefined

Associate library device

### getstate_componenttype

# ISCH\_PrimitiveComponent.getState\_ComponentType() method

Get the property state: device type

## Signature

```typescript
function getState_ComponentType(): ESCH_PrimitiveComponentType;
```

## Returns

[ESCH\_PrimitiveComponentType](../enums/ESCH_PrimitiveComponentType.md)

Device type

### getstate_designator

# ISCH\_PrimitiveComponent.getState\_Designator() method

Get the property state: designator

## Signature

```typescript
function getState_Designator(): string | undefined;
```

## Returns

string \| undefined

Designator

### getstate_footprint

# ISCH\_PrimitiveComponent.getState\_Footprint() method

Get the property state: associate library footprint

## Signature

```typescript
function getState_Footprint(): { libraryUuid: string; uuid: string; name?: string } | undefined;
```

## Returns

{ libraryUuid: string; uuid: string; name?: string } \| undefined

Associate library footprint

### getstate_manufacturer

# ISCH\_PrimitiveComponent.getState\_Manufacturer() method

Get the property state: manufacturer

## Signature

```typescript
function getState_Manufacturer(): string | undefined;
```

## Returns

string \| undefined

Manufacturer

### getstate_manufacturerid

# ISCH\_PrimitiveComponent.getState\_ManufacturerId() method

Get the property state: manufacturer ID

## Signature

```typescript
function getState_ManufacturerId(): string | undefined;
```

## Returns

string \| undefined

Manufacturer ID

### getstate_mirror

# ISCH\_PrimitiveComponent.getState\_Mirror() method

Get the property state: whether it is mirrored

## Signature

```typescript
function getState_Mirror(): boolean;
```

## Returns

boolean

Whether it is mirrored

### getstate_name

# ISCH\_PrimitiveComponent.getState\_Name() method

Get the property state: name

## Signature

```typescript
function getState_Name(): string | undefined;
```

## Returns

string \| undefined

Name

### getstate_net

# ISCH\_PrimitiveComponent.getState\_Net() method

Get the property state: net name

## Signature

```typescript
function getState_Net(): string | undefined;
```

## Returns

string \| undefined

Net name

### getstate_otherproperty

# ISCH\_PrimitiveComponent.getState\_OtherProperty() method

Get the property state: other parameters

## Signature

```typescript
function getState_OtherProperty(): Record<string, string | number | boolean> | undefined;
```

## Returns

Record&lt;string, string \| number \| boolean&gt; \| undefined

Other parameters

### getstate_primitiveid

# ISCH\_PrimitiveComponent.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivetype

# ISCH\_PrimitiveComponent.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): ESCH_PrimitiveType;
```

## Returns

[ESCH\_PrimitiveType](../enums/ESCH_PrimitiveType.md)

Primitive type

### getstate_rotation

# ISCH\_PrimitiveComponent.getState\_Rotation() method

Get the property state: rotation angle

## Signature

```typescript
function getState_Rotation(): number;
```

## Returns

number

Rotation angle

### getstate_subpartname

# ISCH\_PrimitiveComponent.getState\_SubPartName() method

Get the property state: sub-part name

## Signature

```typescript
function getState_SubPartName(): string | undefined;
```

## Returns

string \| undefined

Sub-part name

### getstate_supplier

# ISCH\_PrimitiveComponent.getState\_Supplier() method

Get the property state: supplier

## Signature

```typescript
function getState_Supplier(): string | undefined;
```

## Returns

string \| undefined

Supplier

### getstate_supplierid

# ISCH\_PrimitiveComponent.getState\_SupplierId() method

Get the property state: supplier ID

## Signature

```typescript
function getState_SupplierId(): string | undefined;
```

## Returns

string \| undefined

Supplier ID

### getstate_symbol

# ISCH\_PrimitiveComponent.getState\_Symbol() method

Get the property state: associate library symbol

## Signature

```typescript
function getState_Symbol(): { libraryUuid: string; uuid: string; name?: string } | undefined;
```

## Returns

{ libraryUuid: string; uuid: string; name?: string } \| undefined

Associate library symbol

### getstate_uniqueid

# ISCH\_PrimitiveComponent.getState\_UniqueId() method

Get the property state: unique ID

## Signature

```typescript
function getState_UniqueId(): string | undefined;
```

## Returns

string \| undefined

Unique ID

### getstate_x

# ISCH\_PrimitiveComponent.getState\_X() method

Get the property state: X coordinate

## Signature

```typescript
function getState_X(): number;
```

## Returns

number

X coordinate

### getstate_y

# ISCH\_PrimitiveComponent.getState\_Y() method

Get the property state: Y coordinate

## Signature

```typescript
function getState_Y(): number;
```

## Returns

number

Y coordinate

### isasync

# ISCH\_PrimitiveComponent.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# ISCH\_PrimitiveComponent.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<ISCH_PrimitiveComponent>;
```

## Returns

Promise&lt;[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)<!-- -->&gt;

Device primitive object

### setstate_addintobom

# ISCH\_PrimitiveComponent.setState\_AddIntoBom() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether to add BOM

## Signature

```typescript
function setState_AddIntoBom(addIntoBom: boolean | undefined): ISCH_PrimitiveComponent;
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

addIntoBom

</td><td>

boolean \| undefined

</td><td>

Whether Add to BOM

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Device primitive object

### setstate_addintopcb

# ISCH\_PrimitiveComponent.setState\_AddIntoPcb() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether to switch to PCB

## Signature

```typescript
function setState_AddIntoPcb(addIntoPcb: boolean | undefined): ISCH_PrimitiveComponent;
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

addIntoPcb

</td><td>

boolean \| undefined

</td><td>

Whether Transfer to PCB

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Device primitive object

### setstate_designator

# ISCH\_PrimitiveComponent.setState\_Designator() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: designator

## Signature

```typescript
function setState_Designator(designator: string | undefined): ISCH_PrimitiveComponent;
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

designator

</td><td>

string \| undefined

</td><td>

Designator

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Device primitive object

### setstate_manufacturer

# ISCH\_PrimitiveComponent.setState\_Manufacturer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: manufacturer

## Signature

```typescript
function setState_Manufacturer(manufacturer: string | undefined): ISCH_PrimitiveComponent;
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

manufacturer

</td><td>

string \| undefined

</td><td>

Manufacturer

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Device primitive object

### setstate_manufacturerid

# ISCH\_PrimitiveComponent.setState\_ManufacturerId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: manufacturer ID

## Signature

```typescript
function setState_ManufacturerId(manufacturerId: string | undefined): ISCH_PrimitiveComponent;
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

manufacturerId

</td><td>

string \| undefined

</td><td>

Manufacturer ID

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Device primitive object

### setstate_mirror

# ISCH\_PrimitiveComponent.setState\_Mirror() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is mirrored

## Signature

```typescript
function setState_Mirror(mirror: boolean): ISCH_PrimitiveComponent;
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

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Device primitive object

### setstate_name

# ISCH\_PrimitiveComponent.setState\_Name() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: name

## Signature

```typescript
function setState_Name(name: string | undefined): ISCH_PrimitiveComponent;
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

name

</td><td>

string \| undefined

</td><td>

Name

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Device primitive object

### setstate_net

# ISCH\_PrimitiveComponent.setState\_Net() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: net name

## Signature

```typescript
function setState_Net(net: string | undefined): ISCH_PrimitiveComponent;
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

string \| undefined

</td><td>

Net name

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Device primitive object

### setstate_otherproperty

# ISCH\_PrimitiveComponent.setState\_OtherProperty() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: other parameters

## Signature

```typescript
function setState_OtherProperty(
	otherProperty: Record<string, string | number | boolean>,
): ISCH_PrimitiveComponent;
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

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Device primitive object

### setstate_rotation

# ISCH\_PrimitiveComponent.setState\_Rotation() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: rotation angle

## Signature

```typescript
function setState_Rotation(rotation: number): ISCH_PrimitiveComponent;
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

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Device primitive object

### setstate_supplier

# ISCH\_PrimitiveComponent.setState\_Supplier() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: supplier

## Signature

```typescript
function setState_Supplier(supplier: string | undefined): ISCH_PrimitiveComponent;
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

supplier

</td><td>

string \| undefined

</td><td>

Supplier

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Device primitive object

### setstate_supplierid

# ISCH\_PrimitiveComponent.setState\_SupplierId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: supplier ID

## Signature

```typescript
function setState_SupplierId(supplierId: string | undefined): ISCH_PrimitiveComponent;
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

supplierId

</td><td>

string \| undefined

</td><td>

Supplier ID

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Device primitive object

### setstate_uniqueid

# ISCH\_PrimitiveComponent.setState\_UniqueId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: unique ID

## Signature

```typescript
function setState_UniqueId(uniqueId: string | undefined): ISCH_PrimitiveComponent;
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

uniqueId

</td><td>

string \| undefined

</td><td>

Unique ID

</td></tr>
</tbody></table>

## Returns

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Device primitive object

### setstate_x

# ISCH\_PrimitiveComponent.setState\_X() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: X coordinate

## Signature

```typescript
function setState_X(x: number): ISCH_PrimitiveComponent;
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

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Device primitive object

### setstate_y

# ISCH\_PrimitiveComponent.setState\_Y() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Y coordinate

## Signature

```typescript
function setState_Y(y: number): ISCH_PrimitiveComponent;
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

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Device primitive object

### toasync

# ISCH\_PrimitiveComponent.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): ISCH_PrimitiveComponent;
```

## Returns

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Arc line primitive object

### tosync

# ISCH\_PrimitiveComponent.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): ISCH_PrimitiveComponent;
```

## Returns

[ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

Arc line primitive object

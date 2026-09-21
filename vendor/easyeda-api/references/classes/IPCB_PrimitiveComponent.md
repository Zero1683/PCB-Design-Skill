# IPCB\_PrimitiveComponent class

Device primitive

## Signature

```typescript
class IPCB_PrimitiveComponent implements IPCB_Primitive
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

[done()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getAllPins()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Get all pads associated with the device

</td></tr>
<tr><td>

[getState\_AddIntoBom()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: whether to add BOM

</td></tr>
<tr><td>

[getState\_Component()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: associate library device

</td></tr>
<tr><td>

[getState\_Designator()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: designator

</td></tr>
<tr><td>

[getState\_Footprint()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: associate library footprint

</td></tr>
<tr><td>

[getState\_Layer()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: Layer

</td></tr>
<tr><td>

[getState\_Manufacturer()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: manufacturer

</td></tr>
<tr><td>

[getState\_ManufacturerId()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: manufacturer ID

</td></tr>
<tr><td>

[getState\_Model3D()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: associate library 3D model

</td></tr>
<tr><td>

[getState\_Name()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: name

</td></tr>
<tr><td>

[getState\_OtherProperty()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: other parameters

</td></tr>
<tr><td>

[getState\_Pads()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: pad

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveLock()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: whether it is locked

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[getState\_Rotation()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: rotation angle

</td></tr>
<tr><td>

[getState\_Supplier()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: supplier

</td></tr>
<tr><td>

[getState\_SupplierId()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: supplier ID

</td></tr>
<tr><td>

[getState\_UniqueId()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: unique ID

</td></tr>
<tr><td>

[getState\_X()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: X coordinate

</td></tr>
<tr><td>

[getState\_Y()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Get the property state: Y coordinate

</td></tr>
<tr><td>

[isAsync()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setAttribute(key, value, keyVisible, valueVisible)](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set Property

</td></tr>
<tr><td>

[setState\_AddIntoBom(addIntoBom)](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether to add BOM

</td></tr>
<tr><td>

[setState\_Designator(designator)](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: designator

</td></tr>
<tr><td>

[setState\_Layer(layer)](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Layer

</td></tr>
<tr><td>

[setState\_Manufacturer(manufacturer)](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: manufacturer

</td></tr>
<tr><td>

[setState\_ManufacturerId(manufacturerId)](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: manufacturer ID

</td></tr>
<tr><td>

[setState\_Name(name)](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: name

</td></tr>
<tr><td>

[setState\_OtherProperty(otherProperty)](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: other parameters

</td></tr>
<tr><td>

[setState\_PrimitiveLock(primitiveLock)](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is locked

</td></tr>
<tr><td>

[setState\_Rotation(rotation)](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: rotation angle

</td></tr>
<tr><td>

[setState\_Supplier(supplier)](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: supplier

</td></tr>
<tr><td>

[setState\_SupplierId(supplierId)](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: supplier ID

</td></tr>
<tr><td>

[setState\_UniqueId(uniqueId)](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: unique ID

</td></tr>
<tr><td>

[setState\_X(x)](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: X coordinate

</td></tr>
<tr><td>

[setState\_Y(y)](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Y coordinate

</td></tr>
<tr><td>

[toAsync()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./IPCB_PrimitiveComponent.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 方法详情

### done

# IPCB\_PrimitiveComponent.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<IPCB_PrimitiveComponent>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)<!-- -->&gt;

Device primitive object

### getallpins

# IPCB\_PrimitiveComponent.getAllPins() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all pads associated with the device

## Signature

```typescript
function getAllPins(): Promise<Array<IPCB_PrimitiveComponentPad>>;
```

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveComponentPad](./IPCB_PrimitiveComponentPad.md)<!-- -->&gt;&gt;

Device pad primitive array

### getstate_addintobom

# IPCB\_PrimitiveComponent.getState\_AddIntoBom() method

Get the property state: whether to add BOM

## Signature

```typescript
function getState_AddIntoBom(): boolean;
```

## Returns

boolean

Whether Add to BOM

### getstate_component

# IPCB\_PrimitiveComponent.getState\_Component() method

Get the property state: associate library device

## Signature

```typescript
function getState_Component(): { libraryUuid: string; uuid: string; name?: string } | undefined;
```

## Returns

{ libraryUuid: string; uuid: string; name?: string } \| undefined

Associate library device

### getstate_designator

# IPCB\_PrimitiveComponent.getState\_Designator() method

Get the property state: designator

## Signature

```typescript
function getState_Designator(): string | undefined;
```

## Returns

string \| undefined

Designator

### getstate_footprint

# IPCB\_PrimitiveComponent.getState\_Footprint() method

Get the property state: associate library footprint

## Signature

```typescript
function getState_Footprint(): { libraryUuid: string; uuid: string; name?: string } | undefined;
```

## Returns

{ libraryUuid: string; uuid: string; name?: string } \| undefined

Associate library footprint

### getstate_layer

# IPCB\_PrimitiveComponent.getState\_Layer() method

Get the property state: Layer

## Signature

```typescript
function getState_Layer(): TPCB_LayersOfComponent;
```

## Returns

[TPCB\_LayersOfComponent](../types/TPCB_LayersOfComponent.md)

Layer

### getstate_manufacturer

# IPCB\_PrimitiveComponent.getState\_Manufacturer() method

Get the property state: manufacturer

## Signature

```typescript
function getState_Manufacturer(): string | undefined;
```

## Returns

string \| undefined

Manufacturer

### getstate_manufacturerid

# IPCB\_PrimitiveComponent.getState\_ManufacturerId() method

Get the property state: manufacturer ID

## Signature

```typescript
function getState_ManufacturerId(): string | undefined;
```

## Returns

string \| undefined

Manufacturer ID

### getstate_model3d

# IPCB\_PrimitiveComponent.getState\_Model3D() method

Get the property state: associate library 3D model

## Signature

```typescript
function getState_Model3D(): { libraryUuid: string; uuid: string; name?: string } | undefined;
```

## Returns

{ libraryUuid: string; uuid: string; name?: string } \| undefined

Associate library 3D model

### getstate_name

# IPCB\_PrimitiveComponent.getState\_Name() method

Get the property state: name

## Signature

```typescript
function getState_Name(): string | undefined;
```

## Returns

string \| undefined

Name

### getstate_otherproperty

# IPCB\_PrimitiveComponent.getState\_OtherProperty() method

Get the property state: other parameters

## Signature

```typescript
function getState_OtherProperty(): { [key: string]: string | number | boolean } | undefined;
```

## Returns

{ \[key: string\]: string \| number \| boolean } \| undefined

Other parameters

### getstate_pads

# IPCB\_PrimitiveComponent.getState\_Pads() method

Get the property state: pad

## Signature

```typescript
function getState_Pads():
	Array<{ primitiveId: string; net: string; padNumber: string }> | undefined;
```

## Returns

Array&lt;{ primitiveId: string; net: string; padNumber: string }&gt; \| undefined

Pad

### getstate_primitiveid

# IPCB\_PrimitiveComponent.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivelock

# IPCB\_PrimitiveComponent.getState\_PrimitiveLock() method

Get the property state: whether it is locked

## Signature

```typescript
function getState_PrimitiveLock(): boolean;
```

## Returns

boolean

Whether it is locked

### getstate_primitivetype

# IPCB\_PrimitiveComponent.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): EPCB_PrimitiveType;
```

## Returns

[EPCB\_PrimitiveType](../enums/EPCB_PrimitiveType.md)

Primitive type

### getstate_rotation

# IPCB\_PrimitiveComponent.getState\_Rotation() method

Get the property state: rotation angle

## Signature

```typescript
function getState_Rotation(): number;
```

## Returns

number

Rotation angle

### getstate_supplier

# IPCB\_PrimitiveComponent.getState\_Supplier() method

Get the property state: supplier

## Signature

```typescript
function getState_Supplier(): string | undefined;
```

## Returns

string \| undefined

Supplier

### getstate_supplierid

# IPCB\_PrimitiveComponent.getState\_SupplierId() method

Get the property state: supplier ID

## Signature

```typescript
function getState_SupplierId(): string | undefined;
```

## Returns

string \| undefined

Supplier ID

### getstate_uniqueid

# IPCB\_PrimitiveComponent.getState\_UniqueId() method

Get the property state: unique ID

## Signature

```typescript
function getState_UniqueId(): string | undefined;
```

## Returns

string \| undefined

Unique ID

### getstate_x

# IPCB\_PrimitiveComponent.getState\_X() method

Get the property state: X coordinate

## Signature

```typescript
function getState_X(): number;
```

## Returns

number

X coordinate

### getstate_y

# IPCB\_PrimitiveComponent.getState\_Y() method

Get the property state: Y coordinate

## Signature

```typescript
function getState_Y(): number;
```

## Returns

number

Y coordinate

### isasync

# IPCB\_PrimitiveComponent.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# IPCB\_PrimitiveComponent.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<IPCB_PrimitiveComponent>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)<!-- -->&gt;

Device primitive object

### setattribute

# IPCB\_PrimitiveComponent.setAttribute() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set Property

## Signature

```typescript
function setAttribute(
	key: string,
	value?: string | number | boolean,
	keyVisible?: boolean,
	valueVisible?: boolean,
): Promise<IPCB_PrimitiveAttribute>;
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

key

</td><td>

string

</td><td>

Attribute name. If the device does not have an attribute with this name, the attribute will be added

</td></tr>
<tr><td>

value

</td><td>

string \| number \| boolean

</td><td>

_(Optional)_ Property value

</td></tr>
<tr><td>

keyVisible

</td><td>

boolean

</td><td>

_(Optional)_ Attribute name visibility

</td></tr>
<tr><td>

valueVisible

</td><td>

boolean

</td><td>

_(Optional)_ Attribute value visibility

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveAttribute](./IPCB_PrimitiveAttribute.md)<!-- -->&gt;

Attribute primitive object

### setstate_addintobom

# IPCB\_PrimitiveComponent.setState\_AddIntoBom() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether to add BOM

## Signature

```typescript
function setState_AddIntoBom(addIntoBom: boolean): IPCB_PrimitiveComponent;
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

boolean

</td><td>

Whether Add to BOM

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)

Device primitive object

### setstate_designator

# IPCB\_PrimitiveComponent.setState\_Designator() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: designator

## Signature

```typescript
function setState_Designator(designator: string | undefined): IPCB_PrimitiveComponent;
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

[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)

Device primitive object

### setstate_layer

# IPCB\_PrimitiveComponent.setState\_Layer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Layer

## Signature

```typescript
function setState_Layer(layer: TPCB_LayersOfComponent): IPCB_PrimitiveComponent;
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

[TPCB\_LayersOfComponent](../types/TPCB_LayersOfComponent.md)

</td><td>

Layer

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)

Device primitive object

### setstate_manufacturer

# IPCB\_PrimitiveComponent.setState\_Manufacturer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: manufacturer

## Signature

```typescript
function setState_Manufacturer(manufacturer: string | undefined): IPCB_PrimitiveComponent;
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

[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)

Device primitive object

### setstate_manufacturerid

# IPCB\_PrimitiveComponent.setState\_ManufacturerId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: manufacturer ID

## Signature

```typescript
function setState_ManufacturerId(manufacturerId: string | undefined): IPCB_PrimitiveComponent;
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

[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)

Device primitive object

### setstate_name

# IPCB\_PrimitiveComponent.setState\_Name() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: name

## Signature

```typescript
function setState_Name(name: string | undefined): IPCB_PrimitiveComponent;
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

[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)

Device primitive object

### setstate_otherproperty

# IPCB\_PrimitiveComponent.setState\_OtherProperty() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: other parameters

## Signature

```typescript
function setState_OtherProperty(otherProperty: {
	[key: string]: string | number | boolean;
}): IPCB_PrimitiveComponent;
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

\{ \[key: string\]: string \| number \| boolean \}

</td><td>

Other parameters

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)

Device primitive object

### setstate_primitivelock

# IPCB\_PrimitiveComponent.setState\_PrimitiveLock() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is locked

## Signature

```typescript
function setState_PrimitiveLock(primitiveLock: boolean): IPCB_PrimitiveComponent;
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

[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)

Device primitive object

### setstate_rotation

# IPCB\_PrimitiveComponent.setState\_Rotation() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: rotation angle

## Signature

```typescript
function setState_Rotation(rotation: number): IPCB_PrimitiveComponent;
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

[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)

Device primitive object

### setstate_supplier

# IPCB\_PrimitiveComponent.setState\_Supplier() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: supplier

## Signature

```typescript
function setState_Supplier(supplier: string | undefined): IPCB_PrimitiveComponent;
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

[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)

Device primitive object

### setstate_supplierid

# IPCB\_PrimitiveComponent.setState\_SupplierId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: supplier ID

## Signature

```typescript
function setState_SupplierId(supplierId: string | undefined): IPCB_PrimitiveComponent;
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

[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)

Device primitive object

### setstate_uniqueid

# IPCB\_PrimitiveComponent.setState\_UniqueId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: unique ID

## Signature

```typescript
function setState_UniqueId(uniqueId: string | undefined): IPCB_PrimitiveComponent;
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

[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)

Device primitive object

### setstate_x

# IPCB\_PrimitiveComponent.setState\_X() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: X coordinate

## Signature

```typescript
function setState_X(x: number): IPCB_PrimitiveComponent;
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

[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)

Device primitive object

### setstate_y

# IPCB\_PrimitiveComponent.setState\_Y() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Y coordinate

## Signature

```typescript
function setState_Y(y: number): IPCB_PrimitiveComponent;
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

[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)

Device primitive object

### toasync

# IPCB\_PrimitiveComponent.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): IPCB_PrimitiveComponent;
```

## Returns

[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)

Device primitive object

### tosync

# IPCB\_PrimitiveComponent.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): IPCB_PrimitiveComponent;
```

## Returns

[IPCB\_PrimitiveComponent](./IPCB_PrimitiveComponent.md)

Device primitive object

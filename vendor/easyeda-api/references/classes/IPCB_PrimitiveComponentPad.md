# IPCB\_PrimitiveComponentPad class

Device pad primitive

## Signature

```typescript
class IPCB_PrimitiveComponentPad extends IPCB_PrimitivePad
```
**Extends:** [IPCB\_PrimitivePad](./IPCB_PrimitivePad.md)

## Remarks

A device pad primitive is a special primitive. It refers to the pad associated with a footprint on the PCB canvas

You can only obtain a device pad primitive through [the getAllPinsByPrimitiveId method of the device class](./PCB_PrimitiveComponent.md) or [the getAllPads method of the device primitive](./IPCB_PrimitiveComponent.md)

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

[primitiveType](./IPCB_PrimitiveComponentPad.md)

</td><td>

`protected`

`readonly`

</td><td>

[EPCB\_PrimitiveType.COMPONENT\_PAD](../enums/EPCB_PrimitiveType.md)

</td><td>

图元类型

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

[done()](./IPCB_PrimitiveComponentPad.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getConnectedPrimitives(onlyCentreConnection)](./IPCB_PrimitiveComponentPad.md)

</td><td>

</td><td>

**_(BETA)_** Get connected primitives

</td></tr>
<tr><td>

[getConnectedPrimitives(onlyCentreConnection)](./IPCB_PrimitiveComponentPad.md)

</td><td>

</td><td>

</td></tr>
<tr><td>

[getState\_ParentComponentPrimitiveId()](./IPCB_PrimitiveComponentPad.md)

</td><td>

</td><td>

Get the property state: parent device primitive ID

</td></tr>
<tr><td>

[setState\_ParentComponentPrimitiveId()](./IPCB_PrimitiveComponentPad.md)

</td><td>

</td><td>

Set the property state: parent device primitive ID

</td></tr>
</tbody></table>

---

## 属性详情

### primitivetype

# IPCB\_PrimitiveComponentPad.primitiveType property

图元类型

## Signature

```typescript
function readonly primitiveType: EPCB_PrimitiveType.COMPONENT_PAD;
```


---

## 方法详情

### done

# IPCB\_PrimitiveComponentPad.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<IPCB_PrimitiveComponentPad>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveComponentPad](./IPCB_PrimitiveComponentPad.md)<!-- -->&gt;

Device pad primitive object

### getconnectedprimitives

# IPCB\_PrimitiveComponentPad.getConnectedPrimitives() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get connected primitives

## Signature

```typescript
function getConnectedPrimitives(
	onlyCentreConnection: true,
): Promise<Array<IPCB_PrimitiveLine | IPCB_PrimitiveArc | IPCB_PrimitiveVia>>;
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

onlyCentreConnection

</td><td>

true

</td><td>

Whether to only use center connection. If it is `true`<!-- -->, only center-connected primitives (lines, arc lines, vias) are obtained; if it is `false`<!-- -->, all contacting primitives are obtained

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveLine](./IPCB_PrimitiveLine.md) \| [IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md) \| [IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md)<!-- -->&gt;&gt;

## Remarks

This API can get the primitives that are in direct contact with the pad

### getconnectedprimitives_1

# IPCB\_PrimitiveComponentPad.getConnectedPrimitives() method

## Signature

```typescript
function getConnectedPrimitives(
	onlyCentreConnection: false,
): Promise<
	Array<
		| IPCB_PrimitiveLine
		| IPCB_PrimitiveArc
		| IPCB_PrimitiveVia
		| IPCB_PrimitivePolyline
		| IPCB_PrimitiveFill
	>
>;
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

onlyCentreConnection

</td><td>

false

</td><td>

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveLine](./IPCB_PrimitiveLine.md) \| [IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md) \| [IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md) \| [IPCB\_PrimitivePolyline](./IPCB_PrimitivePolyline.md) \| [IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md)<!-- -->&gt;&gt;

### getstate_parentcomponentprimitiveid

# IPCB\_PrimitiveComponentPad.getState\_ParentComponentPrimitiveId() method

Get the property state: parent device primitive ID

## Signature

```typescript
function getState_ParentComponentPrimitiveId(): string;
```

## Returns

string

Parent device primitive ID

### setstate_parentcomponentprimitiveid

# IPCB\_PrimitiveComponentPad.setState\_ParentComponentPrimitiveId() method

Set the property state: parent device primitive ID

## Signature

```typescript
function setState_ParentComponentPrimitiveId(): IPCB_PrimitiveComponentPad;
```

## Returns

[IPCB\_PrimitiveComponentPad](./IPCB_PrimitiveComponentPad.md)

Device pad primitive object

## Remarks

The properties of this device pad primitive do not support modification. Calling this API will have no effect

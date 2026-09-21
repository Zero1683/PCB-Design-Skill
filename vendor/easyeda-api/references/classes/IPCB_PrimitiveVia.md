# IPCB\_PrimitiveVia class

Via primitive

## Signature

```typescript
class IPCB_PrimitiveVia implements IPCB_Primitive
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

[done()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getAdjacentPrimitives()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

**_(BETA)_** Get Adjacent primitive objects

</td></tr>
<tr><td>

[getState\_DesignRuleBlindViaName()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

Get the property state: blind/buried via design rule item name

</td></tr>
<tr><td>

[getState\_Diameter()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

Get the property state: outer diameter

</td></tr>
<tr><td>

[getState\_HoleDiameter()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

Get the property state: hole diameter

</td></tr>
<tr><td>

[getState\_Net()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

Get the property state: net name

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveLock()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

Get the property state: whether it is locked

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[getState\_SolderMaskExpansion()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

Get the property state: solder mask / paste mask expansion

</td></tr>
<tr><td>

[getState\_ViaType()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

Get the property state: via type

</td></tr>
<tr><td>

[getState\_X()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

Get the property state: X coordinate

</td></tr>
<tr><td>

[getState\_Y()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

Get the property state: Y coordinate

</td></tr>
<tr><td>

[isAsync()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

Query whether the primitive is an async primitive

</td></tr>
<tr><td>

[reset()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
<tr><td>

[setState\_DesignRuleBlindViaName(designRuleBlindViaName)](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: blind/buried via design rule item name

</td></tr>
<tr><td>

[setState\_Diameter(diameter)](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: outer diameter

</td></tr>
<tr><td>

[setState\_HoleDiameter(holeDiameter)](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: hole diameter

</td></tr>
<tr><td>

[setState\_Net(net)](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: net name

</td></tr>
<tr><td>

[setState\_PrimitiveLock(primitiveLock)](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: whether it is locked

</td></tr>
<tr><td>

[setState\_SolderMaskExpansion(solderMaskExpansion)](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: solder mask / paste mask expansion

</td></tr>
<tr><td>

[setState\_ViaType(viaType)](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: via type

</td></tr>
<tr><td>

[setState\_X(x)](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: X coordinate

</td></tr>
<tr><td>

[setState\_Y(y)](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

**_(BETA)_** Set the property state: Y coordinate

</td></tr>
<tr><td>

[toAsync()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

Convert Primitive to Async primitive

</td></tr>
<tr><td>

[toSync()](./IPCB_PrimitiveVia.md)

</td><td>

</td><td>

Convert Primitive to Sync primitive

</td></tr>
</tbody></table>

---

## 方法详情

### done

# IPCB\_PrimitiveVia.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<IPCB_PrimitiveVia>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md)<!-- -->&gt;

Via primitive object

### getadjacentprimitives

# IPCB\_PrimitiveVia.getAdjacentPrimitives() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Adjacent primitive objects

## Signature

```typescript
function getAdjacentPrimitives(): Promise<Array<IPCB_PrimitiveLine | IPCB_PrimitiveArc>>;
```

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveLine](./IPCB_PrimitiveLine.md) \| [IPCB\_PrimitiveArc](./IPCB_PrimitiveArc.md)<!-- -->&gt;&gt;

Adjacent wire and arc-line primitive objects

## Remarks

It will get the wire and arc-line primitive objects directly connected to the via

### getstate_designruleblindvianame

# IPCB\_PrimitiveVia.getState\_DesignRuleBlindViaName() method

Get the property state: blind/buried via design rule item name

## Signature

```typescript
function getState_DesignRuleBlindViaName(): string | null;
```

## Returns

string \| null

Blind/buried via design rule item name

### getstate_diameter

# IPCB\_PrimitiveVia.getState\_Diameter() method

Get the property state: outer diameter

## Signature

```typescript
function getState_Diameter(): number;
```

## Returns

number

Outer diameter

### getstate_holediameter

# IPCB\_PrimitiveVia.getState\_HoleDiameter() method

Get the property state: hole diameter

## Signature

```typescript
function getState_HoleDiameter(): number;
```

## Returns

number

Hole diameter

### getstate_net

# IPCB\_PrimitiveVia.getState\_Net() method

Get the property state: net name

## Signature

```typescript
function getState_Net(): string;
```

## Returns

string

Net name

### getstate_primitiveid

# IPCB\_PrimitiveVia.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivelock

# IPCB\_PrimitiveVia.getState\_PrimitiveLock() method

Get the property state: whether it is locked

## Signature

```typescript
function getState_PrimitiveLock(): boolean;
```

## Returns

boolean

Whether it is locked

### getstate_primitivetype

# IPCB\_PrimitiveVia.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): EPCB_PrimitiveType;
```

## Returns

[EPCB\_PrimitiveType](../enums/EPCB_PrimitiveType.md)

Primitive type

### getstate_soldermaskexpansion

# IPCB\_PrimitiveVia.getState\_SolderMaskExpansion() method

Get the property state: solder mask / paste mask expansion

## Signature

```typescript
function getState_SolderMaskExpansion(): IPCB_PrimitiveSolderMaskAndPasteMaskExpansion | null;
```

## Returns

[IPCB\_PrimitiveSolderMaskAndPasteMaskExpansion](../interfaces/IPCB_PrimitiveSolderMaskAndPasteMaskExpansion.md) \| null

Solder mask / paste mask expansion

### getstate_viatype

# IPCB\_PrimitiveVia.getState\_ViaType() method

Get the property state: via type

## Signature

```typescript
function getState_ViaType(): EPCB_PrimitiveViaType;
```

## Returns

[EPCB\_PrimitiveViaType](../enums/EPCB_PrimitiveViaType.md)

Via type

### getstate_x

# IPCB\_PrimitiveVia.getState\_X() method

Get the property state: X coordinate

## Signature

```typescript
function getState_X(): number;
```

## Returns

number

X coordinate

### getstate_y

# IPCB\_PrimitiveVia.getState\_Y() method

Get the property state: Y coordinate

## Signature

```typescript
function getState_Y(): number;
```

## Returns

number

Y coordinate

### isasync

# IPCB\_PrimitiveVia.isAsync() method

Query whether the primitive is an async primitive

## Signature

```typescript
function isAsync(): boolean;
```

## Returns

boolean

Whether Is async primitive

### reset

# IPCB\_PrimitiveVia.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<IPCB_PrimitiveVia>;
```

## Returns

Promise&lt;[IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md)<!-- -->&gt;

Via primitive object

### setstate_designruleblindvianame

# IPCB\_PrimitiveVia.setState\_DesignRuleBlindViaName() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: blind/buried via design rule item name

## Signature

```typescript
function setState_DesignRuleBlindViaName(designRuleBlindViaName: string | null): IPCB_PrimitiveVia;
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

designRuleBlindViaName

</td><td>

string \| null

</td><td>

Blind/buried via design rule item name

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md)

Via primitive object

### setstate_diameter

# IPCB\_PrimitiveVia.setState\_Diameter() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: outer diameter

## Signature

```typescript
function setState_Diameter(diameter: number): IPCB_PrimitiveVia;
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

diameter

</td><td>

number

</td><td>

Outer diameter

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md)

Via primitive object

### setstate_holediameter

# IPCB\_PrimitiveVia.setState\_HoleDiameter() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: hole diameter

## Signature

```typescript
function setState_HoleDiameter(holeDiameter: number): IPCB_PrimitiveVia;
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

holeDiameter

</td><td>

number

</td><td>

Hole diameter

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md)

Via primitive object

### setstate_net

# IPCB\_PrimitiveVia.setState\_Net() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: net name

## Signature

```typescript
function setState_Net(net: string): IPCB_PrimitiveVia;
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

[IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md)

Via primitive object

### setstate_primitivelock

# IPCB\_PrimitiveVia.setState\_PrimitiveLock() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: whether it is locked

## Signature

```typescript
function setState_PrimitiveLock(primitiveLock: boolean): IPCB_PrimitiveVia;
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

[IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md)

Via primitive object

### setstate_soldermaskexpansion

# IPCB\_PrimitiveVia.setState\_SolderMaskExpansion() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: solder mask / paste mask expansion

## Signature

```typescript
function setState_SolderMaskExpansion(
	solderMaskExpansion: IPCB_PrimitiveSolderMaskAndPasteMaskExpansion | null,
): IPCB_PrimitiveVia;
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

solderMaskExpansion

</td><td>

[IPCB\_PrimitiveSolderMaskAndPasteMaskExpansion](../interfaces/IPCB_PrimitiveSolderMaskAndPasteMaskExpansion.md) \| null

</td><td>

Solder mask / paste mask expansion

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md)

Via primitive object

### setstate_viatype

# IPCB\_PrimitiveVia.setState\_ViaType() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: via type

## Signature

```typescript
function setState_ViaType(viaType: EPCB_PrimitiveViaType): IPCB_PrimitiveVia;
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

viaType

</td><td>

[EPCB\_PrimitiveViaType](../enums/EPCB_PrimitiveViaType.md)

</td><td>

Via type

</td></tr>
</tbody></table>

## Returns

[IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md)

Via primitive object

### setstate_x

# IPCB\_PrimitiveVia.setState\_X() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: X coordinate

## Signature

```typescript
function setState_X(x: number): IPCB_PrimitiveVia;
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

[IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md)

Via primitive object

### setstate_y

# IPCB\_PrimitiveVia.setState\_Y() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the property state: Y coordinate

## Signature

```typescript
function setState_Y(y: number): IPCB_PrimitiveVia;
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

[IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md)

Via primitive object

### toasync

# IPCB\_PrimitiveVia.toAsync() method

Convert Primitive to Async primitive

## Signature

```typescript
function toAsync(): IPCB_PrimitiveVia;
```

## Returns

[IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md)

Via primitive object

### tosync

# IPCB\_PrimitiveVia.toSync() method

Convert Primitive to Sync primitive

## Signature

```typescript
function toSync(): IPCB_PrimitiveVia;
```

## Returns

[IPCB\_PrimitiveVia](./IPCB_PrimitiveVia.md)

Via primitive object

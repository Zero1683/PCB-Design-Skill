# IPCB\_PrimitivePoured class

Copper fill primitive

## Signature

```typescript
class IPCB_PrimitivePoured implements IPCB_Primitive
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

[addSolderMaskFill(pourFillId)](./IPCB_PrimitivePoured.md)

</td><td>

</td><td>

**_(BETA)_** Add: solder mask region

</td></tr>
<tr><td>

[convertToFill(pourFillId)](./IPCB_PrimitivePoured.md)

</td><td>

</td><td>

**_(BETA)_** Convert to: fill primitive

</td></tr>
<tr><td>

[deletePourFills(pourFillIds)](./IPCB_PrimitivePoured.md)

</td><td>

</td><td>

**_(BETA)_** Delete Copper fill region

</td></tr>
<tr><td>

[getState\_PourFills()](./IPCB_PrimitivePoured.md)

</td><td>

</td><td>

Get the property state: copper fill region

</td></tr>
<tr><td>

[getState\_PourPrimitiveId()](./IPCB_PrimitivePoured.md)

</td><td>

</td><td>

Get the property state: copper border primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveId()](./IPCB_PrimitivePoured.md)

</td><td>

</td><td>

Get the property state: primitive ID

</td></tr>
<tr><td>

[getState\_PrimitiveType()](./IPCB_PrimitivePoured.md)

</td><td>

</td><td>

Get the property state: primitive type

</td></tr>
<tr><td>

[reset()](./IPCB_PrimitivePoured.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
</tbody></table>

---

## 方法详情

### addsoldermaskfill

# IPCB\_PrimitivePoured.addSolderMaskFill() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Add: solder mask region

## Signature

```typescript
function addSolderMaskFill(
	pourFillId: IPCB_PrimitivePouredPourFill['id'],
): Promise<IPCB_PrimitiveFill | undefined>;
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

pourFillId

</td><td>

[IPCB\_PrimitivePouredPourFill](../interfaces/IPCB_PrimitivePouredPourFill.md)<!-- -->\['id'\]

</td><td>

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md) \| undefined&gt;

The solder mask region fill primitive object. If conversion fails or the ID is incorrect, `undefined` is returned

### converttofill

# IPCB\_PrimitivePoured.convertToFill() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Convert to: fill primitive

## Signature

```typescript
function convertToFill(
	pourFillId: IPCB_PrimitivePouredPourFill['id'],
): Promise<IPCB_PrimitiveFill | undefined>;
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

pourFillId

</td><td>

[IPCB\_PrimitivePouredPourFill](../interfaces/IPCB_PrimitivePouredPourFill.md)<!-- -->\['id'\]

</td><td>

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveFill](./IPCB_PrimitiveFill.md) \| undefined&gt;

The fill primitive object. If conversion fails or the ID is incorrect, `undefined` is returned

### deletepourfills

# IPCB\_PrimitivePoured.deletePourFills() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete Copper fill region

## Signature

```typescript
function deletePourFills(
	pourFillIds: IPCB_PrimitivePouredPourFill['id'] | Array<IPCB_PrimitivePouredPourFill['id']>,
): Promise<boolean>;
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

pourFillIds

</td><td>

[IPCB\_PrimitivePouredPourFill](../interfaces/IPCB_PrimitivePouredPourFill.md)<!-- -->\['id'\] \| Array&lt;[IPCB\_PrimitivePouredPourFill](../interfaces/IPCB_PrimitivePouredPourFill.md)<!-- -->\['id'\]&gt;

</td><td>

Copper fill region ID

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Delete Whether the operation is successful

### getstate_pourfills

# IPCB\_PrimitivePoured.getState\_PourFills() method

Get the property state: copper fill region

## Signature

```typescript
function getState_PourFills(): Array<IPCB_PrimitivePouredPourFill>;
```

## Returns

Array&lt;[IPCB\_PrimitivePouredPourFill](../interfaces/IPCB_PrimitivePouredPourFill.md)<!-- -->&gt;

Copper fill region

### getstate_pourprimitiveid

# IPCB\_PrimitivePoured.getState\_PourPrimitiveId() method

Get the property state: copper border primitive ID

## Signature

```typescript
function getState_PourPrimitiveId(): string;
```

## Returns

string

Copper border primitive ID

### getstate_primitiveid

# IPCB\_PrimitivePoured.getState\_PrimitiveId() method

Get the property state: primitive ID

## Signature

```typescript
function getState_PrimitiveId(): string;
```

## Returns

string

Primitive ID

### getstate_primitivetype

# IPCB\_PrimitivePoured.getState\_PrimitiveType() method

Get the property state: primitive type

## Signature

```typescript
function getState_PrimitiveType(): EPCB_PrimitiveType;
```

## Returns

[EPCB\_PrimitiveType](../enums/EPCB_PrimitiveType.md)

Primitive type

### reset

# IPCB\_PrimitivePoured.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<IPCB_PrimitivePoured>;
```

## Returns

Promise&lt;[IPCB\_PrimitivePoured](./IPCB_PrimitivePoured.md)<!-- -->&gt;

Copper fill primitive object

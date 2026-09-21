# PCB\_PrimitiveAttribute class

PCB &amp; footprint / property primitive class

## Signature

```typescript
class PCB_PrimitiveAttribute implements IPCB_PrimitiveAPI
```
**Implements:** [IPCB\_PrimitiveAPI](../interfaces/IPCB_PrimitiveAPI.md)

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[delete(primitiveIds)](./PCB_PrimitiveAttribute.md)

</td><td>

</td><td>

**_(BETA)_** Delete Property

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitiveAttribute.md)

</td><td>

</td><td>

**_(BETA)_** Get Property

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitiveAttribute.md)

</td><td>

</td><td>

**_(BETA)_** Get Property

</td></tr>
<tr><td>

[getAll(parentPrimitiveId, layer, primitiveLock)](./PCB_PrimitiveAttribute.md)

</td><td>

</td><td>

**_(BETA)_** Get all Property

</td></tr>
<tr><td>

[getAllPrimitiveId(parentPrimitiveId, layer, primitiveLock)](./PCB_PrimitiveAttribute.md)

</td><td>

</td><td>

**_(BETA)_** Get all Property primitive IDs

</td></tr>
<tr><td>

[modify(primitiveId, property)](./PCB_PrimitiveAttribute.md)

</td><td>

</td><td>

**_(BETA)_** Modify Text

</td></tr>
</tbody></table>

---

## 方法详情

### delete

# PCB\_PrimitiveAttribute.delete() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete Property

## Signature

```typescript
function delete(primitiveIds: string | IPCB_PrimitiveAttribute | Array<string> | Array<IPCB_PrimitiveAttribute>): Promise<boolean>;
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

primitiveIds

</td><td>

string \| [IPCB\_PrimitiveAttribute](./IPCB_PrimitiveAttribute.md) \| Array&lt;string&gt; \| Array&lt;[IPCB\_PrimitiveAttribute](./IPCB_PrimitiveAttribute.md)<!-- -->&gt;

</td><td>

Property primitive ID or Text primitive object

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Delete Whether the operation is successful

### get

# PCB\_PrimitiveAttribute.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Property

## Signature

```typescript
function get(primitiveIds: string): Promise<IPCB_PrimitiveAttribute | undefined>;
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

primitiveIds

</td><td>

string

</td><td>

Property primitive ID, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveAttribute](./IPCB_PrimitiveAttribute.md) \| undefined&gt;

Attribute primitive object, `undefined` indicates that the retrieval failed

### get_1

# PCB\_PrimitiveAttribute.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Property

## Signature

```typescript
function get(primitiveIds: Array<string>): Promise<Array<IPCB_PrimitiveAttribute>>;
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

primitiveIds

</td><td>

Array&lt;string&gt;

</td><td>

Property primitive ID, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveAttribute](./IPCB_PrimitiveAttribute.md)<!-- -->&gt;&gt;

Property primitive object; an empty array indicates that the retrieval failed

## Remarks

If multiple primitive IDs are passed in, a primitive ID that is not matched will not affect the return of other primitives; that is, fewer primitive objects than the number of primitive IDs passed in may be returned.

### getall

# PCB\_PrimitiveAttribute.getAll() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all Property

## Signature

```typescript
function getAll(
	parentPrimitiveId?: string,
	layer?: TPCB_LayersOfImage,
	primitiveLock?: boolean,
): Promise<Array<IPCB_PrimitiveAttribute>>;
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

parentPrimitiveId

</td><td>

string

</td><td>

_(Optional)_ Associated parent primitive ID

</td></tr>
<tr><td>

layer

</td><td>

[TPCB\_LayersOfImage](../types/TPCB_LayersOfImage.md)

</td><td>

_(Optional)_ Layer

</td></tr>
<tr><td>

primitiveLock

</td><td>

boolean

</td><td>

_(Optional)_ Whether it is locked

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveAttribute](./IPCB_PrimitiveAttribute.md)<!-- -->&gt;&gt;

Array of Property primitive objects

### getallprimitiveid

# PCB\_PrimitiveAttribute.getAllPrimitiveId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all Property primitive IDs

## Signature

```typescript
function getAllPrimitiveId(
	parentPrimitiveId?: string,
	layer?: TPCB_LayersOfImage,
	primitiveLock?: boolean,
): Promise<Array<string>>;
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

parentPrimitiveId

</td><td>

string

</td><td>

_(Optional)_ Associated parent primitive ID

</td></tr>
<tr><td>

layer

</td><td>

[TPCB\_LayersOfImage](../types/TPCB_LayersOfImage.md)

</td><td>

_(Optional)_ Layer

</td></tr>
<tr><td>

primitiveLock

</td><td>

boolean

</td><td>

_(Optional)_ Whether it is locked

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;string&gt;&gt;

Array of Property primitive IDs

### modify

# PCB\_PrimitiveAttribute.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Text

## Signature

```typescript
function modify(
	primitiveId: string | IPCB_PrimitiveAttribute,
	property: {
		layer?: TPCB_LayersOfImage;
		x?: number;
		y?: number;
		key?: string;
		value?: string;
		keyVisible?: boolean;
		valueVisible?: boolean;
		fontFamily?: string;
		fontSize?: number;
		lineWidth?: number;
		alignMode?: EPCB_PrimitiveStringAlignMode;
		rotation?: number;
		reverse?: boolean;
		expansion?: number;
		mirror?: boolean;
		primitiveLock?: boolean;
	},
): Promise<IPCB_PrimitiveAttribute | undefined>;
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

primitiveId

</td><td>

string \| [IPCB\_PrimitiveAttribute](./IPCB_PrimitiveAttribute.md)

</td><td>

Primitive ID

</td></tr>
<tr><td>

property

</td><td>

{ layer?: [TPCB\_LayersOfImage](../types/TPCB_LayersOfImage.md)<!-- -->; x?: number; y?: number; key?: string; value?: string; keyVisible?: boolean; valueVisible?: boolean; fontFamily?: string; fontSize?: number; lineWidth?: number; alignMode?: [EPCB\_PrimitiveStringAlignMode](../enums/EPCB_PrimitiveStringAlignMode.md)<!-- -->; rotation?: number; reverse?: boolean; expansion?: number; mirror?: boolean; primitiveLock?: boolean }

</td><td>

Modify Parameter

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveAttribute](./IPCB_PrimitiveAttribute.md) \| undefined&gt;

Text primitive object

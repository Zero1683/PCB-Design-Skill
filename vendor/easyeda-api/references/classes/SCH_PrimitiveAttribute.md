# SCH\_PrimitiveAttribute class

Schematic &amp; symbol / property primitive class

## Signature

```typescript
class SCH_PrimitiveAttribute implements ISCH_PrimitiveAPI
```
**Implements:** [ISCH\_PrimitiveAPI](../interfaces/ISCH_PrimitiveAPI.md)

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[createNetLabel(x, y, net)](./SCH_PrimitiveAttribute.md)

</td><td>

</td><td>

**_(BETA)_** Create a net label

</td></tr>
<tr><td>

[get(primitiveIds)](./SCH_PrimitiveAttribute.md)

</td><td>

</td><td>

**_(BETA)_** Get Property

</td></tr>
<tr><td>

[get(primitiveIds)](./SCH_PrimitiveAttribute.md)

</td><td>

</td><td>

**_(BETA)_** Get Property

</td></tr>
<tr><td>

[getAll(parentPrimitiveId)](./SCH_PrimitiveAttribute.md)

</td><td>

</td><td>

**_(BETA)_** Get all Property

</td></tr>
<tr><td>

[getAllPrimitiveId(parentPrimitiveId)](./SCH_PrimitiveAttribute.md)

</td><td>

</td><td>

**_(BETA)_** Get all Property primitive IDs

</td></tr>
<tr><td>

[modify(primitiveId, property)](./SCH_PrimitiveAttribute.md)

</td><td>

</td><td>

**_(BETA)_** Modify Property

</td></tr>
</tbody></table>

---

## 方法详情

### createnetlabel

# SCH\_PrimitiveAttribute.createNetLabel() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create a net label

## Signature

```typescript
function createNetLabel(
	x: number,
	y: number,
	net: string,
): Promise<ISCH_PrimitiveAttribute | undefined>;
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
<tr><td>

y

</td><td>

number

</td><td>

Y coordinate

</td></tr>
<tr><td>

net

</td><td>

string

</td><td>

Net name

</td></tr>
</tbody></table>

## Returns

Promise&lt;[ISCH\_PrimitiveAttribute](./ISCH_PrimitiveAttribute.md) \| undefined&gt;

Net label attribute primitive

## Remarks

ADD since EDA v4

### get

# SCH\_PrimitiveAttribute.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Property

## Signature

```typescript
function get(primitiveIds: string): Promise<ISCH_PrimitiveAttribute | undefined>;
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

Promise&lt;[ISCH\_PrimitiveAttribute](./ISCH_PrimitiveAttribute.md) \| undefined&gt;

Attribute primitive object, `undefined` indicates that the retrieval failed

### get_1

# SCH\_PrimitiveAttribute.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Property

## Signature

```typescript
function get(primitiveIds: Array<string>): Promise<Array<ISCH_PrimitiveAttribute>>;
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

Promise&lt;Array&lt;[ISCH\_PrimitiveAttribute](./ISCH_PrimitiveAttribute.md)<!-- -->&gt;&gt;

Property primitive object; an empty array indicates that the retrieval failed

## Remarks

If multiple primitive IDs are passed in, a primitive ID that is not matched will not affect the return of other primitives; that is, fewer primitive objects than the number of primitive IDs passed in may be returned.

### getall

# SCH\_PrimitiveAttribute.getAll() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all Property

## Signature

```typescript
function getAll(parentPrimitiveId?: string): Promise<Array<ISCH_PrimitiveAttribute>>;
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

_(Optional)_ Parent primitive ID

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[ISCH\_PrimitiveAttribute](./ISCH_PrimitiveAttribute.md)<!-- -->&gt;&gt;

Array of Property primitive objects

## Remarks

If no parent primitive ID is passed, all attribute primitives in the sheet will be obtained

### getallprimitiveid

# SCH\_PrimitiveAttribute.getAllPrimitiveId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all Property primitive IDs

## Signature

```typescript
function getAllPrimitiveId(parentPrimitiveId?: string): Promise<Array<string>>;
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

_(Optional)_ Parent primitive ID

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;string&gt;&gt;

Array of Property primitive IDs

## Remarks

If no parent primitive ID is passed, all attribute primitives in the sheet will be obtained

### modify

# SCH\_PrimitiveAttribute.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Property

## Signature

```typescript
function modify(
	primitiveId: string | ISCH_PrimitiveAttribute,
	property: {
		x?: number | null;
		y?: number | null;
		rotation?: number | null;
		color?: string | null;
		fontName?: string | null;
		fontSize?: number | null;
		bold?: boolean | null;
		italic?: boolean | null;
		underLine?: boolean | null;
		alignMode?: ESCH_PrimitiveTextAlignMode | null;
		fillColor?: string | null;
		key?: string;
		value?: string;
		keyVisible?: boolean | null;
		valueVisible?: boolean | null;
	},
): Promise<ISCH_PrimitiveAttribute | undefined>;
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

string \| [ISCH\_PrimitiveAttribute](./ISCH_PrimitiveAttribute.md)

</td><td>

Primitive ID

</td></tr>
<tr><td>

property

</td><td>

{ x?: number \| null; y?: number \| null; rotation?: number \| null; color?: string \| null; fontName?: string \| null; fontSize?: number \| null; bold?: boolean \| null; italic?: boolean \| null; underLine?: boolean \| null; alignMode?: [ESCH\_PrimitiveTextAlignMode](../enums/ESCH_PrimitiveTextAlignMode.md) \| null; fillColor?: string \| null; key?: string; value?: string; keyVisible?: boolean \| null; valueVisible?: boolean \| null }

</td><td>

Modify Parameter

</td></tr>
</tbody></table>

## Returns

Promise&lt;[ISCH\_PrimitiveAttribute](./ISCH_PrimitiveAttribute.md) \| undefined&gt;

Attribute primitive object

# PCB\_PrimitiveString class

PCB &amp; footprint / text primitive class

## Signature

```typescript
class PCB_PrimitiveString implements IPCB_PrimitiveAPI
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

[create(layer, x, y, text, fontFamily, fontSize, lineWidth, alignMode, rotation, reverse, expansion, mirror, primitiveLock)](./PCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Create Text

</td></tr>
<tr><td>

[delete(primitiveIds)](./PCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Delete Text

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Get Text

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Get Text

</td></tr>
<tr><td>

[getAll(layer, primitiveLock)](./PCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Get all Text

</td></tr>
<tr><td>

[getAllPrimitiveId(layer, primitiveLock)](./PCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Get all Text primitive IDs

</td></tr>
<tr><td>

[modify(primitiveId, property)](./PCB_PrimitiveString.md)

</td><td>

</td><td>

**_(BETA)_** Modify Text

</td></tr>
</tbody></table>

---

## 方法详情

### create

# PCB\_PrimitiveString.create() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create Text

## Signature

```typescript
function create(
	layer: TPCB_LayersOfImage,
	x: number,
	y: number,
	text: string,
	fontFamily: string,
	fontSize: number,
	lineWidth: number,
	alignMode: EPCB_PrimitiveStringAlignMode,
	rotation: number,
	reverse: boolean,
	expansion: number,
	mirror: boolean,
	primitiveLock: boolean,
): Promise<IPCB_PrimitiveString | undefined>;
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

[TPCB\_LayersOfImage](../types/TPCB_LayersOfImage.md)

</td><td>

Layer

</td></tr>
<tr><td>

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

text

</td><td>

string

</td><td>

Text content

</td></tr>
<tr><td>

fontFamily

</td><td>

string

</td><td>

Font. It needs to be imported into EasyEDA in advance

</td></tr>
<tr><td>

fontSize

</td><td>

number

</td><td>

Font size

</td></tr>
<tr><td>

lineWidth

</td><td>

number

</td><td>

Line width

</td></tr>
<tr><td>

alignMode

</td><td>

[EPCB\_PrimitiveStringAlignMode](../enums/EPCB_PrimitiveStringAlignMode.md)

</td><td>

Alignment mode

</td></tr>
<tr><td>

rotation

</td><td>

number

</td><td>

Rotation angle

</td></tr>
<tr><td>

reverse

</td><td>

boolean

</td><td>

Whether it is inverted

</td></tr>
<tr><td>

expansion

</td><td>

number

</td><td>

Inverted expansion

</td></tr>
<tr><td>

mirror

</td><td>

boolean

</td><td>

Whether it is mirrored

</td></tr>
<tr><td>

primitiveLock

</td><td>

boolean

</td><td>

Whether it is locked

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md) \| undefined&gt;

Text primitive object

### delete

# PCB\_PrimitiveString.delete() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete Text

## Signature

```typescript
function delete(primitiveIds: string | IPCB_PrimitiveString | Array<string> | Array<IPCB_PrimitiveString>): Promise<boolean>;
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

string \| [IPCB\_PrimitiveString](./IPCB_PrimitiveString.md) \| Array&lt;string&gt; \| Array&lt;[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)<!-- -->&gt;

</td><td>

Text primitive ID or Text primitive object

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Delete Whether the operation is successful

### get

# PCB\_PrimitiveString.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Text

## Signature

```typescript
function get(primitiveIds: string): Promise<IPCB_PrimitiveString | undefined>;
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

Text primitive ID, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md) \| undefined&gt;

Text primitive object, `undefined` indicates that the retrieval failed

### get_1

# PCB\_PrimitiveString.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Text

## Signature

```typescript
function get(primitiveIds: Array<string>): Promise<Array<IPCB_PrimitiveString>>;
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

Text primitive ID, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)<!-- -->&gt;&gt;

Text primitive object; an empty array indicates that the retrieval failed

## Remarks

If multiple primitive IDs are passed in, a primitive ID that is not matched will not affect the return of other primitives; that is, fewer primitive objects than the number of primitive IDs passed in may be returned.

### getall

# PCB\_PrimitiveString.getAll() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all Text

## Signature

```typescript
function getAll(
	layer?: TPCB_LayersOfImage,
	primitiveLock?: boolean,
): Promise<Array<IPCB_PrimitiveString>>;
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

Promise&lt;Array&lt;[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)<!-- -->&gt;&gt;

Array of Text primitive objects

### getallprimitiveid

# PCB\_PrimitiveString.getAllPrimitiveId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all Text primitive IDs

## Signature

```typescript
function getAllPrimitiveId(
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

Array of Text primitive IDs

### modify

# PCB\_PrimitiveString.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Text

## Signature

```typescript
function modify(
	primitiveId: string | IPCB_PrimitiveString,
	property: {
		layer?: TPCB_LayersOfImage;
		x?: number;
		y?: number;
		text?: string;
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
): Promise<IPCB_PrimitiveString | undefined>;
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

string \| [IPCB\_PrimitiveString](./IPCB_PrimitiveString.md)

</td><td>

Primitive ID

</td></tr>
<tr><td>

property

</td><td>

{ layer?: [TPCB\_LayersOfImage](../types/TPCB_LayersOfImage.md)<!-- -->; x?: number; y?: number; text?: string; fontFamily?: string; fontSize?: number; lineWidth?: number; alignMode?: [EPCB\_PrimitiveStringAlignMode](../enums/EPCB_PrimitiveStringAlignMode.md)<!-- -->; rotation?: number; reverse?: boolean; expansion?: number; mirror?: boolean; primitiveLock?: boolean }

</td><td>

Modify Parameter

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveString](./IPCB_PrimitiveString.md) \| undefined&gt;

Text primitive object

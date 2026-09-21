# PCB\_PrimitiveImage class

PCB &amp; footprint / image primitive class

## Signature

```typescript
class PCB_PrimitiveImage implements IPCB_PrimitiveAPI
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

[create(x, y, complexPolygon, layer, width, height, rotation, horizonMirror, primitiveLock)](./PCB_PrimitiveImage.md)

</td><td>

</td><td>

Create Image

</td></tr>
<tr><td>

[delete(primitiveIds)](./PCB_PrimitiveImage.md)

</td><td>

</td><td>

**_(BETA)_** Delete Image

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitiveImage.md)

</td><td>

</td><td>

**_(BETA)_** Get Image

</td></tr>
<tr><td>

[get(primitiveIds)](./PCB_PrimitiveImage.md)

</td><td>

</td><td>

**_(BETA)_** Get Image

</td></tr>
<tr><td>

[getAll(layer, primitiveLock)](./PCB_PrimitiveImage.md)

</td><td>

</td><td>

**_(BETA)_** Get all Image

</td></tr>
<tr><td>

[getAllPrimitiveId(layer, primitiveLock)](./PCB_PrimitiveImage.md)

</td><td>

</td><td>

**_(BETA)_** Get all Image primitive IDs

</td></tr>
<tr><td>

[modify(primitiveId, property)](./PCB_PrimitiveImage.md)

</td><td>

</td><td>

**_(BETA)_** Modify Image

</td></tr>
</tbody></table>

---

## 方法详情

### create

# PCB\_PrimitiveImage.create() method

Create Image

## Signature

```typescript
function create(
	x: number,
	y: number,
	complexPolygon:
		| TPCB_PolygonSourceArray
		| Array<TPCB_PolygonSourceArray>
		| IPCB_Polygon
		| IPCB_ComplexPolygon,
	layer: TPCB_LayersOfImage,
	width?: number,
	height?: number,
	rotation?: number,
	horizonMirror?: boolean,
	primitiveLock?: boolean,
): Promise<IPCB_PrimitiveImage | undefined>;
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

BBox top-left point coordinates X

</td></tr>
<tr><td>

y

</td><td>

number

</td><td>

BBox top-left point coordinates Y

</td></tr>
<tr><td>

complexPolygon

</td><td>

[TPCB\_PolygonSourceArray](../types/TPCB_PolygonSourceArray.md) \| Array&lt;[TPCB\_PolygonSourceArray](../types/TPCB_PolygonSourceArray.md)<!-- -->&gt; \| [IPCB\_Polygon](./IPCB_Polygon.md) \| [IPCB\_ComplexPolygon](./IPCB_ComplexPolygon.md)

</td><td>

Image source data (complex polygon). You can use the [PCB\_MathPolygon.convertImageToComplexPolygon()](./PCB_MathPolygon.md) method to convert an image file into complex polygon data

</td></tr>
<tr><td>

layer

</td><td>

[TPCB\_LayersOfImage](../types/TPCB_LayersOfImage.md)

</td><td>

Layer

</td></tr>
<tr><td>

width

</td><td>

number

</td><td>

_(Optional)_ Width

</td></tr>
<tr><td>

height

</td><td>

number

</td><td>

_(Optional)_ Height

</td></tr>
<tr><td>

rotation

</td><td>

number

</td><td>

_(Optional)_ Rotation angle

</td></tr>
<tr><td>

horizonMirror

</td><td>

boolean

</td><td>

_(Optional)_ Whether it is horizontally mirrored

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

Promise&lt;[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md) \| undefined&gt;

Image primitive object

## Remarks

To create a color silkscreen image, use the [binary embedded object primitive class](./PCB_PrimitiveObject.md)

### delete

# PCB\_PrimitiveImage.delete() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete Image

## Signature

```typescript
function delete(primitiveIds: string | IPCB_PrimitiveImage | Array<string> | Array<IPCB_PrimitiveImage>): Promise<boolean>;
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

string \| [IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md) \| Array&lt;string&gt; \| Array&lt;[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md)<!-- -->&gt;

</td><td>

Image primitive ID or Image primitive object

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Delete Whether the operation is successful

### get

# PCB\_PrimitiveImage.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Image

## Signature

```typescript
function get(primitiveIds: string): Promise<IPCB_PrimitiveImage | undefined>;
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

Image primitive ID, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md) \| undefined&gt;

Image primitive object, `undefined` indicates that the retrieval failed

### get_1

# PCB\_PrimitiveImage.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Image

## Signature

```typescript
function get(primitiveIds: Array<string>): Promise<Array<IPCB_PrimitiveImage>>;
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

Image primitive ID, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md)<!-- -->&gt;&gt;

Image primitive object; an empty array indicates that the retrieval failed

## Remarks

If multiple primitive IDs are passed in, a primitive ID that is not matched will not affect the return of other primitives; that is, fewer primitive objects than the number of primitive IDs passed in may be returned.

### getall

# PCB\_PrimitiveImage.getAll() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all Image

## Signature

```typescript
function getAll(
	layer?: TPCB_LayersOfImage,
	primitiveLock?: boolean,
): Promise<Array<IPCB_PrimitiveImage>>;
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

Promise&lt;Array&lt;[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md)<!-- -->&gt;&gt;

Array of Image primitive objects

### getallprimitiveid

# PCB\_PrimitiveImage.getAllPrimitiveId() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all Image primitive IDs

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

Array of Image primitive IDs

### modify

# PCB\_PrimitiveImage.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Image

## Signature

```typescript
function modify(
	primitiveId: string | IPCB_PrimitiveImage,
	property: {
		x?: number;
		y?: number;
		layer?: TPCB_LayersOfImage;
		width?: number;
		height?: number;
		rotation?: number;
		horizonMirror?: boolean;
		primitiveLock?: boolean;
	},
): Promise<IPCB_PrimitiveImage | undefined>;
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

string \| [IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md)

</td><td>

Primitive ID

</td></tr>
<tr><td>

property

</td><td>

{ x?: number; y?: number; layer?: [TPCB\_LayersOfImage](../types/TPCB_LayersOfImage.md)<!-- -->; width?: number; height?: number; rotation?: number; horizonMirror?: boolean; primitiveLock?: boolean }

</td><td>

Modify Parameter

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_PrimitiveImage](./IPCB_PrimitiveImage.md) \| undefined&gt;

Image primitive object

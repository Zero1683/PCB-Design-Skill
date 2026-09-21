# SCH\_PrimitiveRectangle class

Schematic &amp; symbol / rectangle primitive class

## Signature

```typescript
class SCH_PrimitiveRectangle implements ISCH_PrimitiveAPI
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

[create(topLeftX, topLeftY, width, height, cornerRadius, rotation, color, fillColor, lineWidth, lineType, fillStyle)](./SCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Create Rectangle

</td></tr>
<tr><td>

[delete(primitiveIds)](./SCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Delete Rectangle

</td></tr>
<tr><td>

[get(primitiveIds)](./SCH_PrimitiveRectangle.md)

</td><td>

</td><td>

**_(BETA)_** Get Rectangle

</td></tr>
<tr><td>

[get(primitiveIds)](./SCH_PrimitiveRectangle.md)

</td><td>

</td><td>

**_(BETA)_** Get Rectangle

</td></tr>
<tr><td>

[getAll()](./SCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Get all Rectangle

</td></tr>
<tr><td>

[getAllPrimitiveId()](./SCH_PrimitiveRectangle.md)

</td><td>

</td><td>

Get all Rectangle primitive IDs

</td></tr>
<tr><td>

[modify(primitiveId, property)](./SCH_PrimitiveRectangle.md)

</td><td>

</td><td>

**_(BETA)_** Modify Rectangle

</td></tr>
</tbody></table>

---

## 方法详情

### create

# SCH\_PrimitiveRectangle.create() method

Create Rectangle

## Signature

```typescript
function create(
	topLeftX: number,
	topLeftY: number,
	width: number,
	height: number,
	cornerRadius?: number,
	rotation?: number,
	color?: string | null,
	fillColor?: string | null,
	lineWidth?: number | null,
	lineType?: ESCH_PrimitiveLineType | null,
	fillStyle?: ESCH_PrimitiveFillStyle | null,
): Promise<ISCH_PrimitiveRectangle | undefined>;
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

topLeftX

</td><td>

number

</td><td>

Top-left point X

</td></tr>
<tr><td>

topLeftY

</td><td>

number

</td><td>

Top-left point Y

</td></tr>
<tr><td>

width

</td><td>

number

</td><td>

Width

</td></tr>
<tr><td>

height

</td><td>

number

</td><td>

Height

</td></tr>
<tr><td>

cornerRadius

</td><td>

number

</td><td>

_(Optional)_ Corner radius

</td></tr>
<tr><td>

rotation

</td><td>

number

</td><td>

_(Optional)_ Rotation angle, rotating around the top-left point. Options: `0` `90` `180` `270`

</td></tr>
<tr><td>

color

</td><td>

string \| null

</td><td>

_(Optional)_ Color, `null` indicates the default

</td></tr>
<tr><td>

fillColor

</td><td>

string \| null

</td><td>

_(Optional)_ Fill color. `none` indicates no fill, `null` indicates the default

</td></tr>
<tr><td>

lineWidth

</td><td>

number \| null

</td><td>

_(Optional)_ Line width, range `1-10`<!-- -->. `null` indicates the default

</td></tr>
<tr><td>

lineType

</td><td>

[ESCH\_PrimitiveLineType](../enums/ESCH_PrimitiveLineType.md) \| null

</td><td>

_(Optional)_ Line type. `null` indicates the default

</td></tr>
<tr><td>

fillStyle

</td><td>

[ESCH\_PrimitiveFillStyle](../enums/ESCH_PrimitiveFillStyle.md) \| null

</td><td>

_(Optional)_ Fill style, `null` indicates the default

</td></tr>
</tbody></table>

## Returns

Promise&lt;[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md) \| undefined&gt;

Rectangle primitive object

### delete

# SCH\_PrimitiveRectangle.delete() method

Delete Rectangle

## Signature

```typescript
function delete(primitiveIds: string | ISCH_PrimitiveRectangle | Array<string> | Array<ISCH_PrimitiveRectangle>): Promise<boolean>;
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

string \| [ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md) \| Array&lt;string&gt; \| Array&lt;[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)<!-- -->&gt;

</td><td>

Rectangle primitive ID or Rectangle primitive object

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Delete Whether the operation is successful

### get

# SCH\_PrimitiveRectangle.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Rectangle

## Signature

```typescript
function get(primitiveIds: string): Promise<ISCH_PrimitiveRectangle | undefined>;
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

Rectangle primitive ID, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md) \| undefined&gt;

Rectangle primitive object, `undefined` indicates that the retrieval failed

### get_1

# SCH\_PrimitiveRectangle.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Rectangle

## Signature

```typescript
function get(primitiveIds: Array<string>): Promise<Array<ISCH_PrimitiveRectangle>>;
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

Rectangle primitive ID, which can be a string or an array of strings. If it is an array, an array is also returned

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)<!-- -->&gt;&gt;

Rectangle primitive object; an empty array indicates that the retrieval failed

## Remarks

If multiple primitive IDs are passed in, a primitive ID that is not matched will not affect the return of other primitives; that is, fewer primitive objects than the number of primitive IDs passed in may be returned.

### getall

# SCH\_PrimitiveRectangle.getAll() method

Get all Rectangle

## Signature

```typescript
function getAll(): Promise<Array<ISCH_PrimitiveRectangle>>;
```

## Returns

Promise&lt;Array&lt;[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)<!-- -->&gt;&gt;

Array of Rectangle primitive objects

### getallprimitiveid

# SCH\_PrimitiveRectangle.getAllPrimitiveId() method

Get all Rectangle primitive IDs

## Signature

```typescript
function getAllPrimitiveId(): Promise<Array<string>>;
```

## Returns

Promise&lt;Array&lt;string&gt;&gt;

Array of Rectangle primitive IDs

### modify

# SCH\_PrimitiveRectangle.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Rectangle

## Signature

```typescript
function modify(
	primitiveId: string | ISCH_PrimitiveRectangle,
	property: {
		topLeftX?: number;
		topLeftY?: number;
		width?: number;
		height?: number;
		cornerRadius?: number;
		rotation?: number;
		color?: string | null;
		fillColor?: string | null;
		lineWidth?: number | null;
		lineType?: ESCH_PrimitiveLineType | null;
		fillStyle?: ESCH_PrimitiveFillStyle | null;
	},
): Promise<ISCH_PrimitiveRectangle | undefined>;
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

string \| [ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md)

</td><td>

Primitive ID

</td></tr>
<tr><td>

property

</td><td>

{ topLeftX?: number; topLeftY?: number; width?: number; height?: number; cornerRadius?: number; rotation?: number; color?: string \| null; fillColor?: string \| null; lineWidth?: number \| null; lineType?: [ESCH\_PrimitiveLineType](../enums/ESCH_PrimitiveLineType.md) \| null; fillStyle?: [ESCH\_PrimitiveFillStyle](../enums/ESCH_PrimitiveFillStyle.md) \| null }

</td><td>

Modify Parameter

</td></tr>
</tbody></table>

## Returns

Promise&lt;[ISCH\_PrimitiveRectangle](./ISCH_PrimitiveRectangle.md) \| undefined&gt;

Rectangle primitive object

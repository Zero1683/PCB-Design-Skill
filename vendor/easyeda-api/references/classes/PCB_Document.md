# PCB\_Document class

PCB &amp; footprint / document operation class

## Signature

```typescript
class PCB_Document
```

## Remarks

Operations performed on the design document as a whole

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[autoRouting(props)](./PCB_Document.md)

</td><td>

</td><td>

**_(BETA)_** Auto routing

</td></tr>
<tr><td>

[clearRouting(type)](./PCB_Document.md)

</td><td>

</td><td>

**_(BETA)_** Clear routing

</td></tr>
<tr><td>

[convertCanvasOriginToDataOrigin(x, y)](./PCB_Document.md)

</td><td>

</td><td>

Input a canvas coordinate and return the data coordinate corresponding to that coordinate

</td></tr>
<tr><td>

[convertDataOriginToCanvasOrigin(x, y)](./PCB_Document.md)

</td><td>

</td><td>

Input a data coordinate and return the canvas coordinate corresponding to that coordinate

</td></tr>
<tr><td>

[getCalculatingRatlineStatus()](./PCB_Document.md)

</td><td>

</td><td>

Get the current ratline calculation function status

</td></tr>
<tr><td>

[getCanvasOrigin()](./PCB_Document.md)

</td><td>

</td><td>

Get the offset coordinate of the canvas origin relative to the data origin

</td></tr>
<tr><td>

[getCurrentFilterConfiguration()](./PCB_Document.md)

</td><td>

</td><td>

**_(BETA)_** Get Current canvas filter configuration

</td></tr>
<tr><td>

[getPrimitiveAtPoint(x, y)](./PCB_Document.md)

</td><td>

</td><td>

**_(BETA)_** Get The primitive at the coordinate point

</td></tr>
<tr><td>

[getPrimitivesInRegion(left, right, top, bottom, leftToRight)](./PCB_Document.md)

</td><td>

</td><td>

**_(BETA)_** Get All primitives in the region

</td></tr>
<tr><td>

[importAutoLayoutJsonFile(autoLayoutFile)](./PCB_Document.md)

</td><td>

</td><td>

**_(BETA)_** Import auto layout file (JSON)

</td></tr>
<tr><td>

[importAutoRouteJsonFile(autoRouteFile)](./PCB_Document.md)

</td><td>

</td><td>

**_(BETA)_** Import auto routing file (JSON)

</td></tr>
<tr><td>

[importAutoRouteSesFile(autoRouteFile)](./PCB_Document.md)

</td><td>

</td><td>

**_(BETA)_** Import auto routing file (SES)

</td></tr>
<tr><td>

[importChanges(uuid)](./PCB_Document.md)

</td><td>

</td><td>

Import changes from the schematic

</td></tr>
<tr><td>

[navigateToCoordinates(x, y)](./PCB_Document.md)

</td><td>

</td><td>

Locate to canvas coordinate

</td></tr>
<tr><td>

[navigateToRegion(left, right, top, bottom)](./PCB_Document.md)

</td><td>

</td><td>

**_(BETA)_** Locate to canvas region

</td></tr>
<tr><td>

[save()](./PCB_Document.md)

</td><td>

</td><td>

Save Document

</td></tr>
<tr><td>

[setCanvasOrigin(offsetX, offsetY)](./PCB_Document.md)

</td><td>

</td><td>

Set the offset coordinate of the canvas origin relative to the data origin

</td></tr>
<tr><td>

[startCalculatingRatline()](./PCB_Document.md)

</td><td>

</td><td>

Start the ratline calculation function

</td></tr>
<tr><td>

[stopCalculatingRatline()](./PCB_Document.md)

</td><td>

</td><td>

Stop the ratline calculation function

</td></tr>
<tr><td>

[zoomToBoardOutline()](./PCB_Document.md)

</td><td>

</td><td>

**_(BETA)_** Zoom to the board outline (fit the board outline)

</td></tr>
</tbody></table>

---

## 方法详情

### autorouting

# PCB\_Document.autoRouting() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Auto routing

## Signature

```typescript
function autoRouting(props?: IPCB_AutoRoutingProps): Promise<IPCB_AutoRoutingResult>;
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

props

</td><td>

[IPCB\_AutoRoutingProps](../interfaces/IPCB_AutoRoutingProps.md)

</td><td>

_(Optional)_ Auto routing parameter

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_AutoRoutingResult](../interfaces/IPCB_AutoRoutingResult.md)<!-- -->&gt;

Auto routing result

## Remarks

If no parameters are passed in, auto routing will be performed for all unrouted nets

## Example

```javascript
// 对所有未布线的网络进行自动布线
const result = await eda.pcb_Document.autoRouting();
console.log(`布线完成：${result.routedNets}/${result.totalNets}`);

// 指定网络进行自动布线，并忽略部分网络
const result = await eda.pcb_Document.autoRouting({
    nets: ['VCC', 'GND', 'SDA', 'SCL'],
    ignoreNets: ['NC'],
    cornerStyle: EPCB_AutoRoutingCornerStyle.DEGREE_45,
    optimization: EPCB_AutoRoutingOptimization.COMPLETION,
});
```

### clearrouting

# PCB\_Document.clearRouting() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Clear routing

## Signature

```typescript
function clearRouting(type?: 'all' | 'net' | 'connection'): Promise<boolean>;
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

type

</td><td>

'all' \| 'net' \| 'connection'

</td><td>

_(Optional)_ Clear type. If you need to specify a clear type, select the specified primitive in advance

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

### convertcanvasorigintodataorigin

# PCB\_Document.convertCanvasOriginToDataOrigin() method

Input a canvas coordinate and return the data coordinate corresponding to that coordinate

## Signature

```typescript
function convertCanvasOriginToDataOrigin(x: number, y: number): Promise<{ x: number; y: number }>;
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

</td></tr>
<tr><td>

y

</td><td>

number

</td><td>

</td></tr>
</tbody></table>

## Returns

Promise&lt;{ x: number; y: number }&gt;

Data origin coordinate

## Remarks

The coordinates displayed on the EasyEDA front end are all relative to the canvas origin; the EasyEDA API uses the data origin; when creating a PCB, the default canvas origin equals the data origin

### convertdataorigintocanvasorigin

# PCB\_Document.convertDataOriginToCanvasOrigin() method

Input a data coordinate and return the canvas coordinate corresponding to that coordinate

## Signature

```typescript
function convertDataOriginToCanvasOrigin(x: number, y: number): Promise<{ x: number; y: number }>;
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

Data origin X

</td></tr>
<tr><td>

y

</td><td>

number

</td><td>

Data origin Y

</td></tr>
</tbody></table>

## Returns

Promise&lt;{ x: number; y: number }&gt;

Canvas origin coordinate

## Remarks

The coordinates displayed on the EasyEDA front end are all relative to the canvas origin; the EasyEDA API uses the data origin; when creating a PCB, the default canvas origin equals the data origin

### getcalculatingratlinestatus

# PCB\_Document.getCalculatingRatlineStatus() method

Get the current ratline calculation function status

## Signature

```typescript
function getCalculatingRatlineStatus(): Promise<EPCB_DocumentRatlineCalculatingActiveStatus>;
```

## Returns

Promise&lt;[EPCB\_DocumentRatlineCalculatingActiveStatus](../enums/EPCB_DocumentRatlineCalculatingActiveStatus.md)<!-- -->&gt;

Function state

### getcanvasorigin

# PCB\_Document.getCanvasOrigin() method

Get the offset coordinate of the canvas origin relative to the data origin

## Signature

```typescript
function getCanvasOrigin(): Promise<{ offsetX: number; offsetY: number }>;
```

## Returns

Promise&lt;{ offsetX: number; offsetY: number }&gt;

The offset coordinate of the canvas origin relative to the data origin

## Remarks

The coordinates displayed on the EasyEDA Pro front end are all relative to the canvas origin;

The EasyEDA Pro API uses the data origin;

If the returned data is `{ canvasOriginOffsetX: 100, canvasOriginOffsetY: 200 }`<!-- -->, it means the canvas origin is at a position 100 units to the right and 200 units up from the data origin;

The units here are data-level units, which are equivalent to mil on the canvas level in span

### getcurrentfilterconfiguration

# PCB\_Document.getCurrentFilterConfiguration() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Current canvas filter configuration

## Signature

```typescript
function getCurrentFilterConfiguration(): Promise<{ [key: string]: any } | undefined>;
```

## Returns

Promise&lt;{ \[key: string\]: any } \| undefined&gt;

Current canvas filter configuration; `undefined` indicates that the retrieval failed

### getprimitiveatpoint

# PCB\_Document.getPrimitiveAtPoint() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get The primitive at the coordinate point

## Signature

```typescript
function getPrimitiveAtPoint(x: number, y: number): Promise<IPCB_Primitive | undefined>;
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

Coordinate point X

</td></tr>
<tr><td>

y

</td><td>

number

</td><td>

Coordinate point Y

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IPCB\_Primitive](../interfaces/IPCB_Primitive.md) \| undefined&gt;

The primitive at the coordinate point. If no primitive can be found at the coordinate point, `undefined` will be returned

## Remarks

This operation is similar to clicking with the mouse on the front end; it will get the primitive at the specified coordinate point

### getprimitivesinregion

# PCB\_Document.getPrimitivesInRegion() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get All primitives in the region

## Signature

```typescript
function getPrimitivesInRegion(
	left: number,
	right: number,
	top: number,
	bottom: number,
	leftToRight?: boolean,
): Promise<Array<IPCB_Primitive>>;
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

left

</td><td>

number

</td><td>

First X coordinate of the rectangle

</td></tr>
<tr><td>

right

</td><td>

number

</td><td>

Second X coordinate of the rectangle

</td></tr>
<tr><td>

top

</td><td>

number

</td><td>

First Y coordinate of the rectangle

</td></tr>
<tr><td>

bottom

</td><td>

number

</td><td>

Second Y coordinate of the rectangle

</td></tr>
<tr><td>

leftToRight

</td><td>

boolean

</td><td>

_(Optional)_ Whether to only get primitives that are fully enclosed by the box selection. If `false`<!-- -->, primitives touched by the selection are also obtained

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_Primitive](../interfaces/IPCB_Primitive.md)<!-- -->&gt;&gt;

All primitives in the region

### importautolayoutjsonfile

# PCB\_Document.importAutoLayoutJsonFile() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Import auto layout file (JSON)

## Signature

```typescript
function importAutoLayoutJsonFile(autoLayoutFile: File): Promise<boolean>;
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

autoLayoutFile

</td><td>

File

</td><td>

The JSON file to import

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the import operation is successful

## Remarks

You can use  to read in a file

### importautoroutejsonfile

# PCB\_Document.importAutoRouteJsonFile() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Import auto routing file (JSON)

## Signature

```typescript
function importAutoRouteJsonFile(autoRouteFile: File): Promise<boolean>;
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

autoRouteFile

</td><td>

File

</td><td>

The JSON file to import

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the import operation is successful

## Remarks

You can use  to read in a file

### importautoroutesesfile

# PCB\_Document.importAutoRouteSesFile() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Import auto routing file (SES)

## Signature

```typescript
function importAutoRouteSesFile(autoRouteFile: File): Promise<boolean>;
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

autoRouteFile

</td><td>

File

</td><td>

The SES file to import

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the import operation is successful

## Remarks

You can use  to read in a file

### importchanges

# PCB\_Document.importChanges() method

Import changes from the schematic

## Signature

```typescript
function importChanges(uuid?: string): Promise<boolean>;
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

uuid

</td><td>

string

</td><td>

_(Optional)_ Schematic UUID. By default, the schematic associated with the same Board is used

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the import operation was successful. If the import fails or the free PCB has no schematic UUID passed in, `false` is returned

### navigatetocoordinates

# PCB\_Document.navigateToCoordinates() method

Locate to canvas coordinate

## Signature

```typescript
function navigateToCoordinates(x: number, y: number): Promise<boolean>;
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
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

This API positions on the front-end canvas to the specified data-level coordinate;

If you want the front-end canvas coordinate to be consistent with the passed-in data during this operation, it is recommended to call the [PCB\_Document.setCanvasOrigin()](./PCB_Document.md) method and set the offset to zero;

The units here are data-level units, which are equivalent to mil on the canvas level in span

### navigatetoregion

# PCB\_Document.navigateToRegion() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Locate to canvas region

## Signature

```typescript
function navigateToRegion(
	left: number,
	right: number,
	top: number,
	bottom: number,
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

left

</td><td>

number

</td><td>

First X coordinate of the rectangle

</td></tr>
<tr><td>

right

</td><td>

number

</td><td>

Second X coordinate of the rectangle

</td></tr>
<tr><td>

top

</td><td>

number

</td><td>

First Y coordinate of the rectangle

</td></tr>
<tr><td>

bottom

</td><td>

number

</td><td>

Second Y coordinate of the rectangle

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

This API positions on the front-end canvas to the specified region. The region data is an offset relative to the data origin;

For example: the passed-in data is `{left: 0, right: 60, top: 100, bottom: -20}` =<!-- -->&gt; `navigateToRegion(0, 60, 100, -20)`<!-- -->, then the canvas will be positioned to a rectangular range centered at `[30, 40]` with a length of `60` in the x-axis direction and `120` in the y-axis direction;

This API does not perform zooming, but it will generate a rectangle frame indicating the positioning center and the region range;

The units here are data-level units, which are equivalent to mil on the canvas level in span

### save

# PCB\_Document.save() method

Save Document

## Signature

```typescript
function save(): Promise<boolean>;
```

## Returns

Promise&lt;boolean&gt;

Whether the save operation was successful. Errors such as save failure and upload failure all return `false`

### setcanvasorigin

# PCB\_Document.setCanvasOrigin() method

Set the offset coordinate of the canvas origin relative to the data origin

## Signature

```typescript
function setCanvasOrigin(offsetX: number, offsetY: number): Promise<boolean>;
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

offsetX

</td><td>

number

</td><td>

X coordinate offset of the canvas origin relative to the data origin

</td></tr>
<tr><td>

offsetY

</td><td>

number

</td><td>

Y coordinate offset of the canvas origin relative to the data origin

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

The coordinates displayed on the EasyEDA Pro front end are all relative to the canvas origin;

The EasyEDA Pro API uses the data origin;

If you want the front-end canvas coordinate to be consistent with the data during API operations, it is recommended to call this method and set the offset to zero, i.e. `setCanvasOrigin(0, 0)`<!-- -->;

The units here are data-level units, which are equivalent to mil on the canvas level in span

### startcalculatingratline

# PCB\_Document.startCalculatingRatline() method

Start the ratline calculation function

## Signature

```typescript
function startCalculatingRatline(): Promise<boolean>;
```

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

A ratline calculation will be triggered when starting

### stopcalculatingratline

# PCB\_Document.stopCalculatingRatline() method

Stop the ratline calculation function

## Signature

```typescript
function stopCalculatingRatline(): Promise<boolean>;
```

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### zoomtoboardoutline

# PCB\_Document.zoomToBoardOutline() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Zoom to the board outline (fit the board outline)

## Signature

```typescript
function zoomToBoardOutline(): Promise<boolean>;
```

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

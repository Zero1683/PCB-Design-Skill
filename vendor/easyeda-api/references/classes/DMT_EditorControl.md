# DMT\_EditorControl class

Document tree / Editor control class

## Signature

```typescript
class DMT_EditorControl
```

## Remarks

Here the editor control is based on the sheets under the currently open engineering design. Any other `documentUuid` will be considered a non-existent document page

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[activateDocument(tabId)](./DMT_EditorControl.md)

</td><td>

</td><td>

Activate a document

</td></tr>
<tr><td>

[activateSplitScreen(splitScreenId)](./DMT_EditorControl.md)

</td><td>

</td><td>

Activate a split screen

</td></tr>
<tr><td>

[closeDocument(tabId)](./DMT_EditorControl.md)

</td><td>

</td><td>

Close document

</td></tr>
<tr><td>

[createSplitScreen(splitScreenType, tabId)](./DMT_EditorControl.md)

</td><td>

</td><td>

Create Split screen

</td></tr>
<tr><td>

[generateIndicatorMarkers(markers, color, lineWidth, zoom, tabId)](./DMT_EditorControl.md)

</td><td>

</td><td>

**_(BETA)_** Generate indicator markers

</td></tr>
<tr><td>

[getCurrentRenderedAreaImage(tabId)](./DMT_EditorControl.md)

</td><td>

</td><td>

**_(BETA)_** Get the canvas rendering region image

</td></tr>
<tr><td>

[getSplitScreenIdByTabId(tabId)](./DMT_EditorControl.md)

</td><td>

</td><td>

Use tab ID get split screen ID

</td></tr>
<tr><td>

[getSplitScreenTree()](./DMT_EditorControl.md)

</td><td>

</td><td>

Get the editor split screen property tree

</td></tr>
<tr><td>

[getTabsBySplitScreenId(splitScreenId)](./DMT_EditorControl.md)

</td><td>

</td><td>

Get all tabs under the specified split screen ID

</td></tr>
<tr><td>

[mergeAllDocumentFromSplitScreen()](./DMT_EditorControl.md)

</td><td>

</td><td>

Merge all split screens

</td></tr>
<tr><td>

[moveDocumentToSplitScreen(tabId, splitScreenId)](./DMT_EditorControl.md)

</td><td>

</td><td>

Move a document to the specified split screen

</td></tr>
<tr><td>

[openDocument(documentUuid, splitScreenId)](./DMT_EditorControl.md)

</td><td>

</td><td>

Open document

</td></tr>
<tr><td>

[openLibraryDocument(libraryUuid, libraryType, uuid, splitScreenId)](./DMT_EditorControl.md)

</td><td>

</td><td>

**_(BETA)_** Open library symbol, footprint document

</td></tr>
<tr><td>

[removeIndicatorMarkers(tabId)](./DMT_EditorControl.md)

</td><td>

</td><td>

**_(BETA)_** Remove indicator markers

</td></tr>
<tr><td>

[tileAllDocumentToSplitScreen()](./DMT_EditorControl.md)

</td><td>

</td><td>

Tile all documents

</td></tr>
<tr><td>

[zoomTo(x, y, scaleRatio, tabId)](./DMT_EditorControl.md)

</td><td>

</td><td>

**_(BETA)_** Zoom to coordinates

</td></tr>
<tr><td>

[zoomToAllPrimitives(tabId)](./DMT_EditorControl.md)

</td><td>

</td><td>

**_(BETA)_** Zoom to all primitives (fit all)

</td></tr>
<tr><td>

[zoomToRegion(left, right, top, bottom, tabId)](./DMT_EditorControl.md)

</td><td>

</td><td>

**_(BETA)_** Zoom to region

</td></tr>
<tr><td>

[zoomToSelectedPrimitives(tabId)](./DMT_EditorControl.md)

</td><td>

</td><td>

**_(BETA)_** Zoom to the selected primitives (fit selection)

</td></tr>
</tbody></table>

---

## 方法详情

### activatedocument

# DMT\_EditorControl.activateDocument() method

Activate a document

## Signature

```typescript
function activateDocument(tabId: string): Promise<boolean>;
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

tabId

</td><td>

string

</td><td>

Tab ID

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

Switch to the tab of the specified document and place the input focus in it

### activatesplitscreen

# DMT\_EditorControl.activateSplitScreen() method

Activate a split screen

## Signature

```typescript
function activateSplitScreen(splitScreenId: string): Promise<boolean>;
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

splitScreenId

</td><td>

string

</td><td>

Split screen ID

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

Give input focus

### closedocument

# DMT\_EditorControl.closeDocument() method

Close document

## Signature

```typescript
function closeDocument(tabId: string): Promise<boolean>;
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

tabId

</td><td>

string

</td><td>

Tab ID. Here [IDMT\_SchematicPageItem.uuid](../interfaces/IDMT_SchematicPageItem.md)<!-- -->, [IDMT\_PcbItem.uuid](../interfaces/IDMT_PcbItem.md)<!-- -->, and [IDMT\_PanelItem.uuid](../interfaces/IDMT_PanelItem.md) are supported as input

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

If the document has not been saved, executing this operation will directly lose all unsaved data. After completing modification operations, first execute [SCH\_Document.save()](./SCH_Document.md)<!-- -->, [PCB\_Document.save()](./PCB_Document.md)<!-- -->, and [PNL\_Document.save()](./PNL_Document.md) to save the data

### createsplitscreen

# DMT\_EditorControl.createSplitScreen() method

Create Split screen

## Signature

```typescript
function createSplitScreen(
	splitScreenType: EDMT_EditorSplitScreenDirection,
	tabId: string,
): Promise<{ sourceSplitScreenId: string; newSplitScreenId: string } | undefined>;
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

splitScreenType

</td><td>

[EDMT\_EditorSplitScreenDirection](../enums/EDMT_EditorSplitScreenDirection.md)

</td><td>

Split screen type, `horizontal` horizontal, `vertical` vertical

</td></tr>
<tr><td>

tabId

</td><td>

string

</td><td>

Tab ID. This tab will be moved into the new split screen

</td></tr>
</tbody></table>

## Returns

Promise&lt;{ sourceSplitScreenId: string; newSplitScreenId: string } \| undefined&gt;

Split screen ID. `sourceSplitScreenId` represents the source split screen, and `newSplitScreenId` represents the new split screen

## Remarks

Please make sure the split screen corresponding to [tabId](./DMT_EditorControl.md) has more than two tabs; otherwise the split screen will not be executed and `undefined` will be returned

### generateindicatormarkers

# DMT\_EditorControl.generateIndicatorMarkers() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Generate indicator markers

## Signature

```typescript
function generateIndicatorMarkers(
	markers: Array<IDMT_IndicatorMarkerShape>,
	color?: { r: number; g: number; b: number; alpha: number },
	lineWidth?: number,
	zoom?: boolean,
	tabId?: string,
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

markers

</td><td>

Array&lt;[IDMT\_IndicatorMarkerShape](../interfaces/IDMT_IndicatorMarkerShape.md)<!-- -->&gt;

</td><td>

Array of indicator marker shape objects

</td></tr>
<tr><td>

color

</td><td>

\{ r: number; g: number; b: number; alpha: number \}

</td><td>

_(Optional)_ Indicator marker color

</td></tr>
<tr><td>

lineWidth

</td><td>

number

</td><td>

_(Optional)_ Line width

</td></tr>
<tr><td>

zoom

</td><td>

boolean

</td><td>

_(Optional)_ Whether to locate and zoom

</td></tr>
<tr><td>

tabId

</td><td>

string

</td><td>

_(Optional)_ Tab ID. If not passed in, the canvas with the last input focus will be used

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the indicator markers were generated successfully, `false` indicates that the canvas does not support this operation or `tabId` does not exist

## Remarks

In the indicator marker shape data, the coordinate unit span of the schematic and symbol canvases is 0.01inch, and that of the PCB and footprint canvases is mil

### getcurrentrenderedareaimage

# DMT\_EditorControl.getCurrentRenderedAreaImage() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the canvas rendering region image

## Signature

```typescript
function getCurrentRenderedAreaImage(tabId?: string): Promise<Blob | undefined>;
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

tabId

</td><td>

string

</td><td>

_(Optional)_ Tab ID. If not passed in, the canvas with the last input focus will be obtained

</td></tr>
</tbody></table>

## Returns

Promise&lt;Blob \| undefined&gt;

- Blob-format image data of the canvas rendering region

### getsplitscreenidbytabid

# DMT\_EditorControl.getSplitScreenIdByTabId() method

Use tab ID get split screen ID

## Signature

```typescript
function getSplitScreenIdByTabId(tabId: string): Promise<string | undefined>;
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

tabId

</td><td>

string

</td><td>

Tab ID

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

Split screen ID

### getsplitscreentree

# DMT\_EditorControl.getSplitScreenTree() method

Get the editor split screen property tree

## Signature

```typescript
function getSplitScreenTree(): Promise<IDMT_EditorSplitScreenItem | undefined>;
```

## Returns

Promise&lt;[IDMT\_EditorSplitScreenItem](../interfaces/IDMT_EditorSplitScreenItem.md) \| undefined&gt;

The editor split screen property tree. If it is `undefined`<!-- -->, the data retrieval failed

### gettabsbysplitscreenid

# DMT\_EditorControl.getTabsBySplitScreenId() method

Get all tabs under the specified split screen ID

## Signature

```typescript
function getTabsBySplitScreenId(splitScreenId: string): Promise<Array<IDMT_EditorTabItem>>;
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

splitScreenId

</td><td>

string

</td><td>

Split screen ID

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IDMT\_EditorTabItem](../interfaces/IDMT_EditorTabItem.md)<!-- -->&gt;&gt;

Tab list

## Remarks

If there are no direct tabs under the specified split screen (that is, it still has [children](../interfaces/IDMT_EditorSplitScreenItem.md) under it), an empty array will be returned

### mergealldocumentfromsplitscreen

# DMT\_EditorControl.mergeAllDocumentFromSplitScreen() method

Merge all split screens

## Signature

```typescript
function mergeAllDocumentFromSplitScreen(): Promise<boolean>;
```

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

Only available when child split screens exist. It will cancel all child split screens and merge all document tabs into the initial split screen

### movedocumenttosplitscreen

# DMT\_EditorControl.moveDocumentToSplitScreen() method

Move a document to the specified split screen

## Signature

```typescript
function moveDocumentToSplitScreen(tabId: string, splitScreenId: string): Promise<boolean>;
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

tabId

</td><td>

string

</td><td>

Tab ID

</td></tr>
<tr><td>

splitScreenId

</td><td>

string

</td><td>

[Split screen ID](../interfaces/IDMT_EditorSplitScreenItem.md)

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

After moving the document, the editor split screen property tree may change

### opendocument

# DMT\_EditorControl.openDocument() method

Open document

## Signature

```typescript
function openDocument(documentUuid: string, splitScreenId?: string): Promise<string | undefined>;
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

documentUuid

</td><td>

string

</td><td>

Document UUID. Here [IDMT\_SchematicItem.uuid](../interfaces/IDMT_SchematicItem.md)<!-- -->, [IDMT\_SchematicPageItem.uuid](../interfaces/IDMT_SchematicPageItem.md)<!-- -->, [IDMT\_PcbItem.uuid](../interfaces/IDMT_PcbItem.md)<!-- -->, and [IDMT\_PanelItem.uuid](../interfaces/IDMT_PanelItem.md) are supported as input

</td></tr>
<tr><td>

splitScreenId

</td><td>

string

</td><td>

_(Optional)_ Split screen ID, which is the [IDMT\_EditorSplitScreenItem.id](../interfaces/IDMT_EditorSplitScreenItem.md) obtained by the [DMT\_EditorControl.getSplitScreenTree()](./DMT_EditorControl.md) method

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

Tab ID, if it is `undefined`<!-- -->, then open document failed

### openlibrarydocument

# DMT\_EditorControl.openLibraryDocument() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Open library symbol, footprint document

## Signature

```typescript
function openLibraryDocument(
	libraryUuid: string,
	libraryType: ELIB_LibraryType.SYMBOL | ELIB_LibraryType.FOOTPRINT,
	uuid: string,
	splitScreenId?: string,
): Promise<string | undefined>;
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

libraryUuid

</td><td>

string

</td><td>

Library UUID, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
<tr><td>

libraryType

</td><td>

[ELIB\_LibraryType.SYMBOL](../enums/ELIB_LibraryType.md) \| [ELIB\_LibraryType.FOOTPRINT](../enums/ELIB_LibraryType.md)

</td><td>

Library type, support symbol and footprint

</td></tr>
<tr><td>

uuid

</td><td>

string

</td><td>

Symbol, footprint UUID

</td></tr>
<tr><td>

splitScreenId

</td><td>

string

</td><td>

_(Optional)_ Split screen ID, which is the [IDMT\_EditorSplitScreenItem.id](../interfaces/IDMT_EditorSplitScreenItem.md) obtained by the [DMT\_EditorControl.getSplitScreenTree()](./DMT_EditorControl.md) method

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

Tab ID, if it is `undefined`<!-- -->, then open document failed

### removeindicatormarkers

# DMT\_EditorControl.removeIndicatorMarkers() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Remove indicator markers

## Signature

```typescript
function removeIndicatorMarkers(tabId?: string): Promise<boolean>;
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

tabId

</td><td>

string

</td><td>

_(Optional)_ Tab ID. If not passed in, the canvas with the last input focus will be used

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the indicator markers were removed successfully, `false` indicates that the canvas does not support this operation or `tabId` does not exist

## Remarks

This API will remove all generated indicator markers

### tilealldocumenttosplitscreen

# DMT\_EditorControl.tileAllDocumentToSplitScreen() method

Tile all documents

## Signature

```typescript
function tileAllDocumentToSplitScreen(): Promise<boolean>;
```

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

Only available when no child split screens exist. It will automatically create split screens for all opened document tabs

### zoomto

# DMT\_EditorControl.zoomTo() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Zoom to coordinates

## Signature

```typescript
function zoomTo(
	x?: number,
	y?: number,
	scaleRatio?: number,
	tabId?: string,
): Promise<{ left: number; right: number; top: number; bottom: number } | false>;
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

_(Optional)_ Center X coordinate. If not passed in, the current X coordinate will not be changed

</td></tr>
<tr><td>

y

</td><td>

number

</td><td>

_(Optional)_ Center Y coordinate. If not passed in, the current Y coordinate will not be changed

</td></tr>
<tr><td>

scaleRatio

</td><td>

number

</td><td>

_(Optional)_ Zoom ratio. If not passed in, the current zoom ratio will not be changed. The unit span is `1/100`<!-- -->. If `200` is passed in, it means a zoom ratio of `200%`

</td></tr>
<tr><td>

tabId

</td><td>

string

</td><td>

_(Optional)_ Tab ID. If not passed in, the canvas with the last input focus will be used

</td></tr>
</tbody></table>

## Returns

Promise&lt;{ left: number; right: number; top: number; bottom: number } \| false&gt;

Region data after zooming. `false` indicates that the canvas does not support the zoom operation or the `tabId` does not exist

## Remarks

In the schematic and symbol canvases, the coordinate unit span is 0.01inch; in the PCB and footprint canvases, it is mil

### zoomtoallprimitives

# DMT\_EditorControl.zoomToAllPrimitives() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Zoom to all primitives (fit all)

## Signature

```typescript
function zoomToAllPrimitives(
	tabId?: string,
): Promise<{ left: number; right: number; top: number; bottom: number } | false>;
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

tabId

</td><td>

string

</td><td>

_(Optional)_ Tab ID. If not passed in, the canvas with the last input focus will be used

</td></tr>
</tbody></table>

## Returns

Promise&lt;{ left: number; right: number; top: number; bottom: number } \| false&gt;

Region data after zooming. `false` indicates that the canvas does not support the zoom operation or the `tabId` does not exist

## Remarks

In the returned data, the coordinate unit span of the schematic and symbol canvases is 0.01inch, and that of the PCB and footprint canvases is mil

### zoomtoregion

# DMT\_EditorControl.zoomToRegion() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Zoom to region

## Signature

```typescript
function zoomToRegion(
	left: number,
	right: number,
	top: number,
	bottom: number,
	tabId?: string,
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
<tr><td>

tabId

</td><td>

string

</td><td>

_(Optional)_ Tab ID. If not passed in, the canvas with the last input focus will be used

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

In the schematic and symbol canvases, the coordinate unit span is 0.01inch; in the PCB and footprint canvases, it is mil

### zoomtoselectedprimitives

# DMT\_EditorControl.zoomToSelectedPrimitives() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Zoom to the selected primitives (fit selection)

## Signature

```typescript
function zoomToSelectedPrimitives(
	tabId?: string,
): Promise<{ left: number; right: number; top: number; bottom: number } | false>;
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

tabId

</td><td>

string

</td><td>

_(Optional)_ Tab ID. If not passed in, the canvas with the last input focus will be used

</td></tr>
</tbody></table>

## Returns

Promise&lt;{ left: number; right: number; top: number; bottom: number } \| false&gt;

Region data after zooming. `false` indicates that the canvas does not support the zoom operation or the `tabId` does not exist

## Remarks

In the returned data, the coordinate unit span of the schematic and symbol canvases is 0.01inch, and that of the PCB and footprint canvases is mil

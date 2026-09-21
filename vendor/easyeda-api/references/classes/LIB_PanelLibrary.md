# LIB\_PanelLibrary class

Comprehensive library / panel library class

## Signature

```typescript
class LIB_PanelLibrary
```

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[copy(panelLibraryUuid, libraryUuid, targetLibraryUuid, targetClassification, newPanelLibraryName)](./LIB_PanelLibrary.md)

</td><td>

</td><td>

**_(BETA)_** Copy Panel library

</td></tr>
<tr><td>

[create(libraryUuid, panelLibraryName, classification, description)](./LIB_PanelLibrary.md)

</td><td>

</td><td>

**_(BETA)_** Create Panel library

</td></tr>
<tr><td>

[delete(panelLibraryUuid, libraryUuid)](./LIB_PanelLibrary.md)

</td><td>

</td><td>

**_(BETA)_** Delete Panel library

</td></tr>
<tr><td>

[get(panelLibraryUuid, libraryUuid)](./LIB_PanelLibrary.md)

</td><td>

</td><td>

**_(BETA)_** Get all properties of the panel library

</td></tr>
<tr><td>

[modify(panelLibraryUuid, libraryUuid, panelLibraryName, classification, description)](./LIB_PanelLibrary.md)

</td><td>

</td><td>

**_(BETA)_** Modify Panel library

</td></tr>
<tr><td>

[openInEditor(panelLibraryUuid, libraryUuid, splitScreenId)](./LIB_PanelLibrary.md)

</td><td>

</td><td>

**_(BETA)_** Open in the editor document

</td></tr>
<tr><td>

[search(key, libraryUuid, classification, itemsOfPage, page)](./LIB_PanelLibrary.md)

</td><td>

</td><td>

**_(BETA)_** Search panel library

</td></tr>
</tbody></table>

---

## 方法详情

### copy

# LIB\_PanelLibrary.copy() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Copy Panel library

## Signature

```typescript
function copy(
	panelLibraryUuid: string,
	libraryUuid: string,
	targetLibraryUuid: string,
	targetClassification?: ILIB_ClassificationIndex | Array<string>,
	newPanelLibraryName?: string,
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

panelLibraryUuid

</td><td>

string

</td><td>

Panel library UUID

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

Library UUID, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
<tr><td>

targetLibraryUuid

</td><td>

string

</td><td>

Target library UUID

</td></tr>
<tr><td>

targetClassification

</td><td>

[ILIB\_ClassificationIndex](../interfaces/ILIB_ClassificationIndex.md) \| Array&lt;string&gt;

</td><td>

_(Optional)_ Classification in the target library

</td></tr>
<tr><td>

newPanelLibraryName

</td><td>

string

</td><td>

_(Optional)_ New panel library name. If a panel library with the same name exists in the target library, the copy will fail

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

UUID of the new panel library in the target library

### create

# LIB\_PanelLibrary.create() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create Panel library

## Signature

```typescript
function create(
	libraryUuid: string,
	panelLibraryName: string,
	classification?: ILIB_ClassificationIndex | Array<string>,
	description?: string,
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

panelLibraryName

</td><td>

string

</td><td>

Panel library name

</td></tr>
<tr><td>

classification

</td><td>

[ILIB\_ClassificationIndex](../interfaces/ILIB_ClassificationIndex.md) \| Array&lt;string&gt;

</td><td>

_(Optional)_ Classification

</td></tr>
<tr><td>

description

</td><td>

string

</td><td>

_(Optional)_ Description

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

Panel library UUID

### delete

# LIB\_PanelLibrary.delete() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete Panel library

## Signature

```typescript
function delete(panelLibraryUuid: string, libraryUuid: string): Promise<boolean>;
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

panelLibraryUuid

</td><td>

string

</td><td>

Panel library UUID

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

Library UUID, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### get

# LIB\_PanelLibrary.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all properties of the panel library

## Signature

```typescript
function get(
	panelLibraryUuid: string,
	libraryUuid?: string,
): Promise<ILIB_PanelLibraryItem | undefined>;
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

panelLibraryUuid

</td><td>

string

</td><td>

Panel library UUID

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

_(Optional)_ Library UUID, default is system library, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
</tbody></table>

## Returns

Promise&lt;[ILIB\_PanelLibraryItem](../interfaces/ILIB_PanelLibraryItem.md) \| undefined&gt;

Panel library property

### modify

# LIB\_PanelLibrary.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Panel library

## Signature

```typescript
function modify(
	panelLibraryUuid: string,
	libraryUuid: string,
	panelLibraryName?: string,
	classification?: ILIB_ClassificationIndex | Array<string> | null,
	description?: string | null,
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

panelLibraryUuid

</td><td>

string

</td><td>

Panel library UUID

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

Library UUID, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
<tr><td>

panelLibraryName

</td><td>

string

</td><td>

_(Optional)_ Panel library name

</td></tr>
<tr><td>

classification

</td><td>

[ILIB\_ClassificationIndex](../interfaces/ILIB_ClassificationIndex.md) \| Array&lt;string&gt; \| null

</td><td>

_(Optional)_ Classification

</td></tr>
<tr><td>

description

</td><td>

string \| null

</td><td>

_(Optional)_ Description

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

If you want to clear certain properties, set their values to `null`

### openineditor

# LIB\_PanelLibrary.openInEditor() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Open in the editor document

## Signature

```typescript
function openInEditor(
	panelLibraryUuid: string,
	libraryUuid: string,
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

panelLibraryUuid

</td><td>

string

</td><td>

Panel library UUID

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

Library UUID, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
<tr><td>

splitScreenId

</td><td>

string

</td><td>

_(Optional)_ Split screen ID. If not filled in, it opens in the split screen with the last input focus by default. It can be obtained using the APIs in [DMT\_EditorControl](./DMT_EditorControl.md)

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

Tab ID, corresponding to [IDMT\_EditorTabItem.tabId](../interfaces/IDMT_EditorTabItem.md)<!-- -->. You can use [DMT\_EditorControl.getSplitScreenIdByTabId()](./DMT_EditorControl.md) to get the split screen ID

### search

# LIB\_PanelLibrary.search() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Search panel library

## Signature

```typescript
function search(
	key: string,
	libraryUuid?: string,
	classification?: ILIB_ClassificationIndex | Array<string>,
	itemsOfPage?: number,
	page?: number,
): Promise<Array<ILIB_PanelLibrarySearchItem>>;
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

key

</td><td>

string

</td><td>

Search keyword

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

_(Optional)_ Library UUID, default is system library, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
<tr><td>

classification

</td><td>

[ILIB\_ClassificationIndex](../interfaces/ILIB_ClassificationIndex.md) \| Array&lt;string&gt;

</td><td>

_(Optional)_ Classification, defaults to all

</td></tr>
<tr><td>

itemsOfPage

</td><td>

number

</td><td>

_(Optional)_ Number of search results per page

</td></tr>
<tr><td>

page

</td><td>

number

</td><td>

_(Optional)_ Page count

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[ILIB\_PanelLibrarySearchItem](../interfaces/ILIB_PanelLibrarySearchItem.md)<!-- -->&gt;&gt;

List of searched panel library properties

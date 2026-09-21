# LIB\_Cbb class

Comprehensive library / reuse block class

## Signature

```typescript
class LIB_Cbb
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

[copy(cbbUuid, libraryUuid, targetLibraryUuid, targetClassification, newCbbName)](./LIB_Cbb.md)

</td><td>

</td><td>

**_(BETA)_** Copy Reuse block

</td></tr>
<tr><td>

[create(libraryUuid, cbbName, classification, description)](./LIB_Cbb.md)

</td><td>

</td><td>

**_(BETA)_** Create Reuse block

</td></tr>
<tr><td>

[delete(cbbUuid, libraryUuid)](./LIB_Cbb.md)

</td><td>

</td><td>

**_(BETA)_** Delete Reuse block

</td></tr>
<tr><td>

[get(cbbUuid, libraryUuid)](./LIB_Cbb.md)

</td><td>

</td><td>

**_(BETA)_** Get all properties of the reuse block

</td></tr>
<tr><td>

[modify(cbbUuid, libraryUuid, cbbName, classification, description)](./LIB_Cbb.md)

</td><td>

</td><td>

**_(BETA)_** Modify Reuse block

</td></tr>
<tr><td>

[openProjectInEditor(cbbUuid, libraryUuid)](./LIB_Cbb.md)

</td><td>

</td><td>

**_(BETA)_** Open in the editor reuse block project

</td></tr>
<tr><td>

[openSymbolInEditor(cbbUuid, libraryUuid, splitScreenId)](./LIB_Cbb.md)

</td><td>

</td><td>

**_(BETA)_** Open in the editor reuse block symbol

</td></tr>
<tr><td>

[search(key, libraryUuid, classification, itemsOfPage, page)](./LIB_Cbb.md)

</td><td>

</td><td>

**_(BETA)_** Search reuse block

</td></tr>
</tbody></table>

---

## 方法详情

### copy

# LIB\_Cbb.copy() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Copy Reuse block

## Signature

```typescript
function copy(
	cbbUuid: string,
	libraryUuid: string,
	targetLibraryUuid: string,
	targetClassification?: ILIB_ClassificationIndex | Array<string>,
	newCbbName?: string,
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

cbbUuid

</td><td>

string

</td><td>

Reuse block UUID

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

newCbbName

</td><td>

string

</td><td>

_(Optional)_ New reuse block name. If a reuse block with the same name exists in the target library, the copy will fail

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

UUID of the new reuse block in the target library

### create

# LIB\_Cbb.create() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create Reuse block

## Signature

```typescript
function create(
	libraryUuid: string,
	cbbName: string,
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

cbbName

</td><td>

string

</td><td>

Reuse block name

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

Reuse block UUID

### delete

# LIB\_Cbb.delete() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete Reuse block

## Signature

```typescript
function delete(cbbUuid: string, libraryUuid: string): Promise<boolean>;
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

cbbUuid

</td><td>

string

</td><td>

Reuse block UUID

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

# LIB\_Cbb.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all properties of the reuse block

## Signature

```typescript
function get(cbbUuid: string, libraryUuid?: string): Promise<ILIB_CbbItem | undefined>;
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

cbbUuid

</td><td>

string

</td><td>

Reuse block UUID

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

Promise&lt;[ILIB\_CbbItem](../interfaces/ILIB_CbbItem.md) \| undefined&gt;

Reuse block property

### modify

# LIB\_Cbb.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Reuse block

## Signature

```typescript
function modify(
	cbbUuid: string,
	libraryUuid: string,
	cbbName?: string,
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

cbbUuid

</td><td>

string

</td><td>

Reuse block UUID

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

Library UUID, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
<tr><td>

cbbName

</td><td>

string

</td><td>

_(Optional)_ Reuse block name

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

### openprojectineditor

# LIB\_Cbb.openProjectInEditor() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Open in the editor reuse block project

## Signature

```typescript
function openProjectInEditor(cbbUuid: string, libraryUuid: string): Promise<boolean>;
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

cbbUuid

</td><td>

string

</td><td>

Reuse block UUID

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

## Remarks

This operation will open the module project in the EDA front end. If another project was previously opened with unsaved changes, executing this operation will directly lose all unsaved data

### opensymbolineditor

# LIB\_Cbb.openSymbolInEditor() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Open in the editor reuse block symbol

## Signature

```typescript
function openSymbolInEditor(
	cbbUuid: string,
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

cbbUuid

</td><td>

string

</td><td>

Reuse block UUID

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

# LIB\_Cbb.search() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Search reuse block

## Signature

```typescript
function search(
	key: string,
	libraryUuid?: string,
	classification?: ILIB_ClassificationIndex | Array<string>,
	itemsOfPage?: number,
	page?: number,
): Promise<Array<ILIB_CbbSearchItem>>;
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

Promise&lt;Array&lt;[ILIB\_CbbSearchItem](../interfaces/ILIB_CbbSearchItem.md)<!-- -->&gt;&gt;

List of searched reuse block properties

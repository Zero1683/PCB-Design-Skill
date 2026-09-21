# LIB\_Footprint class

Comprehensive library / footprint class

## Signature

```typescript
class LIB_Footprint
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

[copy(footprintUuid, libraryUuid, targetLibraryUuid, targetClassification, newFootprintName)](./LIB_Footprint.md)

</td><td>

</td><td>

**_(BETA)_** Copy Footprint

</td></tr>
<tr><td>

[create(libraryUuid, footprintName, classification, description, otherProperty)](./LIB_Footprint.md)

</td><td>

</td><td>

**_(BETA)_** Create Footprint

</td></tr>
<tr><td>

[delete(footprintUuid, libraryUuid)](./LIB_Footprint.md)

</td><td>

</td><td>

**_(BETA)_** Delete Footprint

</td></tr>
<tr><td>

[get(footprintUuid, libraryUuid)](./LIB_Footprint.md)

</td><td>

</td><td>

**_(BETA)_** Get all properties of the footprint

</td></tr>
<tr><td>

[getRenderImage(source)](./LIB_Footprint.md)

</td><td>

</td><td>

**_(BETA)_** Get the footprint render image

</td></tr>
<tr><td>

[modify(footprintUuid, libraryUuid, footprintName, classification, description, otherProperty)](./LIB_Footprint.md)

</td><td>

</td><td>

**_(BETA)_** Modify Footprint

</td></tr>
<tr><td>

[openInEditor(footprintUuid, libraryUuid, splitScreenId)](./LIB_Footprint.md)

</td><td>

</td><td>

**_(BETA)_** Open in the editor document

</td></tr>
<tr><td>

[search(key, libraryUuid, classification, itemsOfPage, page)](./LIB_Footprint.md)

</td><td>

</td><td>

**_(BETA)_** Search footprint

</td></tr>
<tr><td>

[searchByProperties(properties, libraryUuid)](./LIB_Footprint.md)

</td><td>

</td><td>

**_(BETA)_** Search footprints precisely by properties

</td></tr>
<tr><td>

[updateDocumentSource(footprintUuid, libraryUuid, documentSource)](./LIB_Footprint.md)

</td><td>

</td><td>

**_(BETA)_** Update the document source code of the footprint

</td></tr>
</tbody></table>

---

## 方法详情

### copy

# LIB\_Footprint.copy() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Copy Footprint

## Signature

```typescript
function copy(
	footprintUuid: string,
	libraryUuid: string,
	targetLibraryUuid: string,
	targetClassification?: ILIB_ClassificationIndex | Array<string>,
	newFootprintName?: string,
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

footprintUuid

</td><td>

string

</td><td>

Footprint UUID

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

newFootprintName

</td><td>

string

</td><td>

_(Optional)_ New footprint name. If a footprint with the same name exists in the target library, the copy will fail

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

UUID of the new footprint in the target library

### create

# LIB\_Footprint.create() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create Footprint

## Signature

```typescript
function create(
	libraryUuid: string,
	footprintName: string,
	classification?: ILIB_ClassificationIndex | Array<string>,
	description?: string,
	otherProperty?: Record<string, boolean | number | string | undefined>,
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

footprintName

</td><td>

string

</td><td>

Footprint name

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
<tr><td>

otherProperty

</td><td>

Record&lt;string, boolean \| number \| string \| undefined&gt;

</td><td>

_(Optional)_ 其它属性

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

Footprint UUID

### delete

# LIB\_Footprint.delete() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete Footprint

## Signature

```typescript
function delete(footprintUuid: string, libraryUuid: string): Promise<boolean>;
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

footprintUuid

</td><td>

string

</td><td>

Footprint UUID

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

# LIB\_Footprint.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all properties of the footprint

## Signature

```typescript
function get(footprintUuid: string, libraryUuid?: string): Promise<ILIB_FootprintItem | undefined>;
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

footprintUuid

</td><td>

string

</td><td>

Footprint UUID

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

Promise&lt;[ILIB\_FootprintItem](../interfaces/ILIB_FootprintItem.md) \| undefined&gt;

Footprint property

### getrenderimage

# LIB\_Footprint.getRenderImage() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the footprint render image

## Signature

```typescript
function getRenderImage(source: {
	footprintUuid: string;
	libraryUuid: string;
}): Promise<Blob | undefined>;
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

source

</td><td>

\{ footprintUuid: string; libraryUuid: string \}

</td><td>

</td></tr>
</tbody></table>

## Returns

Promise&lt;Blob \| undefined&gt;

Footprint render image

### modify

# LIB\_Footprint.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Footprint

## Signature

```typescript
function modify(
	footprintUuid: string,
	libraryUuid: string,
	footprintName?: string,
	classification?: ILIB_ClassificationIndex | Array<string> | null,
	description?: string | null,
	otherProperty?: Record<string, boolean | number | string | undefined | null>,
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

footprintUuid

</td><td>

string

</td><td>

Footprint UUID

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

Library UUID, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
<tr><td>

footprintName

</td><td>

string

</td><td>

_(Optional)_ Footprint name

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
<tr><td>

otherProperty

</td><td>

Record&lt;string, boolean \| number \| string \| undefined \| null&gt;

</td><td>

_(Optional)_ 其它属性，如希望清除某些属性，则将其的值设置为 `null`

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

If you want to clear certain properties, set their values to `null`

### openineditor

# LIB\_Footprint.openInEditor() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Open in the editor document

## Signature

```typescript
function openInEditor(
	footprintUuid: string,
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

footprintUuid

</td><td>

string

</td><td>

Footprint UUID

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

# LIB\_Footprint.search() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Search footprint

## Signature

```typescript
function search(
	key: string,
	libraryUuid?: string,
	classification?: ILIB_ClassificationIndex | Array<string>,
	itemsOfPage?: number,
	page?: number,
): Promise<Array<ILIB_FootprintSearchItem>>;
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

Promise&lt;Array&lt;[ILIB\_FootprintSearchItem](../interfaces/ILIB_FootprintSearchItem.md)<!-- -->&gt;&gt;

List of searched footprint properties

### searchbyproperties

# LIB\_Footprint.searchByProperties() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Search footprints precisely by properties

## Signature

```typescript
function searchByProperties(
	properties: ILIB_FootprintPropertiesForSearch,
	libraryUuid?: string,
): Promise<Array<ILIB_FootprintSearchItem>>;
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

properties

</td><td>

[ILIB\_FootprintPropertiesForSearch](../interfaces/ILIB_FootprintPropertiesForSearch.md)

</td><td>

Property

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

Promise&lt;Array&lt;[ILIB\_FootprintSearchItem](../interfaces/ILIB_FootprintSearchItem.md)<!-- -->&gt;&gt;

List of searched footprint properties

### updatedocumentsource

# LIB\_Footprint.updateDocumentSource() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Update the document source code of the footprint

## Signature

```typescript
function updateDocumentSource(
	footprintUuid: string,
	libraryUuid: string,
	documentSource: string,
): Promise<boolean | undefined>;
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

footprintUuid

</td><td>

string

</td><td>

Footprint UUID

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

Library UUID, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
<tr><td>

documentSource

</td><td>

string

</td><td>

Document source code

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean \| undefined&gt;

Whether the update is successful

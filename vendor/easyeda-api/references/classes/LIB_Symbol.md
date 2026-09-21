# LIB\_Symbol class

Comprehensive library / symbol class

## Signature

```typescript
class LIB_Symbol
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

[copy(symbolUuid, libraryUuid, targetLibraryUuid, targetClassification, newSymbolName)](./LIB_Symbol.md)

</td><td>

</td><td>

**_(BETA)_** Copy Symbol

</td></tr>
<tr><td>

[create(libraryUuid, symbolName, classification, symbolType, description, otherProperty)](./LIB_Symbol.md)

</td><td>

</td><td>

**_(BETA)_** Create Symbol

</td></tr>
<tr><td>

[delete(symbolUuid, libraryUuid)](./LIB_Symbol.md)

</td><td>

</td><td>

**_(BETA)_** Delete Symbol

</td></tr>
<tr><td>

[get(symbolUuid, libraryUuid)](./LIB_Symbol.md)

</td><td>

</td><td>

**_(BETA)_** Get all properties of the symbol

</td></tr>
<tr><td>

[getRenderImage(source)](./LIB_Symbol.md)

</td><td>

</td><td>

**_(BETA)_** Get the symbol render image

</td></tr>
<tr><td>

[modify(symbolUuid, libraryUuid, symbolName, classification, description, otherProperty)](./LIB_Symbol.md)

</td><td>

</td><td>

**_(BETA)_** Modify Symbol

</td></tr>
<tr><td>

[openInEditor(symbolUuid, libraryUuid, splitScreenId)](./LIB_Symbol.md)

</td><td>

</td><td>

**_(BETA)_** Open in the editor document

</td></tr>
<tr><td>

[search(key, libraryUuid, classification, symbolType, itemsOfPage, page)](./LIB_Symbol.md)

</td><td>

</td><td>

**_(BETA)_** Search symbol

</td></tr>
<tr><td>

[searchByProperties(properties, libraryUuid)](./LIB_Symbol.md)

</td><td>

</td><td>

**_(BETA)_** Search symbols precisely by properties

</td></tr>
<tr><td>

[updateDocumentSource(symbolUuid, libraryUuid, documentSource)](./LIB_Symbol.md)

</td><td>

</td><td>

**_(BETA)_** Update the document source code of the symbol

</td></tr>
</tbody></table>

---

## 方法详情

### copy

# LIB\_Symbol.copy() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Copy Symbol

## Signature

```typescript
function copy(
	symbolUuid: string,
	libraryUuid: string,
	targetLibraryUuid: string,
	targetClassification?: ILIB_ClassificationIndex | Array<string>,
	newSymbolName?: string,
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

symbolUuid

</td><td>

string

</td><td>

Symbol UUID

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

newSymbolName

</td><td>

string

</td><td>

_(Optional)_ New symbol name. If a symbol with the same name exists in the target library, the copy will fail

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

UUID of the new symbol in the target library

### create

# LIB\_Symbol.create() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create Symbol

## Signature

```typescript
function create(
	libraryUuid: string,
	symbolName: string,
	classification?: ILIB_ClassificationIndex | Array<string>,
	symbolType?: ELIB_SymbolType,
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

symbolName

</td><td>

string

</td><td>

Symbol name

</td></tr>
<tr><td>

classification

</td><td>

[ILIB\_ClassificationIndex](../interfaces/ILIB_ClassificationIndex.md) \| Array&lt;string&gt;

</td><td>

_(Optional)_ Classification

</td></tr>
<tr><td>

symbolType

</td><td>

[ELIB\_SymbolType](../enums/ELIB_SymbolType.md)

</td><td>

_(Optional)_ Symbol type

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

Symbol UUID

### delete

# LIB\_Symbol.delete() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete Symbol

## Signature

```typescript
function delete(symbolUuid: string, libraryUuid: string): Promise<boolean>;
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

symbolUuid

</td><td>

string

</td><td>

Symbol UUID

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

# LIB\_Symbol.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all properties of the symbol

## Signature

```typescript
function get(symbolUuid: string, libraryUuid?: string): Promise<ILIB_SymbolItem | undefined>;
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

symbolUuid

</td><td>

string

</td><td>

Symbol UUID

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

Promise&lt;[ILIB\_SymbolItem](../interfaces/ILIB_SymbolItem.md) \| undefined&gt;

Symbol property

### getrenderimage

# LIB\_Symbol.getRenderImage() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the symbol render image

## Signature

```typescript
function getRenderImage(source: {
	symbolUuid: string;
	libraryUuid: string;
	subPartName?: string;
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

\{ symbolUuid: string; libraryUuid: string; subPartName?: string \}

</td><td>

</td></tr>
</tbody></table>

## Returns

Promise&lt;Blob \| undefined&gt;

Symbol render image

### modify

# LIB\_Symbol.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Symbol

## Signature

```typescript
function modify(
	symbolUuid: string,
	libraryUuid: string,
	symbolName?: string,
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

symbolUuid

</td><td>

string

</td><td>

Symbol UUID

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

Library UUID, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
<tr><td>

symbolName

</td><td>

string

</td><td>

_(Optional)_ Symbol name

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

# LIB\_Symbol.openInEditor() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Open in the editor document

## Signature

```typescript
function openInEditor(
	symbolUuid: string,
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

symbolUuid

</td><td>

string

</td><td>

Symbol UUID

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

# LIB\_Symbol.search() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Search symbol

## Signature

```typescript
function search(
	key: string,
	libraryUuid?: string,
	classification?: ILIB_ClassificationIndex | Array<string>,
	symbolType?: ELIB_SymbolType,
	itemsOfPage?: number,
	page?: number,
): Promise<Array<ILIB_SymbolSearchItem>>;
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

symbolType

</td><td>

[ELIB\_SymbolType](../enums/ELIB_SymbolType.md)

</td><td>

_(Optional)_ Symbol type, defaults to all

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

Promise&lt;Array&lt;[ILIB\_SymbolSearchItem](../interfaces/ILIB_SymbolSearchItem.md)<!-- -->&gt;&gt;

List of searched symbol properties

### searchbyproperties

# LIB\_Symbol.searchByProperties() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Search symbols precisely by properties

## Signature

```typescript
function searchByProperties(
	properties: ILIB_SymbolPropertiesForSearch,
	libraryUuid?: string,
): Promise<Array<ILIB_SymbolSearchItem>>;
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

[ILIB\_SymbolPropertiesForSearch](../interfaces/ILIB_SymbolPropertiesForSearch.md)

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

Promise&lt;Array&lt;[ILIB\_SymbolSearchItem](../interfaces/ILIB_SymbolSearchItem.md)<!-- -->&gt;&gt;

List of searched symbol properties

### updatedocumentsource

# LIB\_Symbol.updateDocumentSource() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Update the document source code of the symbol

## Signature

```typescript
function updateDocumentSource(
	symbolUuid: string,
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

symbolUuid

</td><td>

string

</td><td>

Symbol UUID

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

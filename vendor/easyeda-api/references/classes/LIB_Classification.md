# LIB\_Classification class

Comprehensive library / library classification index class

## Signature

```typescript
class LIB_Classification
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

[createPrimary(libraryUuid, libraryType, primaryClassificationName)](./LIB_Classification.md)

</td><td>

</td><td>

**_(BETA)_** Create a primary classification

</td></tr>
<tr><td>

[createSecondary(libraryUuid, libraryType, primaryClassificationUuid, secondaryClassificationName)](./LIB_Classification.md)

</td><td>

</td><td>

**_(BETA)_** Create a secondary classification

</td></tr>
<tr><td>

[deleteByIndex(classificationIndex)](./LIB_Classification.md)

</td><td>

</td><td>

**_(BETA)_** Delete the classification at the specified index

</td></tr>
<tr><td>

[deleteByUuid(libraryUuid, classificationUuid)](./LIB_Classification.md)

</td><td>

</td><td>

**_(BETA)_** Delete the classification with the specified UUID

</td></tr>
<tr><td>

[getAllClassificationTree(libraryUuid, libraryType)](./LIB_Classification.md)

</td><td>

</td><td>

**_(BETA)_** Get the tree composed of all classification information

</td></tr>
<tr><td>

[getIndexByName(libraryUuid, libraryType, primaryClassificationName, secondaryClassificationName)](./LIB_Classification.md)

</td><td>

</td><td>

**_(BETA)_** Get the classification index of the classification with the specified name

</td></tr>
<tr><td>

[getNameByIndex(classificationIndex)](./LIB_Classification.md)

</td><td>

</td><td>

**_(BETA)_** Get the name of the classification at the specified index

</td></tr>
<tr><td>

[getNameByUuid(libraryUuid, libraryType, primaryClassificationUuid, secondaryClassificationUuid)](./LIB_Classification.md)

</td><td>

</td><td>

**_(BETA)_** Get the name of the classification with the specified UUID

</td></tr>
</tbody></table>

---

## 方法详情

### createprimary

# LIB\_Classification.createPrimary() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

> Warning: This API is now obsolete.
>
> since EDA v3.2; dropped EDA v3.3

Create a primary classification

## Signature

```typescript
function createPrimary(
	libraryUuid: string,
	libraryType: ELIB_LibraryType,
	primaryClassificationName: string,
): Promise<ILIB_ClassificationIndex | undefined>;
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

Library UUID

</td></tr>
<tr><td>

libraryType

</td><td>

[ELIB\_LibraryType](../enums/ELIB_LibraryType.md)

</td><td>

Library type

</td></tr>
<tr><td>

primaryClassificationName

</td><td>

string

</td><td>

Primary classification name

</td></tr>
</tbody></table>

## Returns

Promise&lt;[ILIB\_ClassificationIndex](../interfaces/ILIB_ClassificationIndex.md) \| undefined&gt;

Classification index

### createsecondary

# LIB\_Classification.createSecondary() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

> Warning: This API is now obsolete.
>
> since EDA v3.2; dropped EDA v3.3

Create a secondary classification

## Signature

```typescript
function createSecondary(
	libraryUuid: string,
	libraryType: ELIB_LibraryType,
	primaryClassificationUuid: string,
	secondaryClassificationName: string,
): Promise<ILIB_ClassificationIndex | undefined>;
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

Library UUID

</td></tr>
<tr><td>

libraryType

</td><td>

[ELIB\_LibraryType](../enums/ELIB_LibraryType.md)

</td><td>

Library type

</td></tr>
<tr><td>

primaryClassificationUuid

</td><td>

string

</td><td>

Primary classification UUID

</td></tr>
<tr><td>

secondaryClassificationName

</td><td>

string

</td><td>

Secondary classification name

</td></tr>
</tbody></table>

## Returns

Promise&lt;[ILIB\_ClassificationIndex](../interfaces/ILIB_ClassificationIndex.md) \| undefined&gt;

Classification index

### deletebyindex

# LIB\_Classification.deleteByIndex() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

> Warning: This API is now obsolete.
>
> since EDA v3.2; dropped EDA v3.3

Delete the classification at the specified index

## Signature

```typescript
function deleteByIndex(classificationIndex: ILIB_ClassificationIndex): Promise<boolean>;
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

classificationIndex

</td><td>

[ILIB\_ClassificationIndex](../interfaces/ILIB_ClassificationIndex.md)

</td><td>

Classification index

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### deletebyuuid

# LIB\_Classification.deleteByUuid() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

> Warning: This API is now obsolete.
>
> since EDA v3.2; dropped EDA v3.3

Delete the classification with the specified UUID

## Signature

```typescript
function deleteByUuid(libraryUuid: string, classificationUuid: string): Promise<boolean>;
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

Library UUID

</td></tr>
<tr><td>

classificationUuid

</td><td>

string

</td><td>

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### getallclassificationtree

# LIB\_Classification.getAllClassificationTree() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

> Warning: This API is now obsolete.
>
> since EDA v3.2; dropped EDA v3.3

Get the tree composed of all classification information

## Signature

```typescript
function getAllClassificationTree(
	libraryUuid: string,
	libraryType: ELIB_LibraryType,
): Promise<
	Array<{
		name: string;
		uuid: string;
		children?: Array<{ name: string; uuid: string }> | undefined;
	}>
>;
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

Library UUID

</td></tr>
<tr><td>

libraryType

</td><td>

[ELIB\_LibraryType](../enums/ELIB_LibraryType.md)

</td><td>

Library type

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;{ name: string; uuid: string; children?: Array&lt;{ name: string; uuid: string }&gt; \| undefined }&gt;&gt;

Tree structure data composed of classification information

### getindexbyname

# LIB\_Classification.getIndexByName() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

> Warning: This API is now obsolete.
>
> since EDA v3.2; dropped EDA v3.3

Get the classification index of the classification with the specified name

## Signature

```typescript
function getIndexByName(
	libraryUuid: string,
	libraryType: ELIB_LibraryType,
	primaryClassificationName: string,
	secondaryClassificationName?: string,
): Promise<ILIB_ClassificationIndex | undefined>;
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

Library UUID

</td></tr>
<tr><td>

libraryType

</td><td>

[ELIB\_LibraryType](../enums/ELIB_LibraryType.md)

</td><td>

Library type

</td></tr>
<tr><td>

primaryClassificationName

</td><td>

string

</td><td>

Primary classification name

</td></tr>
<tr><td>

secondaryClassificationName

</td><td>

string

</td><td>

_(Optional)_ Secondary classification name

</td></tr>
</tbody></table>

## Returns

Promise&lt;[ILIB\_ClassificationIndex](../interfaces/ILIB_ClassificationIndex.md) \| undefined&gt;

Classification index

## Remarks

The classification index contains the UUID of the classification. For details, refer to [ILIB\_ClassificationIndex](../interfaces/ILIB_ClassificationIndex.md)

### getnamebyindex

# LIB\_Classification.getNameByIndex() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

> Warning: This API is now obsolete.
>
> since EDA v3.2; dropped EDA v3.3

Get the name of the classification at the specified index

## Signature

```typescript
function getNameByIndex(
	classificationIndex: ILIB_ClassificationIndex,
): Promise<
	| { primaryClassificationName: string; secondaryClassificationName?: string | undefined }
	| undefined
>;
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

classificationIndex

</td><td>

[ILIB\_ClassificationIndex](../interfaces/ILIB_ClassificationIndex.md)

</td><td>

Classification index

</td></tr>
</tbody></table>

## Returns

Promise&lt;{ primaryClassificationName: string; secondaryClassificationName?: string \| undefined } \| undefined&gt;

Name of the two-level classification

### getnamebyuuid

# LIB\_Classification.getNameByUuid() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

> Warning: This API is now obsolete.
>
> since EDA v3.2; dropped EDA v3.3

Get the name of the classification with the specified UUID

## Signature

```typescript
function getNameByUuid(
	libraryUuid: string,
	libraryType: ELIB_LibraryType,
	primaryClassificationUuid: string,
	secondaryClassificationUuid?: string,
): Promise<
	| { primaryClassificationName: string; secondaryClassificationName?: string | undefined }
	| undefined
>;
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

Library UUID

</td></tr>
<tr><td>

libraryType

</td><td>

[ELIB\_LibraryType](../enums/ELIB_LibraryType.md)

</td><td>

Library type

</td></tr>
<tr><td>

primaryClassificationUuid

</td><td>

string

</td><td>

Primary classification UUID

</td></tr>
<tr><td>

secondaryClassificationUuid

</td><td>

string

</td><td>

_(Optional)_ Secondary classification UUID. If not specified, only the primary classification information is obtained

</td></tr>
</tbody></table>

## Returns

Promise&lt;{ primaryClassificationName: string; secondaryClassificationName?: string \| undefined } \| undefined&gt;

Name of the two-level classification

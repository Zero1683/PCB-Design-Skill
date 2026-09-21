# LIB\_Device class

Comprehensive library / device class

## Signature

```typescript
class LIB_Device
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

[copy(deviceUuid, libraryUuid, targetLibraryUuid, targetClassification, newDeviceName)](./LIB_Device.md)

</td><td>

</td><td>

**_(BETA)_** Copy Device

</td></tr>
<tr><td>

[create(libraryUuid, deviceName, classification, association, description, property)](./LIB_Device.md)

</td><td>

</td><td>

**_(BETA)_** Create Device

</td></tr>
<tr><td>

[delete(deviceUuid, libraryUuid)](./LIB_Device.md)

</td><td>

</td><td>

**_(BETA)_** Delete Device

</td></tr>
<tr><td>

[get(deviceUuid, libraryUuid)](./LIB_Device.md)

</td><td>

</td><td>

**_(BETA)_** Get all properties of the device

</td></tr>
<tr><td>

[getByLcscIds(lcscIds, libraryUuid, allowMultiMatch)](./LIB_Device.md)

</td><td>

</td><td>

**_(BETA)_** Get a device using an LCSC C number

</td></tr>
<tr><td>

[getByLcscIds(lcscIds, libraryUuid, allowMultiMatch)](./LIB_Device.md)

</td><td>

</td><td>

**_(BETA)_** Batch get devices using LCSC C numbers

</td></tr>
<tr><td>

[modify(deviceUuid, libraryUuid, deviceName, classification, association, description, property)](./LIB_Device.md)

</td><td>

</td><td>

**_(BETA)_** Modify Device

</td></tr>
<tr><td>

[search(key, libraryUuid, classification, symbolType, itemsOfPage, page)](./LIB_Device.md)

</td><td>

</td><td>

**_(BETA)_** Search device

</td></tr>
<tr><td>

[searchByProperties(properties, libraryUuid, classification, symbolType, itemsOfPage, page)](./LIB_Device.md)

</td><td>

</td><td>

**_(BETA)_** Search devices precisely by properties

</td></tr>
</tbody></table>

---

## 方法详情

### copy

# LIB\_Device.copy() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Copy Device

## Signature

```typescript
function copy(
	deviceUuid: string,
	libraryUuid: string,
	targetLibraryUuid: string,
	targetClassification?: ILIB_ClassificationIndex | Array<string>,
	newDeviceName?: string,
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

deviceUuid

</td><td>

string

</td><td>

Device UUID

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

newDeviceName

</td><td>

string

</td><td>

_(Optional)_ New device name. If a device with the same name exists in the target library, the copy will fail

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

UUID of the new device in the target library

### create

# LIB\_Device.create() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create Device

## Signature

```typescript
function create(
	libraryUuid: string,
	deviceName: string,
	classification?: ILIB_ClassificationIndex | Array<string>,
	association?: {
		symbolType?: ELIB_SymbolType;
		symbolUuid?: string;
		symbol?: { uuid: string; libraryUuid: string };
		footprintUuid?: string;
		footprint?: { uuid: string; libraryUuid: string };
		model3D?: { uuid: string; libraryUuid: string };
		imageData?: File | Blob;
	},
	description?: string,
	property?: ILIB_DeviceExtendPropertyItem,
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

deviceName

</td><td>

string

</td><td>

Device name

</td></tr>
<tr><td>

classification

</td><td>

[ILIB\_ClassificationIndex](../interfaces/ILIB_ClassificationIndex.md) \| Array&lt;string&gt;

</td><td>

_(Optional)_ Classification

</td></tr>
<tr><td>

association

</td><td>

{ symbolType?: [ELIB\_SymbolType](../enums/ELIB_SymbolType.md)<!-- -->; symbolUuid?: string; symbol?: { uuid: string; libraryUuid: string }; footprintUuid?: string; footprint?: { uuid: string; libraryUuid: string }; model3D?: { uuid: string; libraryUuid: string }; imageData?: File \| Blob }

</td><td>

_(Optional)_ Associate a symbol, footprint, and image. Specifying `symbolType` creates a new symbol; if no new symbol is needed, `symbolType` does not need to be specified. However, note that if no new symbol is created and no symbol association information is specified, the device cannot be created

</td></tr>
<tr><td>

description

</td><td>

string

</td><td>

_(Optional)_ Description

</td></tr>
<tr><td>

property

</td><td>

[ILIB\_DeviceExtendPropertyItem](../interfaces/ILIB_DeviceExtendPropertyItem.md)

</td><td>

_(Optional)_ Other property, only `designator`<!-- -->, `addIntoBom`<!-- -->, `addIntoPcb` exists default value

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

Device UUID

### delete

# LIB\_Device.delete() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete Device

## Signature

```typescript
function delete(deviceUuid: string, libraryUuid: string): Promise<boolean>;
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

deviceUuid

</td><td>

string

</td><td>

Device UUID

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

# LIB\_Device.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all properties of the device

## Signature

```typescript
function get(deviceUuid: string, libraryUuid?: string): Promise<ILIB_DeviceItem | undefined>;
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

deviceUuid

</td><td>

string

</td><td>

Device UUID

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

Promise&lt;[ILIB\_DeviceItem](../interfaces/ILIB_DeviceItem.md) \| undefined&gt;

Device property

### getbylcscids

# LIB\_Device.getByLcscIds() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get a device using an LCSC C number

## Signature

```typescript
function getByLcscIds<T extends boolean>(
	lcscIds: string,
	libraryUuid?: string,
	allowMultiMatch?: T,
): Promise<T extends true ? ILIB_DeviceSearchItem | undefined : Array<ILIB_DeviceSearchItem>>;
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

lcscIds

</td><td>

string

</td><td>

LCSC C number

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

_(Optional)_ Library UUID, default is system library, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
<tr><td>

allowMultiMatch

</td><td>

T

</td><td>

_(Optional)_ Whether a single LCSC C number is allowed to match multiple results

</td></tr>
</tbody></table>

## Returns

Promise&lt;T extends true ? [ILIB\_DeviceSearchItem](../interfaces/ILIB_DeviceSearchItem.md) \| undefined : Array&lt;[ILIB\_DeviceSearchItem](../interfaces/ILIB_DeviceSearchItem.md)<!-- -->&gt;&gt;

Searched device properties

## Remarks

By default, if multiple devices with the same C number are matched in the same library, only the first result will be returned;

If you want to return multiple results, set `allowMultiMatch` to `true`<!-- -->;

This API is temporarily unavailable in the private deployment environment

### getbylcscids_1

# LIB\_Device.getByLcscIds() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Batch get devices using LCSC C numbers

## Signature

```typescript
function getByLcscIds(
	lcscIds: Array<string>,
	libraryUuid?: string,
	allowMultiMatch?: boolean,
): Promise<Array<ILIB_DeviceSearchItem>>;
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

lcscIds

</td><td>

Array&lt;string&gt;

</td><td>

Array of LCSC C numbers

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

_(Optional)_ Library UUID, default is system library, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
<tr><td>

allowMultiMatch

</td><td>

boolean

</td><td>

_(Optional)_ Whether a single LCSC C number is allowed to match multiple results

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[ILIB\_DeviceSearchItem](../interfaces/ILIB_DeviceSearchItem.md)<!-- -->&gt;&gt;

List of searched device properties

## Remarks

By default, if multiple devices with the same C number are matched in the same library, only the first result will be returned;

If you want to return multiple results, set `allowMultiMatch` to `true`<!-- -->;

This API is temporarily unavailable in the private deployment environment

### modify

# LIB\_Device.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Device

## Signature

```typescript
function modify(
	deviceUuid: string,
	libraryUuid: string,
	deviceName?: string,
	classification?: ILIB_ClassificationIndex | Array<string> | null,
	association?: {
		symbolUuid?: string;
		symbol?: { uuid: string; libraryUuid: string };
		footprintUuid?: string | null;
		footprint?: { uuid: string; libraryUuid: string } | null;
		model3D?: { uuid: string; libraryUuid: string } | null;
		imageData?: File | Blob | null;
	},
	description?: string | null,
	property?: {
		name?: string | null;
		designator?: string;
		addIntoBom?: boolean;
		addIntoPcb?: boolean;
		net?: string;
		manufacturer?: string | null;
		manufacturerId?: string | null;
		supplier?: string | null;
		supplierId?: string | null;
		otherProperty?: { [key: string]: boolean | number | string | undefined | null };
	},
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

deviceUuid

</td><td>

string

</td><td>

Device UUID

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

Library UUID, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
<tr><td>

deviceName

</td><td>

string

</td><td>

_(Optional)_ Device name

</td></tr>
<tr><td>

classification

</td><td>

[ILIB\_ClassificationIndex](../interfaces/ILIB_ClassificationIndex.md) \| Array&lt;string&gt; \| null

</td><td>

_(Optional)_ Classification

</td></tr>
<tr><td>

association

</td><td>

\{ symbolUuid?: string; symbol?: \{ uuid: string; libraryUuid: string \}; footprintUuid?: string \| null; footprint?: \{ uuid: string; libraryUuid: string \} \| null; model3D?: \{ uuid: string; libraryUuid: string \} \| null; imageData?: File \| Blob \| null \}

</td><td>

_(Optional)_ Associated symbol, footprint, image

</td></tr>
<tr><td>

description

</td><td>

string \| null

</td><td>

_(Optional)_ Description

</td></tr>
<tr><td>

property

</td><td>

\{ name?: string \| null; designator?: string; addIntoBom?: boolean; addIntoPcb?: boolean; net?: string; manufacturer?: string \| null; manufacturerId?: string \| null; supplier?: string \| null; supplierId?: string \| null; otherProperty?: \{ \[key: string\]: boolean \| number \| string \| undefined \| null \} \}

</td><td>

_(Optional)_ Other property

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

If you want to clear certain properties, set their values to `null`

### search

# LIB\_Device.search() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Search device

## Signature

```typescript
function search(
	key: string,
	libraryUuid?: string,
	classification?: ILIB_ClassificationIndex | Array<string>,
	symbolType?: ELIB_SymbolType,
	itemsOfPage?: number,
	page?: number,
): Promise<Array<ILIB_DeviceSearchItem>>;
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

Promise&lt;Array&lt;[ILIB\_DeviceSearchItem](../interfaces/ILIB_DeviceSearchItem.md)<!-- -->&gt;&gt;

List of searched device properties

### searchbyproperties

# LIB\_Device.searchByProperties() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Search devices precisely by properties

## Signature

```typescript
function searchByProperties(
	properties: ILIB_DevicePropertiesForSearch,
	libraryUuid?: string,
	classification?: Array<string>,
	symbolType?: ELIB_SymbolType,
	itemsOfPage?: number,
	page?: number,
): Promise<Array<ILIB_DeviceSearchItem>>;
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

[ILIB\_DevicePropertiesForSearch](../interfaces/ILIB_DevicePropertiesForSearch.md)

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
<tr><td>

classification

</td><td>

Array&lt;string&gt;

</td><td>

_(Optional)_ Classification, defaults to all ADD since EDA v4

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

Promise&lt;Array&lt;[ILIB\_DeviceSearchItem](../interfaces/ILIB_DeviceSearchItem.md)<!-- -->&gt;&gt;

List of searched device properties

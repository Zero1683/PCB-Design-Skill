# LIB\_LibrariesList class

Comprehensive library / library list class

## Signature

```typescript
class LIB_LibrariesList
```

## Remarks

All APIs here are based on the current workspace environment of the editor. To switch to another workspace, use the [DMT\_Workspace.toggleToWorkspace()](./DMT_Workspace.md) API

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[getAllLibrariesList()](./LIB_LibrariesList.md)

</td><td>

</td><td>

Get the list of all libraries

</td></tr>
<tr><td>

[getFavoriteLibraryUuid()](./LIB_LibrariesList.md)

</td><td>

</td><td>

Get the UUID of the favorite library

</td></tr>
<tr><td>

[getPersonalLibraryUuid()](./LIB_LibrariesList.md)

</td><td>

</td><td>

Get the UUID of the personal library

</td></tr>
<tr><td>

[getProjectLibraryUuid()](./LIB_LibrariesList.md)

</td><td>

</td><td>

Get the UUID of the project library

</td></tr>
<tr><td>

[getSystemLibraryUuid()](./LIB_LibrariesList.md)

</td><td>

</td><td>

Get the UUID of the system library

</td></tr>
<tr><td>

[registerExtendLibrary(title, libraryFunctions)](./LIB_LibrariesList.md)

</td><td>

</td><td>

**_(BETA)_** Register an external library

</td></tr>
</tbody></table>

---

## 方法详情

### getalllibrarieslist

# LIB\_LibrariesList.getAllLibrariesList() method

Get the list of all libraries

## Signature

```typescript
function getAllLibrariesList(): Promise<Array<ILIB_LibraryInfo>>;
```

## Returns

Promise&lt;Array&lt;[ILIB\_LibraryInfo](../interfaces/ILIB_LibraryInfo.md)<!-- -->&gt;&gt;

Library information list

## Remarks

This does not get the information of the system library, personal library, project library, or favorite library. To get their information, use the [getSystemLibraryUuid](./LIB_LibrariesList.md)<!-- -->, [getPersonalLibraryUuid](./LIB_LibrariesList.md)<!-- -->, [getProjectLibraryUuid](./LIB_LibrariesList.md)<!-- -->, and [getFavoriteLibraryUuid](./LIB_LibrariesList.md) APIs

### getfavoritelibraryuuid

# LIB\_LibrariesList.getFavoriteLibraryUuid() method

Get the UUID of the favorite library

## Signature

```typescript
function getFavoriteLibraryUuid(): Promise<string | undefined>;
```

## Returns

Promise&lt;string \| undefined&gt;

UUID of the favorite library

## Remarks

It will get the UUID of the favorite library under the current editor workspace

### getpersonallibraryuuid

# LIB\_LibrariesList.getPersonalLibraryUuid() method

Get the UUID of the personal library

## Signature

```typescript
function getPersonalLibraryUuid(): Promise<string | undefined>;
```

## Returns

Promise&lt;string \| undefined&gt;

UUID of the personal library

## Remarks

It will get the UUID of the personal library under the current editor workspace. In the private deployment environment, the personal library does not exist, and this API will always return `undefined`

### getprojectlibraryuuid

# LIB\_LibrariesList.getProjectLibraryUuid() method

Get the UUID of the project library

## Signature

```typescript
function getProjectLibraryUuid(): Promise<string | undefined>;
```

## Returns

Promise&lt;string \| undefined&gt;

UUID of the project library

## Remarks

Calling it without an open project will return `undefined`

### getsystemlibraryuuid

# LIB\_LibrariesList.getSystemLibraryUuid() method

Get the UUID of the system library

## Signature

```typescript
function getSystemLibraryUuid(): Promise<string | undefined>;
```

## Returns

Promise&lt;string \| undefined&gt;

UUID of the system library

### registerextendlibrary

# LIB\_LibrariesList.registerExtendLibrary() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Register an external library

## Signature

```typescript
function registerExtendLibrary(
	title: string,
	libraryFunctions: {
		device?: ILIB_ExtendLibraryDeviceFunctions;
		symbol?: ILIB_ExtendLibrarySymbolFunctions;
		footprint?: ILIB_ExtendLibraryFootprintFunctions;
		cbb?: ILIB_ExtendLibraryCbbFunctions;
		model3d?: ILIB_ExtendLibrary3DModelFunctions;
	},
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

title

</td><td>

string

</td><td>

Title

</td></tr>
<tr><td>

libraryFunctions

</td><td>

{ device?: [ILIB\_ExtendLibraryDeviceFunctions](../interfaces/ILIB_ExtendLibraryDeviceFunctions.md)<!-- -->; symbol?: [ILIB\_ExtendLibrarySymbolFunctions](../interfaces/ILIB_ExtendLibrarySymbolFunctions.md)<!-- -->; footprint?: [ILIB\_ExtendLibraryFootprintFunctions](../interfaces/ILIB_ExtendLibraryFootprintFunctions.md)<!-- -->; cbb?: [ILIB\_ExtendLibraryCbbFunctions](../interfaces/ILIB_ExtendLibraryCbbFunctions.md)<!-- -->; model3d?: [ILIB\_ExtendLibrary3DModelFunctions](../interfaces/ILIB_ExtendLibrary3DModelFunctions.md) }

</td><td>

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

Library UUID

## Remarks

Note: This API is only valid for extensions. Calling it in a standalone script environment will always `throw Error`

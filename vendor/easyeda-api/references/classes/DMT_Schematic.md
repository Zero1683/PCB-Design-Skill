# DMT\_Schematic class

Document tree / Schematic management class

## Signature

```typescript
class DMT_Schematic
```

## Remarks

Operations related to schematic management in the currently open project

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[copySchematic(schematicUuid, boardName)](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Copy Schematic

</td></tr>
<tr><td>

[copySchematicPage(schematicPageUuid, schematicUuid)](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Copy Schematic sheet

</td></tr>
<tr><td>

[createSchematic(boardName)](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Create Schematic

</td></tr>
<tr><td>

[createSchematicPage(schematicUuid)](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Create Schematic sheet

</td></tr>
<tr><td>

[deleteSchematic(schematicUuid)](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Delete Schematic

</td></tr>
<tr><td>

[deleteSchematicPage(schematicPageUuid)](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Delete Schematic sheet

</td></tr>
<tr><td>

[getAllSchematicPagesInfo()](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Get all in the project schematic sheet detailed properties of

</td></tr>
<tr><td>

[getAllSchematicsInfo()](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Get all in the project schematic detailed properties of

</td></tr>
<tr><td>

[getCurrentSchematicAllSchematicPagesInfo()](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Get the detailed properties of all schematic sheets in the current schematic

</td></tr>
<tr><td>

[getCurrentSchematicInfo()](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Get detailed properties of Current schematic

</td></tr>
<tr><td>

[getCurrentSchematicPageInfo()](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Get detailed properties of Current schematic sheet

</td></tr>
<tr><td>

[getSchematicInfo(schematicUuid)](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Get detailed properties of Schematic

</td></tr>
<tr><td>

[getSchematicPageInfo(schematicPageUuid)](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Get detailed properties of Schematic sheet

</td></tr>
<tr><td>

[modifySchematicName(schematicUuid, schematicName)](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Modify Schematic name

</td></tr>
<tr><td>

[modifySchematicPageName(schematicPageUuid, schematicPageName)](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Modify Schematic sheet name

</td></tr>
<tr><td>

[modifySchematicPageTitleBlock(showTitleBlock, titleBlockData)](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Modify the title block of a schematic sheet

</td></tr>
<tr><td>

[reorderSchematicPages(schematicUuid, schematicPageItemsArray)](./DMT_Schematic.md)

</td><td>

</td><td>

**_(BETA)_** Reorder schematic sheets

</td></tr>
</tbody></table>

---

## 方法详情

### copyschematic

# DMT\_Schematic.copySchematic() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Copy Schematic

## Signature

```typescript
function copySchematic(schematicUuid: string, boardName?: string): Promise<string | undefined>;
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

schematicUuid

</td><td>

string

</td><td>

Source schematic UUID

</td></tr>
<tr><td>

boardName

</td><td>

string

</td><td>

_(Optional)_ Name of the board the new schematic belongs to. If not specified, it is a free schematic

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

New schematic UUID. If it is `undefined`<!-- -->, the copy failed

## Remarks

If the schematic is already associated with a reuse block (a reuse block symbol with the same name exists in the project library), copying the schematic will also create a new reuse block symbol

### copyschematicpage

# DMT\_Schematic.copySchematicPage() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Copy Schematic sheet

## Signature

```typescript
function copySchematicPage(
	schematicPageUuid: string,
	schematicUuid?: string,
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

schematicPageUuid

</td><td>

string

</td><td>

Source schematic sheet UUID

</td></tr>
<tr><td>

schematicUuid

</td><td>

string

</td><td>

_(Optional)_ Target schematic UUID. If not specified, it is the current schematic

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

New schematic sheet UUID. If it is `undefined`<!-- -->, the copy failed

### createschematic

# DMT\_Schematic.createSchematic() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create Schematic

## Signature

```typescript
function createSchematic(boardName?: string): Promise<string | undefined>;
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

boardName

</td><td>

string

</td><td>

_(Optional)_ Name of the board it belongs to. If not specified, it is a free schematic

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

Schematic UUID, if it is `undefined` creation fails

### createschematicpage

# DMT\_Schematic.createSchematicPage() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create Schematic sheet

## Signature

```typescript
function createSchematicPage(schematicUuid: string): Promise<string | undefined>;
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

schematicUuid

</td><td>

string

</td><td>

UUID of the schematic it belongs to

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

Schematic sheet UUID, if it is `undefined` creation fails

### deleteschematic

# DMT\_Schematic.deleteSchematic() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete Schematic

## Signature

```typescript
function deleteSchematic(schematicUuid: string): Promise<boolean>;
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

schematicUuid

</td><td>

string

</td><td>

Schematic UUID

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

If the schematic is already associated with a reuse block (a reuse block symbol with the same name exists in the project library), deleting the schematic will also delete the associated PCB and reuse block symbol. If the reuse block symbol cannot be deleted, it will be skipped

### deleteschematicpage

# DMT\_Schematic.deleteSchematicPage() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete Schematic sheet

## Signature

```typescript
function deleteSchematicPage(schematicPageUuid: string): Promise<boolean>;
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

schematicPageUuid

</td><td>

string

</td><td>

Schematic sheet UUID

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### getallschematicpagesinfo

# DMT\_Schematic.getAllSchematicPagesInfo() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all in the project schematic sheet detailed properties of

## Signature

```typescript
function getAllSchematicPagesInfo(): Promise<Array<IDMT_SchematicPageItem>>;
```

## Returns

Promise&lt;Array&lt;[IDMT\_SchematicPageItem](../interfaces/IDMT_SchematicPageItem.md)<!-- -->&gt;&gt;

Array of detailed properties of all schematic sheets

### getallschematicsinfo

# DMT\_Schematic.getAllSchematicsInfo() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all in the project schematic detailed properties of

## Signature

```typescript
function getAllSchematicsInfo(): Promise<Array<IDMT_SchematicItem>>;
```

## Returns

Promise&lt;Array&lt;[IDMT\_SchematicItem](../interfaces/IDMT_SchematicItem.md)<!-- -->&gt;&gt;

Array of detailed properties of all schematics

### getcurrentschematicallschematicpagesinfo

# DMT\_Schematic.getCurrentSchematicAllSchematicPagesInfo() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the detailed properties of all schematic sheets in the current schematic

## Signature

```typescript
function getCurrentSchematicAllSchematicPagesInfo(): Promise<Array<IDMT_SchematicPageItem>>;
```

## Returns

Promise&lt;Array&lt;[IDMT\_SchematicPageItem](../interfaces/IDMT_SchematicPageItem.md)<!-- -->&gt;&gt;

Array of detailed properties of all schematic sheets

### getcurrentschematicinfo

# DMT\_Schematic.getCurrentSchematicInfo() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get detailed properties of Current schematic

## Signature

```typescript
function getCurrentSchematicInfo(): Promise<IDMT_SchematicItem | undefined>;
```

## Returns

Promise&lt;[IDMT\_SchematicItem](../interfaces/IDMT_SchematicItem.md) \| undefined&gt;

Schematic detailed properties of; if it is `undefined`<!-- -->, the retrieval failed

## Remarks

It will get the detailed properties of the schematic associated with the currently open schematic sheet that has the last input focus

### getcurrentschematicpageinfo

# DMT\_Schematic.getCurrentSchematicPageInfo() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get detailed properties of Current schematic sheet

## Signature

```typescript
function getCurrentSchematicPageInfo(): Promise<IDMT_SchematicPageItem | undefined>;
```

## Returns

Promise&lt;[IDMT\_SchematicPageItem](../interfaces/IDMT_SchematicPageItem.md) \| undefined&gt;

Schematic sheet detailed properties of; if it is `undefined`<!-- -->, the retrieval failed

## Remarks

It will get the detailed properties of the currently open schematic sheet that has the last input focus

### getschematicinfo

# DMT\_Schematic.getSchematicInfo() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get detailed properties of Schematic

## Signature

```typescript
function getSchematicInfo(schematicUuid: string): Promise<IDMT_SchematicItem | undefined>;
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

schematicUuid

</td><td>

string

</td><td>

Schematic UUID

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IDMT\_SchematicItem](../interfaces/IDMT_SchematicItem.md) \| undefined&gt;

Schematic detailed properties of; if it is `undefined`<!-- -->, the retrieval failed

### getschematicpageinfo

# DMT\_Schematic.getSchematicPageInfo() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get detailed properties of Schematic sheet

## Signature

```typescript
function getSchematicPageInfo(
	schematicPageUuid: string,
): Promise<IDMT_SchematicPageItem | undefined>;
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

schematicPageUuid

</td><td>

string

</td><td>

Schematic sheet UUID

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IDMT\_SchematicPageItem](../interfaces/IDMT_SchematicPageItem.md) \| undefined&gt;

Schematic sheet detailed properties of; if it is `undefined`<!-- -->, the retrieval failed

### modifyschematicname

# DMT\_Schematic.modifySchematicName() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Schematic name

## Signature

```typescript
function modifySchematicName(schematicUuid: string, schematicName: string): Promise<boolean>;
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

schematicUuid

</td><td>

string

</td><td>

Schematic UUID

</td></tr>
<tr><td>

schematicName

</td><td>

string

</td><td>

Schematic name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether Modify Successful

## Remarks

If the schematic is already associated with a reuse block (a reuse block symbol with the same name exists in the project library), modifying the name will also modify the reuse block symbol name and the associated PCB name

### modifyschematicpagename

# DMT\_Schematic.modifySchematicPageName() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Schematic sheet name

## Signature

```typescript
function modifySchematicPageName(
	schematicPageUuid: string,
	schematicPageName: string,
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

schematicPageUuid

</td><td>

string

</td><td>

Schematic sheet UUID

</td></tr>
<tr><td>

schematicPageName

</td><td>

string

</td><td>

Schematic sheet name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether Modify Successful

### modifyschematicpagetitleblock

# DMT\_Schematic.modifySchematicPageTitleBlock() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify the title block of a schematic sheet

## Signature

```typescript
function modifySchematicPageTitleBlock(
	showTitleBlock?: boolean,
	titleBlockData?: { [key: string]: { showTitle?: boolean; showValue?: boolean; value?: any } },
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

showTitleBlock

</td><td>

boolean

</td><td>

_(Optional)_ Whether to show the title block. If undefined, the current state will be kept

</td></tr>
<tr><td>

titleBlockData

</td><td>

\{ \[key: string\]: \{ showTitle?: boolean; showValue?: boolean; value?: any \} \}

</td><td>

_(Optional)_ The title block items to be modified and their modified values

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the modification was successful. If `showTitleBlock` and `titleBlockData` are not passed in, `false` will be returned. Note that if unrecognized title block items exist but the program does not report an error, `true` will be returned because the unrecognized items are ignored

## Remarks

`titleBlockData` only needs to pass in any title block items to be modified as `key`<!-- -->, along with the values to modify them to. Any unrecognized title block items will be ignored, and any unpassed items and values will remain in their default state

### reorderschematicpages

# DMT\_Schematic.reorderSchematicPages() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reorder schematic sheets

## Signature

```typescript
function reorderSchematicPages(
	schematicUuid: string,
	schematicPageItemsArray: Array<IDMT_SchematicPageItem>,
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

schematicUuid

</td><td>

string

</td><td>

The UUID of the schematic associated with the sheets being sorted

</td></tr>
<tr><td>

schematicPageItemsArray

</td><td>

Array&lt;[IDMT\_SchematicPageItem](../interfaces/IDMT_SchematicPageItem.md)<!-- -->&gt;

</td><td>

Array of all schematic sheet properties

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Sorting whether the operation is successful

## Remarks

Here, the array of source schematic sheet properties needs to be obtained through [DMT\_Schematic.getAllSchematicPagesInfo()](./DMT_Schematic.md) or other upstream methods. After sorting the array, pass it in

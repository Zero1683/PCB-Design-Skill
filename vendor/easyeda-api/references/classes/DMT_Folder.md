# DMT\_Folder class

Document tree / Folder class

## Signature

```typescript
class DMT_Folder
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

[createFolder(folderName, teamUuid, parentFolderUuid, description)](./DMT_Folder.md)

</td><td>

</td><td>

**_(BETA)_** Create Folder

</td></tr>
<tr><td>

[deleteFolder(teamUuid, folderUuid)](./DMT_Folder.md)

</td><td>

</td><td>

Delete Folder

</td></tr>
<tr><td>

[getAllFoldersUuid(teamUuid)](./DMT_Folder.md)

</td><td>

</td><td>

Get the UUIDs of all folders

</td></tr>
<tr><td>

[getFolderInfo(teamUuid, folderUuid)](./DMT_Folder.md)

</td><td>

</td><td>

Get Folder detailed properties

</td></tr>
<tr><td>

[modifyFolderDescription(teamUuid, folderUuid, description)](./DMT_Folder.md)

</td><td>

</td><td>

**_(BETA)_** Modify Folder description

</td></tr>
<tr><td>

[modifyFolderName(teamUuid, folderUuid, folderName)](./DMT_Folder.md)

</td><td>

</td><td>

Modify Folder name

</td></tr>
<tr><td>

[moveFolderToFolder(teamUuid, folderUuid, parentFolderUuid)](./DMT_Folder.md)

</td><td>

</td><td>

Move folder

</td></tr>
</tbody></table>

---

## 方法详情

### createfolder

# DMT\_Folder.createFolder() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create Folder

## Signature

```typescript
function createFolder(
	folderName: string,
	teamUuid: string,
	parentFolderUuid?: string,
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

folderName

</td><td>

string

</td><td>

Folder name

</td></tr>
<tr><td>

teamUuid

</td><td>

string

</td><td>

Team UUID

</td></tr>
<tr><td>

parentFolderUuid

</td><td>

string

</td><td>

_(Optional)_ Parent folder UUID. If not specified, it is the root folder

</td></tr>
<tr><td>

description

</td><td>

string

</td><td>

_(Optional)_ Folder description

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

Folder UUID, if it is `undefined` creation fails

### deletefolder

# DMT\_Folder.deleteFolder() method

Delete Folder

## Signature

```typescript
function deleteFolder(teamUuid: string, folderUuid: string): Promise<boolean>;
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

teamUuid

</td><td>

string

</td><td>

Team UUID

</td></tr>
<tr><td>

folderUuid

</td><td>

string

</td><td>

Folder UUID

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### getallfoldersuuid

# DMT\_Folder.getAllFoldersUuid() method

Get the UUIDs of all folders

## Signature

```typescript
function getAllFoldersUuid(teamUuid: string): Promise<Array<string>>;
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

teamUuid

</td><td>

string

</td><td>

Team UUID

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;string&gt;&gt;

Folder UUID array

## Remarks

This API ignores hierarchy information. It will return the UUIDs of folders at all levels and place them in a one-dimensional array

### getfolderinfo

# DMT\_Folder.getFolderInfo() method

Get Folder detailed properties

## Signature

```typescript
function getFolderInfo(teamUuid: string, folderUuid: string): Promise<IDMT_FolderItem | undefined>;
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

teamUuid

</td><td>

string

</td><td>

Team UUID

</td></tr>
<tr><td>

folderUuid

</td><td>

string

</td><td>

Folder UUID

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IDMT\_FolderItem](../interfaces/IDMT_FolderItem.md) \| undefined&gt;

Folder property; if it is `undefined`<!-- -->, the retrieval failed

## Remarks

When [parentFolderUuid](../interfaces/IDMT_FolderItem.md) equals [teamUuid](../interfaces/IDMT_FolderItem.md)<!-- -->, it means the current folder is a first-level folder under the specified team

### modifyfolderdescription

# DMT\_Folder.modifyFolderDescription() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Folder description

## Signature

```typescript
function modifyFolderDescription(
	teamUuid: string,
	folderUuid: string,
	description?: string,
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

teamUuid

</td><td>

string

</td><td>

Team UUID

</td></tr>
<tr><td>

folderUuid

</td><td>

string

</td><td>

Folder UUID

</td></tr>
<tr><td>

description

</td><td>

string

</td><td>

_(Optional)_ Folder description. If it is `undefined`<!-- -->, the existing project description is cleared

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether Modify Successful

## Remarks

Modifying the folder description requires interaction with the workspace system. The modification is delayed and takes effect only after a short wait

### modifyfoldername

# DMT\_Folder.modifyFolderName() method

Modify Folder name

## Signature

```typescript
function modifyFolderName(
	teamUuid: string,
	folderUuid: string,
	folderName: string,
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

teamUuid

</td><td>

string

</td><td>

Team UUID

</td></tr>
<tr><td>

folderUuid

</td><td>

string

</td><td>

Folder UUID

</td></tr>
<tr><td>

folderName

</td><td>

string

</td><td>

Folder name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether Modify Successful

### movefoldertofolder

# DMT\_Folder.moveFolderToFolder() method

Move folder

## Signature

```typescript
function moveFolderToFolder(
	teamUuid: string,
	folderUuid: string,
	parentFolderUuid?: string,
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

teamUuid

</td><td>

string

</td><td>

Team UUID

</td></tr>
<tr><td>

folderUuid

</td><td>

string

</td><td>

Folder UUID

</td></tr>
<tr><td>

parentFolderUuid

</td><td>

string

</td><td>

_(Optional)_ Parent folder UUID. If not specified, it defaults to the root folder

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the move is successful

# DMT\_Board class

Document tree / Board management class

## Signature

```typescript
class DMT_Board
```

## Remarks

Operations related to board management in the currently open project

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[copyBoard(sourceBoardName)](./DMT_Board.md)

</td><td>

</td><td>

Copy Board

</td></tr>
<tr><td>

[createBoard(schematicUuid, pcbUuid)](./DMT_Board.md)

</td><td>

</td><td>

**_(BETA)_** Create Board

</td></tr>
<tr><td>

[deleteBoard(boardName)](./DMT_Board.md)

</td><td>

</td><td>

Delete Board

</td></tr>
<tr><td>

[getAllBoardsInfo()](./DMT_Board.md)

</td><td>

</td><td>

Get all in the project board detailed properties of

</td></tr>
<tr><td>

[getBoardInfo(boardName)](./DMT_Board.md)

</td><td>

</td><td>

Get detailed properties of Board

</td></tr>
<tr><td>

[getCurrentBoardInfo()](./DMT_Board.md)

</td><td>

</td><td>

Get detailed properties of Current board

</td></tr>
<tr><td>

[modifyBoardName(originalBoardName, boardName)](./DMT_Board.md)

</td><td>

</td><td>

Modify Board name

</td></tr>
</tbody></table>

---

## 方法详情

### copyboard

# DMT\_Board.copyBoard() method

Copy Board

## Signature

```typescript
function copyBoard(sourceBoardName: string): Promise<string | undefined>;
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

sourceBoardName

</td><td>

string

</td><td>

Source board name

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

New board name, if it is `undefined` the copy fails

### createboard

# DMT\_Board.createBoard() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create Board

## Signature

```typescript
function createBoard(schematicUuid?: string, pcbUuid?: string): Promise<string | undefined>;
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

_(Optional)_ Associated schematic UUID

</td></tr>
<tr><td>

pcbUuid

</td><td>

string

</td><td>

_(Optional)_ Associated PCB UUID

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

Board name, if it is `undefined` creation fails

### deleteboard

# DMT\_Board.deleteBoard() method

Delete Board

## Signature

```typescript
function deleteBoard(boardName: string): Promise<boolean>;
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

Board name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

If the specified board does not exist, the API will return `false`<!-- -->, indicating that the operation failed

### getallboardsinfo

# DMT\_Board.getAllBoardsInfo() method

Get all in the project board detailed properties of

## Signature

```typescript
function getAllBoardsInfo(): Promise<Array<IDMT_BoardItem>>;
```

## Returns

Promise&lt;Array&lt;[IDMT\_BoardItem](../interfaces/IDMT_BoardItem.md)<!-- -->&gt;&gt;

Array of detailed properties of all Board

### getboardinfo

# DMT\_Board.getBoardInfo() method

Get detailed properties of Board

## Signature

```typescript
function getBoardInfo(boardName: string): Promise<IDMT_BoardItem | undefined>;
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

Board name

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IDMT\_BoardItem](../interfaces/IDMT_BoardItem.md) \| undefined&gt;

Board detailed properties of; if it is `undefined`<!-- -->, the retrieval failed

### getcurrentboardinfo

# DMT\_Board.getCurrentBoardInfo() method

Get detailed properties of Current board

## Signature

```typescript
function getCurrentBoardInfo(): Promise<IDMT_BoardItem | undefined>;
```

## Returns

Promise&lt;[IDMT\_BoardItem](../interfaces/IDMT_BoardItem.md) \| undefined&gt;

Board detailed properties of; if it is `undefined`<!-- -->, the retrieval failed

## Remarks

It will get the detailed properties of the board associated with the currently open schematic or PCB that has the last input focus

### modifyboardname

# DMT\_Board.modifyBoardName() method

Modify Board name

## Signature

```typescript
function modifyBoardName(originalBoardName: string, boardName: string): Promise<boolean>;
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

originalBoardName

</td><td>

string

</td><td>

Original board name

</td></tr>
<tr><td>

boardName

</td><td>

string

</td><td>

New board name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether Modify Successful

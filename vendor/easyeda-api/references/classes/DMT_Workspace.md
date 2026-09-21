# DMT\_Workspace class

Document tree / Workspace class

## Signature

```typescript
class DMT_Workspace
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

[getAllWorkspacesInfo()](./DMT_Workspace.md)

</td><td>

</td><td>

Get the detailed properties of all workspaces

</td></tr>
<tr><td>

[getCurrentWorkspaceInfo()](./DMT_Workspace.md)

</td><td>

</td><td>

Get the detailed properties of the current workspace

</td></tr>
<tr><td>

[toggleToWorkspace(workspaceUuid)](./DMT_Workspace.md)

</td><td>

</td><td>

Switch to workspace

</td></tr>
</tbody></table>

---

## 方法详情

### getallworkspacesinfo

# DMT\_Workspace.getAllWorkspacesInfo() method

Get the detailed properties of all workspaces

## Signature

```typescript
function getAllWorkspacesInfo(): Promise<Array<IDMT_WorkspaceItem>>;
```

## Returns

Promise&lt;Array&lt;[IDMT\_WorkspaceItem](../interfaces/IDMT_WorkspaceItem.md)<!-- -->&gt;&gt;

Detailed properties of all workspaces

### getcurrentworkspaceinfo

# DMT\_Workspace.getCurrentWorkspaceInfo() method

Get the detailed properties of the current workspace

## Signature

```typescript
function getCurrentWorkspaceInfo(): Promise<IDMT_WorkspaceItem | undefined>;
```

## Returns

Promise&lt;[IDMT\_WorkspaceItem](../interfaces/IDMT_WorkspaceItem.md) \| undefined&gt;

Detailed properties of the workspace. If it is `undefined`<!-- -->, the retrieval failed

## Remarks

It will get the detailed properties of the current workspace

### toggletoworkspace

# DMT\_Workspace.toggleToWorkspace() method

Switch to workspace

## Signature

```typescript
function toggleToWorkspace(workspaceUuid?: string): Promise<boolean>;
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

workspaceUuid

</td><td>

string

</td><td>

_(Optional)_ Workspace UUID. If not specified, it will switch to the personal workspace

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the switch operation was successful

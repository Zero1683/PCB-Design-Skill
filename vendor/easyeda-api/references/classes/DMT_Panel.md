# DMT\_Panel class

Document tree / Panel management class

## Signature

```typescript
class DMT_Panel
```

## Remarks

Operations related to panel management in the currently open project

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[copyPanel(panelUuid)](./DMT_Panel.md)

</td><td>

</td><td>

Copy Panel

</td></tr>
<tr><td>

[createPanel()](./DMT_Panel.md)

</td><td>

</td><td>

**_(BETA)_** Create Panel

</td></tr>
<tr><td>

[deletePanel(panelUuid)](./DMT_Panel.md)

</td><td>

</td><td>

Delete Panel

</td></tr>
<tr><td>

[getAllPanelsInfo()](./DMT_Panel.md)

</td><td>

</td><td>

Get all in the project panel detailed properties of

</td></tr>
<tr><td>

[getCurrentPanelInfo()](./DMT_Panel.md)

</td><td>

</td><td>

Get detailed properties of Current panel

</td></tr>
<tr><td>

[getPanelInfo(panelUuid)](./DMT_Panel.md)

</td><td>

</td><td>

Get detailed properties of Panel

</td></tr>
<tr><td>

[modifyPanelName(panelUuid, panelName)](./DMT_Panel.md)

</td><td>

</td><td>

Modify Panel name

</td></tr>
</tbody></table>

---

## 方法详情

### copypanel

# DMT\_Panel.copyPanel() method

Copy Panel

## Signature

```typescript
function copyPanel(panelUuid: string): Promise<string | undefined>;
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

panelUuid

</td><td>

string

</td><td>

Source panel UUID

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

New panel UUID. If it is `undefined`<!-- -->, the copy failed

### createpanel

# DMT\_Panel.createPanel() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create Panel

## Signature

```typescript
function createPanel(): Promise<string | undefined>;
```

## Returns

Promise&lt;string \| undefined&gt;

Panel UUID, if it is `undefined` creation fails

### deletepanel

# DMT\_Panel.deletePanel() method

Delete Panel

## Signature

```typescript
function deletePanel(panelUuid: string): Promise<boolean>;
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

panelUuid

</td><td>

string

</td><td>

Panel UUID

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### getallpanelsinfo

# DMT\_Panel.getAllPanelsInfo() method

Get all in the project panel detailed properties of

## Signature

```typescript
function getAllPanelsInfo(): Promise<Array<IDMT_PanelItem>>;
```

## Returns

Promise&lt;Array&lt;[IDMT\_PanelItem](../interfaces/IDMT_PanelItem.md)<!-- -->&gt;&gt;

Array of detailed properties of all panels

### getcurrentpanelinfo

# DMT\_Panel.getCurrentPanelInfo() method

Get detailed properties of Current panel

## Signature

```typescript
function getCurrentPanelInfo(): Promise<IDMT_PanelItem | undefined>;
```

## Returns

Promise&lt;[IDMT\_PanelItem](../interfaces/IDMT_PanelItem.md) \| undefined&gt;

Panel detailed properties of; if it is `undefined`<!-- -->, the retrieval failed

## Remarks

It will get the detailed properties of the currently open panel that has the last input focus

### getpanelinfo

# DMT\_Panel.getPanelInfo() method

Get detailed properties of Panel

## Signature

```typescript
function getPanelInfo(panelUuid: string): Promise<IDMT_PanelItem | undefined>;
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

panelUuid

</td><td>

string

</td><td>

Panel UUID

</td></tr>
</tbody></table>

## Returns

Promise&lt;[IDMT\_PanelItem](../interfaces/IDMT_PanelItem.md) \| undefined&gt;

Panel detailed properties of; if it is `undefined`<!-- -->, the retrieval failed

### modifypanelname

# DMT\_Panel.modifyPanelName() method

Modify Panel name

## Signature

```typescript
function modifyPanelName(panelUuid: string, panelName: string): Promise<boolean>;
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

panelUuid

</td><td>

string

</td><td>

Panel UUID

</td></tr>
<tr><td>

panelName

</td><td>

string

</td><td>

Panel name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether Modify Successful

# DMT\_SelectControl class

Document tree / selection control class

## Signature

```typescript
class DMT_SelectControl
```

## Remarks

Query and control of the selection focus in the document tree

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[getCurrentDocumentInfo()](./DMT_SelectControl.md)

</td><td>

</td><td>

**_(BETA)_** Get the properties of the current document

</td></tr>
</tbody></table>

---

## 方法详情

### getcurrentdocumentinfo

# DMT\_SelectControl.getCurrentDocumentInfo() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the properties of the current document

## Signature

```typescript
function getCurrentDocumentInfo(): Promise<IDMT_EditorDocumentItem | undefined>;
```

## Returns

Promise&lt;[IDMT\_EditorDocumentItem](../interfaces/IDMT_EditorDocumentItem.md) \| undefined&gt;

An object composed of the document type, UUID, the UUID of the project it belongs to, and the UUID of the library it belongs to. If it is `undefined`<!-- -->, the retrieval failed

## Remarks

It will get the document type, UUID, and the UUID of the project or library it belongs to for the currently open document that has the last input focus

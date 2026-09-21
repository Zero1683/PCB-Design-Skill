# LIB\_SelectControl class

Comprehensive library / selection control class

## Signature

```typescript
class LIB_SelectControl
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

[getSelectedLibraryRowInfo()](./LIB_SelectControl.md)

</td><td>

</td><td>

**_(BETA)_** Get the information of the currently selected row in the bottom library

</td></tr>
</tbody></table>

---

## 方法详情

### getselectedlibraryrowinfo

# LIB\_SelectControl.getSelectedLibraryRowInfo() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the information of the currently selected row in the bottom library

## Signature

```typescript
function getSelectedLibraryRowInfo(): Promise<ILIB_LibraryItem | undefined>;
```

## Returns

Promise&lt;[ILIB\_LibraryItem](../interfaces/ILIB_LibraryItem.md) \| undefined&gt;

Library property object; if it is `undefined`<!-- -->, the retrieval failed

## Remarks

It will get the library type, UUID, and the UUID of the library it belongs to for the currently selected row in the bottom library

# SYS\_ShortcutKey class

System / shortcut key class

## Signature

```typescript
class SYS_ShortcutKey
```

## Remarks

Register and manage system shortcut keys

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[getShortcutKeys(includeSystem)](./SYS_ShortcutKey.md)

</td><td>

</td><td>

**_(BETA)_** Query shortcut key list

</td></tr>
<tr><td>

[registerShortcutKey(shortcutKey, title, callbackFn, documentType, scene)](./SYS_ShortcutKey.md)

</td><td>

</td><td>

**_(BETA)_** Register shortcut key

</td></tr>
<tr><td>

[unregisterShortcutKey(shortcutKey)](./SYS_ShortcutKey.md)

</td><td>

</td><td>

**_(BETA)_** Unregister a shortcut key

</td></tr>
</tbody></table>

---

## 方法详情

### getshortcutkeys

# SYS\_ShortcutKey.getShortcutKeys() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Query shortcut key list

## Signature

```typescript
function getShortcutKeys(
	includeSystem?: boolean,
): Promise<
	Array<{
		shortcutKey: TSYS_ShortcutKeys;
		title: string;
		documentType: Array<ESYS_ShortcutKeyEffectiveEditorDocumentType>;
		scene: Array<ESYS_ShortcutKeyEffectiveEditorScene>;
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

includeSystem

</td><td>

boolean

</td><td>

_(Optional)_ Whether Contain system shortcut key

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;{ shortcutKey: [TSYS\_ShortcutKeys](../types/TSYS_ShortcutKeys.md)<!-- -->; title: string; documentType: Array&lt;[ESYS\_ShortcutKeyEffectiveEditorDocumentType](../enums/ESYS_ShortcutKeyEffectiveEditorDocumentType.md)<!-- -->&gt;; scene: Array&lt;[ESYS\_ShortcutKeyEffectiveEditorScene](../enums/ESYS_ShortcutKeyEffectiveEditorScene.md)<!-- -->&gt; }&gt;&gt;

Shortcut key list

### registershortcutkey

# SYS\_ShortcutKey.registerShortcutKey() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Register shortcut key

## Signature

```typescript
function registerShortcutKey(
	shortcutKey: TSYS_ShortcutKeys,
	title: string,
	callbackFn: (shortcutKey: TSYS_ShortcutKeys) => void | Promise<void>,
	documentType?: Array<ESYS_ShortcutKeyEffectiveEditorDocumentType>,
	scene?: Array<ESYS_ShortcutKeyEffectiveEditorScene>,
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

shortcutKey

</td><td>

[TSYS\_ShortcutKeys](../types/TSYS_ShortcutKeys.md)

</td><td>

Shortcut key. If the array contains multiple elements, it is parsed as a combined shortcut key and sorted by rules before being stored in the cache

</td></tr>
<tr><td>

title

</td><td>

string

</td><td>

Shortcut key title, the friendly name of the shortcut key

</td></tr>
<tr><td>

callbackFn

</td><td>

(shortcutKey: [TSYS\_ShortcutKeys](../types/TSYS_ShortcutKeys.md)<!-- -->) =&gt; void \| Promise&lt;void&gt;

</td><td>

Callback function

</td></tr>
<tr><td>

documentType

</td><td>

Array&lt;[ESYS\_ShortcutKeyEffectiveEditorDocumentType](../enums/ESYS_ShortcutKeyEffectiveEditorDocumentType.md)<!-- -->&gt;

</td><td>

_(Optional)_

</td></tr>
<tr><td>

scene

</td><td>

Array&lt;[ESYS\_ShortcutKeyEffectiveEditorScene](../enums/ESYS_ShortcutKeyEffectiveEditorScene.md)<!-- -->&gt;

</td><td>

_(Optional)_

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Register whether the operation is successful

### unregistershortcutkey

# SYS\_ShortcutKey.unregisterShortcutKey() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Unregister a shortcut key

## Signature

```typescript
function unregisterShortcutKey(shortcutKey: TSYS_ShortcutKeys): Promise<boolean>;
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

shortcutKey

</td><td>

[TSYS\_ShortcutKeys](../types/TSYS_ShortcutKeys.md)

</td><td>

Shortcut key. The order of the passed-in elements is not distinguished; it will be sorted automatically and the matching shortcut key will be queried

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the unregistration operation was successful

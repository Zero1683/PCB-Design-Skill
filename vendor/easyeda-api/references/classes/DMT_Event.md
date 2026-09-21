# DMT\_Event class

Document tree / event class

## Signature

```typescript
class DMT_Event
```

## Remarks

Register an event callback

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[addEditorTabEventListener(id, eventType, callFn, onlyOnce)](./DMT_Event.md)

</td><td>

</td><td>

**_(BETA)_** Add an editor tab event listener

</td></tr>
<tr><td>

[isEventListenerAlreadyExist(id)](./DMT_Event.md)

</td><td>

</td><td>

Query whether the event listener exists

</td></tr>
<tr><td>

[removeEventListener(id)](./DMT_Event.md)

</td><td>

</td><td>

Remove Event listener

</td></tr>
</tbody></table>

---

## 方法详情

### addeditortabeventlistener

# DMT\_Event.addEditorTabEventListener() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Add an editor tab event listener

## Signature

```typescript
function addEditorTabEventListener(
	id: string,
	eventType: 'all' | EDMT_EditorTabEventType,
	callFn: (
		eventType: EDMT_EditorTabEventType,
		props: { documentType: EDMT_EditorDocumentType; title: string; tabId: string },
	) => void | Promise<void>,
	onlyOnce?: boolean,
): void;
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

id

</td><td>

string

</td><td>

Event ID, used to prevent duplicate event registration

</td></tr>
<tr><td>

eventType

</td><td>

'all' \| [EDMT\_EditorTabEventType](../enums/EDMT_EditorTabEventType.md)

</td><td>

Event type

</td></tr>
<tr><td>

callFn

</td><td>

(eventType: [EDMT\_EditorTabEventType](../enums/EDMT_EditorTabEventType.md)<!-- -->, props: { documentType: [EDMT\_EditorDocumentType](../enums/EDMT_EditorDocumentType.md)<!-- -->; title: string; tabId: string }) =&gt; void \| Promise&lt;void&gt;

</td><td>

The callback function triggered when the event fires

</td></tr>
<tr><td>

onlyOnce

</td><td>

boolean

</td><td>

_(Optional)_ Whether to listen only once

</td></tr>
</tbody></table>

## Returns

void

## Remarks

Note: This API is only valid for extensions. Calling it in a standalone script environment will always `throw Error`

When the [tab event type](../enums/EDMT_EditorTabEventType.md) is [close](../enums/EDMT_EditorTabEventType.md) or [open](../enums/EDMT_EditorTabEventType.md)<!-- -->, the [switch](../enums/EDMT_EditorTabEventType.md) event will also be triggered

### iseventlisteneralreadyexist

# DMT\_Event.isEventListenerAlreadyExist() method

Query whether the event listener exists

## Signature

```typescript
function isEventListenerAlreadyExist(id: string): boolean;
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

id

</td><td>

string

</td><td>

Event ID

</td></tr>
</tbody></table>

## Returns

boolean

Whether the event listener exists

### removeeventlistener

# DMT\_Event.removeEventListener() method

Remove Event listener

## Signature

```typescript
function removeEventListener(id: string): boolean;
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

id

</td><td>

string

</td><td>

Event ID

</td></tr>
</tbody></table>

## Returns

boolean

Whether Remove Specify event listener

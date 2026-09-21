# PCB\_Event class

PCB &amp; footprint / event class

## Signature

```typescript
class PCB_Event
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

[addCrossProbeSelectEventListener(id, callFn)](./PCB_Event.md)

</td><td>

</td><td>

**_(BETA)_** Add a cross-probe selection event listener

</td></tr>
<tr><td>

[addMouseEventListener(id, eventType, callFn, onlyOnce)](./PCB_Event.md)

</td><td>

</td><td>

**_(BETA)_** Add a mouse event listener

</td></tr>
<tr><td>

[addNetEventListener(id, eventType, callFn, onlyOnce)](./PCB_Event.md)

</td><td>

</td><td>

**_(BETA)_** Add a net event listener

</td></tr>
<tr><td>

[addPrimitiveEventListener(id, eventType, callFn, onlyOnce)](./PCB_Event.md)

</td><td>

</td><td>

**_(BETA)_** Add a primitive event listener

</td></tr>
<tr><td>

[addRayTracerEngine3DViewCameraChangeEventListener(id, callFn, onlyOnce)](./PCB_Event.md)

</td><td>

</td><td>

**_(BETA)_** Add a ray tracer engine 3D preview camera change (dragging the 3D model) event listener

</td></tr>
<tr><td>

[addRayTracerEngine3DViewClickMaterialEventListener(id, callFn, onlyOnce)](./PCB_Event.md)

</td><td>

</td><td>

**_(BETA)_** Add a ray tracer engine 3D preview material click event listener

</td></tr>
<tr><td>

[addRealTimeDrcResultEventListener(id, eventType, callFn)](./PCB_Event.md)

</td><td>

</td><td>

**_(BETA)_** Add a real-time DRC result event listener

</td></tr>
<tr><td>

[isEventListenerAlreadyExist(id)](./PCB_Event.md)

</td><td>

</td><td>

Query whether the event listener exists

</td></tr>
<tr><td>

[removeEventListener(id)](./PCB_Event.md)

</td><td>

</td><td>

Remove Event listener

</td></tr>
</tbody></table>

---

## 方法详情

### addcrossprobeselecteventlistener

# PCB\_Event.addCrossProbeSelectEventListener() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Add a cross-probe selection event listener

## Signature

```typescript
function addCrossProbeSelectEventListener(
	id: string,
	callFn: (props: any) => void | Promise<void>,
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

callFn

</td><td>

(props: any) =&gt; void \| Promise&lt;void&gt;

</td><td>

The callback function triggered when the event fires

</td></tr>
</tbody></table>

## Returns

void

## Remarks

Note: This API is only valid for extensions. Calling it in a standalone script environment will always `throw Error`

### addmouseeventlistener

# PCB\_Event.addMouseEventListener() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Add a mouse event listener

## Signature

```typescript
function addMouseEventListener(
	id: string,
	eventType: 'all' | EPCB_MouseEventType,
	callFn: (
		eventType: EPCB_MouseEventType,
		props: [
			{
				primitiveId: string;
				primitiveType: EPCB_PrimitiveType;
				net?: string;
				designator?: string;
				parentComponentPrimitiveId?: string;
				parentComponentDesignator?: string;
			},
		],
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

'all' \| [EPCB\_MouseEventType](../enums/EPCB_MouseEventType.md)

</td><td>

Event type

</td></tr>
<tr><td>

callFn

</td><td>

(eventType: [EPCB\_MouseEventType](../enums/EPCB_MouseEventType.md)<!-- -->, props: \[{ primitiveId: string; primitiveType: [EPCB\_PrimitiveType](../enums/EPCB_PrimitiveType.md)<!-- -->; net?: string; designator?: string; parentComponentPrimitiveId?: string; parentComponentDesignator?: string }\]) =&gt; void \| Promise&lt;void&gt;

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

### addneteventlistener

# PCB\_Event.addNetEventListener() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Add a net event listener

## Signature

```typescript
function addNetEventListener(
	id: string,
	eventType: 'all' | EPCB_NetEventType,
	callFn: (eventType: EPCB_NetEventType, props: [{ net: string }]) => void | Promise<void>,
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

'all' \| [EPCB\_NetEventType](../enums/EPCB_NetEventType.md)

</td><td>

Event type

</td></tr>
<tr><td>

callFn

</td><td>

(eventType: [EPCB\_NetEventType](../enums/EPCB_NetEventType.md)<!-- -->, props: \[{ net: string }\]) =&gt; void \| Promise&lt;void&gt;

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

Net select event only

1. When the net option is selected in the filter panel and a net is selected on the canvas

2. When a net is selected in Engineering Design -<!-- -->&gt; Nets

the event will be triggered

Note: This API is only valid for extensions. Calling it in a standalone script environment will always `throw Error`

### addprimitiveeventlistener

# PCB\_Event.addPrimitiveEventListener() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Add a primitive event listener

## Signature

```typescript
function addPrimitiveEventListener(
	id: string,
	eventType: 'all' | EPCB_PrimitiveEventType,
	callFn: (
		eventType: EPCB_PrimitiveEventType,
		props: [
			{
				primitiveId: string;
				primitiveType: EPCB_PrimitiveType;
				net?: string;
				designator?: string;
				parentComponentPrimitiveId?: string;
				parentComponentDesignator?: string;
			},
		],
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

'all' \| [EPCB\_PrimitiveEventType](../enums/EPCB_PrimitiveEventType.md)

</td><td>

Event type

</td></tr>
<tr><td>

callFn

</td><td>

(eventType: [EPCB\_PrimitiveEventType](../enums/EPCB_PrimitiveEventType.md)<!-- -->, props: \[{ primitiveId: string; primitiveType: [EPCB\_PrimitiveType](../enums/EPCB_PrimitiveType.md)<!-- -->; net?: string; designator?: string; parentComponentPrimitiveId?: string; parentComponentDesignator?: string }\]) =&gt; void \| Promise&lt;void&gt;

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

### addraytracerengine3dviewcamerachangeeventlistener

# PCB\_Event.addRayTracerEngine3DViewCameraChangeEventListener() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Add a ray tracer engine 3D preview camera change (dragging the 3D model) event listener

## Signature

```typescript
function addRayTracerEngine3DViewCameraChangeEventListener(
	id: string,
	callFn: (props: {
		position: { x: number; y: number; z: number };
		rotation: { x: number; y: number; z: number };
		focalLength: number;
	}) => void | Promise<void>,
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

callFn

</td><td>

(props: { position: { x: number; y: number; z: number }; rotation: { x: number; y: number; z: number }; focalLength: number }) =&gt; void \| Promise&lt;void&gt;

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

Note: This API is only valid for extensions. Calling it in a standalone script environment will always `throw Error` ADD since EDA v4

### addraytracerengine3dviewclickmaterialeventlistener

# PCB\_Event.addRayTracerEngine3DViewClickMaterialEventListener() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Add a ray tracer engine 3D preview material click event listener

## Signature

```typescript
function addRayTracerEngine3DViewClickMaterialEventListener(
	id: string,
	callFn: (props: { materialId: number; material: any }) => void | Promise<void>,
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

callFn

</td><td>

(props: { materialId: number; material: any }) =&gt; void \| Promise&lt;void&gt;

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

Note: This API is only valid for extensions. Calling it in a standalone script environment will always `throw Error` ADD since EDA v4

### addrealtimedrcresulteventlistener

# PCB\_Event.addRealTimeDrcResultEventListener() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Add a real-time DRC result event listener

## Signature

```typescript
function addRealTimeDrcResultEventListener(
	id: string,
	eventType: 'all',
	callFn: (eventType: undefined, props: [{ drcResult: any }]) => void | Promise<void>,
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

'all'

</td><td>

Event type

</td></tr>
<tr><td>

callFn

</td><td>

(eventType: undefined, props: \[{ drcResult: any }\]) =&gt; void \| Promise&lt;void&gt;

</td><td>

The callback function triggered when the event fires

</td></tr>
</tbody></table>

## Returns

void

## Remarks

Note: This API is only valid for extensions. Calling it in a standalone script environment will always `throw Error`

### iseventlisteneralreadyexist

# PCB\_Event.isEventListenerAlreadyExist() method

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

# PCB\_Event.removeEventListener() method

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

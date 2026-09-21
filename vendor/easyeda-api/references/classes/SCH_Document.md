# SCH\_Document class

Schematic &amp; symbol / document operation class

## Signature

```typescript
class SCH_Document
```

## Remarks

Operations performed on the design document as a whole

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[autoLayout(props)](./SCH_Document.md)

</td><td>

</td><td>

**_(BETA)_** Auto layout

</td></tr>
<tr><td>

[autoRouting(props)](./SCH_Document.md)

</td><td>

</td><td>

**_(BETA)_** Auto routing

</td></tr>
<tr><td>

[importChanges()](./SCH_Document.md)

</td><td>

</td><td>

Import changes from the PCB

</td></tr>
<tr><td>

[save()](./SCH_Document.md)

</td><td>

</td><td>

Save Document

</td></tr>
</tbody></table>

---

## 方法详情

### autolayout

# SCH\_Document.autoLayout() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Auto layout

## Signature

```typescript
function autoLayout(props?: {
	uuids?: Array<string>;
	netlist?: {
		component: {
			[uniqueId: string]: {
				pinInfoMap: {
					[key: string]: {
						name: string;
						number: string;
						net: string;
						props: { 'Pin Number': string };
					};
				};
			};
		};
	};
	designatorDeviceTypeMap?: {
		[designator: string]:
			| 'resistor'
			| 'capacitor'
			| 'inductive'
			| 'diode'
			| 'triode'
			| 'oscillator'
			| 'chip'
			| 'otherDevice';
	};
}): Promise<any>;
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

props

</td><td>

{ uuids?: Array&lt;string&gt;; netlist?: { component: { \[uniqueId: string\]: { pinInfoMap: { \[key: string\]: { name: string; number: string; net: string; props: { 'Pin Number': string } } } } } }; designatorDeviceTypeMap?: { \[designator: string\]: 'resistor' \| 'capacitor' \| 'inductive' \| 'diode' \| 'triode' \| 'oscillator' \| 'chip' \| 'otherDevice' } }

</td><td>

_(Optional)_ Auto layout parameter

</td></tr>
</tbody></table>

## Returns

Promise&lt;any&gt;

Auto layout result

## Remarks

If no parameters are passed in, auto layout will be performed for all devices

### autorouting

# SCH\_Document.autoRouting() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Auto routing

## Signature

```typescript
function autoRouting(props?: {
	uuids?: Array<string>;
	netlist?: {
		component: {
			[uniqueId: string]: {
				pinInfoMap: {
					[key: string]: {
						name: string;
						number: string;
						net: string;
						props: { 'Pin Number': string };
					};
				};
			};
		};
	};
	designatorDeviceTypeMap?: {
		[designator: string]:
			| 'resistor'
			| 'capacitor'
			| 'inductive'
			| 'diode'
			| 'triode'
			| 'oscillator'
			| 'chip'
			| 'otherDevice';
	};
}): Promise<any>;
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

props

</td><td>

{ uuids?: Array&lt;string&gt;; netlist?: { component: { \[uniqueId: string\]: { pinInfoMap: { \[key: string\]: { name: string; number: string; net: string; props: { 'Pin Number': string } } } } } }; designatorDeviceTypeMap?: { \[designator: string\]: 'resistor' \| 'capacitor' \| 'inductive' \| 'diode' \| 'triode' \| 'oscillator' \| 'chip' \| 'otherDevice' } }

</td><td>

_(Optional)_ Auto routing parameter

</td></tr>
</tbody></table>

## Returns

Promise&lt;any&gt;

Auto routing result

## Remarks

If no parameters are passed in, auto routing will be performed for all unrouted nets

### importchanges

# SCH\_Document.importChanges() method

Import changes from the PCB

## Signature

```typescript
function importChanges(): Promise<boolean>;
```

## Returns

Promise&lt;boolean&gt;

Whether the import operation is successful, import failed or a free schematic return `false`

### save

# SCH\_Document.save() method

Save Document

## Signature

```typescript
function save(): Promise<boolean>;
```

## Returns

Promise&lt;boolean&gt;

Whether the save operation was successful. Errors such as save failure and upload failure all return `false`

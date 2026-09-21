# LIB\_SimulationModel class

Comprehensive library / simulation model class

## Signature

```typescript
class LIB_SimulationModel
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

[copy(simulationModelUuid, libraryUuid, targetLibraryUuid, targetClassification, newSimulationModelName)](./LIB_SimulationModel.md)

</td><td>

</td><td>

**_(BETA)_** Copy the simulation model

</td></tr>
<tr><td>

[create(libraryUuid, model, classification, description)](./LIB_SimulationModel.md)

</td><td>

</td><td>

**_(BETA)_** Create a simulation model

</td></tr>
<tr><td>

[delete(simulationModelUuid, libraryUuid)](./LIB_SimulationModel.md)

</td><td>

</td><td>

**_(BETA)_** Delete the simulation model

</td></tr>
<tr><td>

[get(simulationModelUuid, libraryUuid)](./LIB_SimulationModel.md)

</td><td>

</td><td>

**_(BETA)_** Get all properties of the simulation model

</td></tr>
<tr><td>

[modify(simulationModelUuid, libraryUuid, modelProps, classification, description)](./LIB_SimulationModel.md)

</td><td>

</td><td>

**_(BETA)_** Modify the simulation model

</td></tr>
<tr><td>

[search(key, libraryUuid, classification, simulationModelType, itemsOfPage, page)](./LIB_SimulationModel.md)

</td><td>

</td><td>

**_(BETA)_** Search simulation models

</td></tr>
</tbody></table>

---

## 方法详情

### copy

# LIB\_SimulationModel.copy() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Copy the simulation model

## Signature

```typescript
function copy(
	simulationModelUuid: string,
	libraryUuid: string,
	targetLibraryUuid: string,
	targetClassification?: Array<string>,
	newSimulationModelName?: string,
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

simulationModelUuid

</td><td>

string

</td><td>

Simulation model UUID

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

Library UUID, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
<tr><td>

targetLibraryUuid

</td><td>

string

</td><td>

Target library UUID

</td></tr>
<tr><td>

targetClassification

</td><td>

Array&lt;string&gt;

</td><td>

_(Optional)_ Classification in the target library

</td></tr>
<tr><td>

newSimulationModelName

</td><td>

string

</td><td>

_(Optional)_ New simulation model name. If a symbol with the same name exists in the target library, the copy will fail

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

UUID of the new simulation model in the target library

## Remarks

ADD since EDA v3.2.167

### create

# LIB\_SimulationModel.create() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create a simulation model

## Signature

```typescript
function create(
	libraryUuid: string,
	model: { modelType: 'Ngspice' } & (
		| { modelFile: Blob; modelName?: string; modelCategory?: string; modelPin?: string }
		| { modelData: string; modelName?: string; modelCategory?: string; modelPin?: string }
	),
	classification?: Array<string>,
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

libraryUuid

</td><td>

string

</td><td>

Library UUID, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
<tr><td>

model

</td><td>

{ modelType: 'Ngspice' } &amp; ({ modelFile: Blob; modelName?: string; modelCategory?: string; modelPin?: string } \| { modelData: string; modelName?: string; modelCategory?: string; modelPin?: string })

</td><td>

Simulation model data

</td></tr>
<tr><td>

classification

</td><td>

Array&lt;string&gt;

</td><td>

_(Optional)_ Classification

</td></tr>
<tr><td>

description

</td><td>

string

</td><td>

_(Optional)_ Description

</td></tr>
</tbody></table>

## Returns

Promise&lt;string \| undefined&gt;

Simulation model UUID

## Remarks

ADD since EDA v3.2.167

### delete

# LIB\_SimulationModel.delete() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete the simulation model

## Signature

```typescript
function delete(simulationModelUuid: string, libraryUuid: string): Promise<boolean>;
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

simulationModelUuid

</td><td>

string

</td><td>

Simulation model UUID

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

Library UUID, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

ADD since EDA v3.2.167

### get

# LIB\_SimulationModel.get() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all properties of the simulation model

## Signature

```typescript
function get(
	simulationModelUuid: string,
	libraryUuid?: string,
): Promise<ILIB_SimulationModelItem | undefined>;
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

simulationModelUuid

</td><td>

string

</td><td>

Simulation model UUID

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

_(Optional)_ Library UUID, default is system library, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
</tbody></table>

## Returns

Promise&lt;[ILIB\_SimulationModelItem](../interfaces/ILIB_SimulationModelItem.md) \| undefined&gt;

Simulation model properties

## Remarks

Note: This API is only valid for the private deployment edition. Calling it in other editions will always `throw Error` ADD since EDA v3.2.167

### modify

# LIB\_SimulationModel.modify() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify the simulation model

## Signature

```typescript
function modify(
	simulationModelUuid: string,
	libraryUuid: string,
	modelProps?: { modelName?: string; modelCategory?: string; modelPin?: string },
	classification?: Array<string> | null,
	description?: string | null,
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

simulationModelUuid

</td><td>

string

</td><td>

Simulation model UUID

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

Library UUID, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
<tr><td>

modelProps

</td><td>

\{ modelName?: string; modelCategory?: string; modelPin?: string \}

</td><td>

_(Optional)_ Simulation model properties

</td></tr>
<tr><td>

classification

</td><td>

Array&lt;string&gt; \| null

</td><td>

_(Optional)_ Classification

</td></tr>
<tr><td>

description

</td><td>

string \| null

</td><td>

_(Optional)_ Description

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

If you want to clear certain properties, set their values to `null` ADD since EDA v3.2.167

### search

# LIB\_SimulationModel.search() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Search simulation models

## Signature

```typescript
function search(
	key: string,
	libraryUuid?: string,
	classification?: Array<string>,
	simulationModelType?: ELIB_SimulationModelType,
	itemsOfPage?: number,
	page?: number,
): Promise<Array<ILIB_SimulationModelSearchItem>>;
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

key

</td><td>

string

</td><td>

Search keyword

</td></tr>
<tr><td>

libraryUuid

</td><td>

string

</td><td>

_(Optional)_ Library UUID, default is system library, you can use [LIB\_LibrariesList](./LIB_LibrariesList.md) APIs in

</td></tr>
<tr><td>

classification

</td><td>

Array&lt;string&gt;

</td><td>

_(Optional)_ Classification, defaults to all

</td></tr>
<tr><td>

simulationModelType

</td><td>

[ELIB\_SimulationModelType](../enums/ELIB_SimulationModelType.md)

</td><td>

_(Optional)_ Simulation model type, defaults to all

</td></tr>
<tr><td>

itemsOfPage

</td><td>

number

</td><td>

_(Optional)_ Number of search results per page

</td></tr>
<tr><td>

page

</td><td>

number

</td><td>

_(Optional)_ Page count

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[ILIB\_SimulationModelSearchItem](../interfaces/ILIB_SimulationModelSearchItem.md)<!-- -->&gt;&gt;

List of searched simulation model properties

## Remarks

ADD since EDA v3.2.167

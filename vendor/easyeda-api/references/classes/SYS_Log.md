# SYS\_Log class

System / log class

## Signature

```typescript
class SYS_Log
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

[add(message, type)](./SYS_Log.md)

</td><td>

</td><td>

Add a log entry

</td></tr>
<tr><td>

[clear()](./SYS_Log.md)

</td><td>

</td><td>

Clear the log

</td></tr>
<tr><td>

[export(types)](./SYS_Log.md)

</td><td>

</td><td>

Export the log

</td></tr>
<tr><td>

[find(message, types)](./SYS_Log.md)

</td><td>

</td><td>

Find entries

</td></tr>
<tr><td>

[sort(types)](./SYS_Log.md)

</td><td>

</td><td>

Filter and get log entries

</td></tr>
</tbody></table>

---

## 方法详情

### add

# SYS\_Log.add() method

Add a log entry

## Signature

```typescript
function add(message: string, type?: ESYS_LogType): void;
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

message

</td><td>

string

</td><td>

Log content

</td></tr>
<tr><td>

type

</td><td>

[ESYS\_LogType](../enums/ESYS_LogType.md)

</td><td>

_(Optional)_ Log type

</td></tr>
</tbody></table>

## Returns

void

### clear

# SYS\_Log.clear() method

Clear the log

## Signature

```typescript
function clear(): void;
```

## Returns

void

### export

# SYS\_Log.export() method

Export the log

## Signature

```typescript
function export(types?: ESYS_LogType | Array<ESYS_LogType>): void;
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

types

</td><td>

[ESYS\_LogType](../enums/ESYS_LogType.md) \| Array&lt;[ESYS\_LogType](../enums/ESYS_LogType.md)<!-- -->&gt;

</td><td>

_(Optional)_ Log type

</td></tr>
</tbody></table>

## Returns

void

### find

# SYS\_Log.find() method

Find entries

## Signature

```typescript
function find(
	message:
		| string
		| Array<
			| string
			| {
				text: string;
				attr?: {
					id?: string;
					path?: string;
					sheet?: string;
					pcbid?: string;
					type?: string;
				};
			}
		>,
	types?: ESYS_LogType | Array<ESYS_LogType>,
): Promise<Array<ISYS_LogLine>>;
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

message

</td><td>

string \| Array&lt;string \| { text: string; attr?: { id?: string; path?: string; sheet?: string; pcbid?: string; type?: string } }&gt;

</td><td>

Find content

</td></tr>
<tr><td>

types

</td><td>

[ESYS\_LogType](../enums/ESYS_LogType.md) \| Array&lt;[ESYS\_LogType](../enums/ESYS_LogType.md)<!-- -->&gt;

</td><td>

_(Optional)_ Array of log types. The search can be performed within the specified log types

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[ISYS\_LogLine](../interfaces/ISYS_LogLine.md)<!-- -->&gt;&gt;

Array of log entries matching the find criteria

## Remarks

If the log panel is open, the find operation will also be displayed on the front end

### sort

# SYS\_Log.sort() method

Filter and get log entries

## Signature

```typescript
function sort(types?: ESYS_LogType | Array<ESYS_LogType>): Promise<Array<ISYS_LogLine>>;
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

types

</td><td>

[ESYS\_LogType](../enums/ESYS_LogType.md) \| Array&lt;[ESYS\_LogType](../enums/ESYS_LogType.md)<!-- -->&gt;

</td><td>

_(Optional)_ Array of log types. Multiple log types can be specified at the same time. If not specified, all types are used

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[ISYS\_LogLine](../interfaces/ISYS_LogLine.md)<!-- -->&gt;&gt;

Array of log entries matching the filter criteria

## Remarks

If the log panel is open, the filter operation will also be displayed on the front end

# SYS\_Tool class

System / tool class

## Signature

```typescript
class SYS_Tool
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

[netlistComparison(netlist1, netlist2)](./SYS_Tool.md)

</td><td>

</td><td>

**_(BETA)_** Netlist comparison

</td></tr>
</tbody></table>

---

## 方法详情

### netlistcomparison

# SYS\_Tool.netlistComparison() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Netlist comparison

## Signature

```typescript
function netlistComparison(
	netlist1: string | { projectUuid: string; documentUuid: string } | File,
	netlist2: string | { projectUuid: string; documentUuid: string } | File,
): Promise<
	Array<{
		type: 'Net' | 'Component';
		object: string;
		netlist1Name: Array<string>;
		netlist2Name: Array<string>;
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

netlist1

</td><td>

string \| { projectUuid: string; documentUuid: string } \| File

</td><td>

Netlist 1, which can be: 1. The UUID of a schematic or PCB in the current project; 2. The project UUID and schematic/PCB UUID of another project; 3. Schematic or PCB file data

</td></tr>
<tr><td>

netlist2

</td><td>

string \| { projectUuid: string; documentUuid: string } \| File

</td><td>

Netlist 2, which can be: 1. The UUID of a schematic or PCB in the current project; 2. The project UUID and schematic/PCB UUID of another project; 3. Schematic or PCB file data

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;{ type: 'Net' \| 'Component'; object: string; netlist1Name: Array&lt;string&gt;; netlist2Name: Array&lt;string&gt; }&gt;&gt;

Netlist comparison result

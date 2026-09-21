# PCB\_Drc class

PCB &amp; footprint / design rule check (DRC) class

## Signature

```typescript
class PCB_Drc
```

## Remarks

Check and set DRC rules

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[addNetToEqualLengthNetGroup(equalLengthNetGroupName, net)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Add a net to an equal-length net group

</td></tr>
<tr><td>

[addNetToNetClass(netClassName, net)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Will net add to net class

</td></tr>
<tr><td>

[addPadPairToPadPairGroup(padPairGroupName, padPair)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Add a pad pair to a pad pair group

</td></tr>
<tr><td>

[check(strict, userInterface, includeVerboseError)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Check DRC

</td></tr>
<tr><td>

[check(strict, userInterface, includeVerboseError)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Check DRC

</td></tr>
<tr><td>

[createDifferentialPair(differentialPairName, positiveNet, negativeNet)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Create a differential pair

</td></tr>
<tr><td>

[createEqualLengthNetGroup(equalLengthNetGroupName, nets, color)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Create an equal-length net group

</td></tr>
<tr><td>

[createNetClass(netClassName, nets, color)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Create Net class

</td></tr>
<tr><td>

[createPadPairGroup(padPairGroupName, padPairs)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Create a pad pair group

</td></tr>
<tr><td>

[deleteDifferentialPair(differentialPairName)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Delete the differential pair

</td></tr>
<tr><td>

[deleteEqualLengthNetGroup(equalLengthNetGroupName)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Delete the equal-length net group

</td></tr>
<tr><td>

[deleteNetClass(netClassName)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Delete Net class

</td></tr>
<tr><td>

[deletePadPairGroup(padPairGroupName)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Delete the pad pair group

</td></tr>
<tr><td>

[deleteRuleConfiguration(configurationName)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Delete Design rule configuration

</td></tr>
<tr><td>

[getAllDifferentialPairs()](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Get the detailed properties of all differential pairs

</td></tr>
<tr><td>

[getAllEqualLengthNetGroups()](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Get the detailed properties of all equal-length net groups

</td></tr>
<tr><td>

[getAllNetClasses()](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Get all Net class detailed properties of

</td></tr>
<tr><td>

[getAllPadPairGroups()](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Get the detailed properties of all pad pair groups

</td></tr>
<tr><td>

[getAllRuleConfigurations(includeSystem)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Get all Design rule configuration

</td></tr>
<tr><td>

[getCurrentRuleConfiguration()](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Get Current design rule configuration

</td></tr>
<tr><td>

[getCurrentRuleConfigurationName()](./PCB_Drc.md)

</td><td>

</td><td>

Get Current design rule configuration name

</td></tr>
<tr><td>

[getDefaultRuleConfigurationName()](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Get the name of the default design rule configuration for new PCBs

</td></tr>
<tr><td>

[getNetByNetRules()](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Get Net - net rules

</td></tr>
<tr><td>

[getNetRules()](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Get Net rules

</td></tr>
<tr><td>

[getPadPairGroupMinWireLength(padPairGroupName)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Get the minimum wire length of a pad pair group

</td></tr>
<tr><td>

[getRegionRules()](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Get region rules

</td></tr>
<tr><td>

[getRuleConfiguration(configurationName)](./PCB_Drc.md)

</td><td>

</td><td>

Get Specify design rule configuration

</td></tr>
<tr><td>

[modifyDifferentialPairName(originalDifferentialPairName, differentialPairName)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Modify the name of the differential pair

</td></tr>
<tr><td>

[modifyDifferentialPairNegativeNet(differentialPairName, negativeNet)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Modify the negative net of the differential pair

</td></tr>
<tr><td>

[modifyDifferentialPairPositiveNet(differentialPairName, positiveNet)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Modify the positive net of the differential pair

</td></tr>
<tr><td>

[modifyEqualLengthNetGroupName(originalEqualLengthNetGroupName, equalLengthNetGroupName)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Modify the name of the equal-length net group

</td></tr>
<tr><td>

[modifyNetClassName(originalNetClassName, netClassName)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Modify Net class name of

</td></tr>
<tr><td>

[modifyPadPairGroupName(originalPadPairGroupName, padPairGroupName)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Modify the name of the pad pair group

</td></tr>
<tr><td>

[overwriteCurrentRuleConfiguration(ruleConfiguration)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Overwrite current design rule configuration

</td></tr>
<tr><td>

[overwriteNetByNetRules(netByNetRules)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Overwrite net - net rules

</td></tr>
<tr><td>

[overwriteNetRules(netRules)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Overwrite net rules

</td></tr>
<tr><td>

[overwriteRegionRules(regionRules)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Overwrite region rules

</td></tr>
<tr><td>

[removeNetFromEqualLengthNetGroup(equalLengthNetGroupName, net)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Remove a net from an equal-length net group

</td></tr>
<tr><td>

[removeNetFromNetClass(netClassName, net)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** From net class in remove net

</td></tr>
<tr><td>

[removePadPairFromPadPairGroup(padPairGroupName, padPair)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Remove a pad pair from a pad pair group

</td></tr>
<tr><td>

[renameRuleConfiguration(originalConfigurationName, configurationName)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Rename the design rule configuration

</td></tr>
<tr><td>

[saveRuleConfiguration(ruleConfiguration, configurationName, allowOverwrite)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Save Design rule configuration

</td></tr>
<tr><td>

[setAsDefaultRuleConfiguration(configurationName)](./PCB_Drc.md)

</td><td>

</td><td>

**_(BETA)_** Set as the default design rule configuration for new PCBs

</td></tr>
</tbody></table>

---

## 方法详情

### addnettoequallengthnetgroup

# PCB\_Drc.addNetToEqualLengthNetGroup() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Add a net to an equal-length net group

## Signature

```typescript
function addNetToEqualLengthNetGroup(
	equalLengthNetGroupName: string,
	net: string | Array<string>,
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

equalLengthNetGroupName

</td><td>

string

</td><td>

Equal-length net group name

</td></tr>
<tr><td>

net

</td><td>

string \| Array&lt;string&gt;

</td><td>

Net name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### addnettonetclass

# PCB\_Drc.addNetToNetClass() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Will net add to net class

## Signature

```typescript
function addNetToNetClass(netClassName: string, net: string | Array<string>): Promise<boolean>;
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

netClassName

</td><td>

string

</td><td>

Net class name

</td></tr>
<tr><td>

net

</td><td>

string \| Array&lt;string&gt;

</td><td>

Net name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### addpadpairtopadpairgroup

# PCB\_Drc.addPadPairToPadPairGroup() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Add a pad pair to a pad pair group

## Signature

```typescript
function addPadPairToPadPairGroup(
	padPairGroupName: string,
	padPair: [string, string] | Array<[string, string]>,
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

padPairGroupName

</td><td>

string

</td><td>

Pad pair group name

</td></tr>
<tr><td>

padPair

</td><td>

\[string, string\] \| Array&lt;\[string, string\]&gt;

</td><td>

Pad for

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Example

There are three different usages, and make sure the corresponding pads already exist on the canvas. They are: 1. Free pad - free pad; 2. Device pad - device pad; 3. Device pad - free pad await eda.pcb\_Drc.addPadPairToPadPairGroup('test',\['e0','e1'\]) // 游离焊盘-游离焊盘 await eda.pcb\_Drc.addPadPairToPadPairGroup('test',\['R1:1','R1:2'\]) // 器件焊盘 - 器件焊盘 await eda.pcb\_Drc.addPadPairToPadPairGroup('test',\['R1:1','e1'\]) // 器件焊盘 - 游离焊盘

### check

# PCB\_Drc.check() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Check DRC

## Signature

```typescript
function check(
	strict: boolean,
	userInterface: boolean,
	includeVerboseError: false,
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

strict

</td><td>

boolean

</td><td>

Whether strict checking is enabled. The current PCB is uniformly in strict checking mode

</td></tr>
<tr><td>

userInterface

</td><td>

boolean

</td><td>

Whether to show the UI (open the bottom DRC window)

</td></tr>
<tr><td>

includeVerboseError

</td><td>

false

</td><td>

Whether to include detailed error information in the return value. If it is `true`<!-- -->, the return value will always be an array

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the DRC check passed

### check_1

# PCB\_Drc.check() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Check DRC

## Signature

```typescript
function check(
	strict: boolean,
	userInterface: boolean,
	includeVerboseError: true,
): Promise<Array<any>>;
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

strict

</td><td>

boolean

</td><td>

Whether strict checking is enabled. The current PCB is uniformly in strict checking mode

</td></tr>
<tr><td>

userInterface

</td><td>

boolean

</td><td>

Whether to show the UI (open the bottom DRC window)

</td></tr>
<tr><td>

includeVerboseError

</td><td>

true

</td><td>

Whether to include detailed error information in the return value. If it is `true`<!-- -->, the return value will always be an array

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;any&gt;&gt;

Detailed results of the DRC check

### createdifferentialpair

# PCB\_Drc.createDifferentialPair() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create a differential pair

## Signature

```typescript
function createDifferentialPair(
	differentialPairName: string,
	positiveNet: string,
	negativeNet: string,
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

differentialPairName

</td><td>

string

</td><td>

Differential pair name

</td></tr>
<tr><td>

positiveNet

</td><td>

string

</td><td>

Positive net name

</td></tr>
<tr><td>

negativeNet

</td><td>

string

</td><td>

Negative net name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### createequallengthnetgroup

# PCB\_Drc.createEqualLengthNetGroup() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create an equal-length net group

## Signature

```typescript
function createEqualLengthNetGroup(
	equalLengthNetGroupName: string,
	nets: Array<string>,
	color: IPCB_EqualLengthNetGroupItem['color'],
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

equalLengthNetGroupName

</td><td>

string

</td><td>

Equal-length net group name

</td></tr>
<tr><td>

nets

</td><td>

Array&lt;string&gt;

</td><td>

Net name array

</td></tr>
<tr><td>

color

</td><td>

[IPCB\_EqualLengthNetGroupItem](../interfaces/IPCB_EqualLengthNetGroupItem.md)<!-- -->\['color'\]

</td><td>

Equal-length net group color

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### createnetclass

# PCB\_Drc.createNetClass() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create Net class

## Signature

```typescript
function createNetClass(
	netClassName: string,
	nets: Array<string>,
	color: IPCB_EqualLengthNetGroupItem['color'],
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

netClassName

</td><td>

string

</td><td>

Net class name

</td></tr>
<tr><td>

nets

</td><td>

Array&lt;string&gt;

</td><td>

Net name array

</td></tr>
<tr><td>

color

</td><td>

[IPCB\_EqualLengthNetGroupItem](../interfaces/IPCB_EqualLengthNetGroupItem.md)<!-- -->\['color'\]

</td><td>

Net class color

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### createpadpairgroup

# PCB\_Drc.createPadPairGroup() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Create a pad pair group

## Signature

```typescript
function createPadPairGroup(
	padPairGroupName: string,
	padPairs: Array<[string, string]>,
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

padPairGroupName

</td><td>

string

</td><td>

Pad pair group name

</td></tr>
<tr><td>

padPairs

</td><td>

Array&lt;\[string, string\]&gt;

</td><td>

Pad for array

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Example

There are three different usages, and make sure the corresponding pads already exist on the canvas. They are: 1. Free pad - free pad; 2. Device pad - device pad; 3. Device pad - free pad await eda.pcb\_Drc.createPadPairGroup('test',\[\['e0','e1'\]\]) // 游离焊盘-游离焊盘 await eda.pcb\_Drc.createPadPairGroup('test',\[\['R1:1','R1:2'\],\['R2:1','R2:2'\]\]) // 器件焊盘 - 器件焊盘 await eda.pcb\_Drc.createPadPairGroup('test',\[\['R1:1','e0'\],\['R1:2','e1'\]\]) // 器件焊盘 - 游离焊盘

### deletedifferentialpair

# PCB\_Drc.deleteDifferentialPair() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete the differential pair

## Signature

```typescript
function deleteDifferentialPair(differentialPairName: string): Promise<boolean>;
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

differentialPairName

</td><td>

string

</td><td>

Differential pair name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### deleteequallengthnetgroup

# PCB\_Drc.deleteEqualLengthNetGroup() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete the equal-length net group

## Signature

```typescript
function deleteEqualLengthNetGroup(equalLengthNetGroupName: string): Promise<boolean>;
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

equalLengthNetGroupName

</td><td>

string

</td><td>

Equal-length net group name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### deletenetclass

# PCB\_Drc.deleteNetClass() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete Net class

## Signature

```typescript
function deleteNetClass(netClassName: string): Promise<boolean>;
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

netClassName

</td><td>

string

</td><td>

Net class name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### deletepadpairgroup

# PCB\_Drc.deletePadPairGroup() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete the pad pair group

## Signature

```typescript
function deletePadPairGroup(padPairGroupName: string): Promise<boolean>;
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

padPairGroupName

</td><td>

string

</td><td>

Pad pair group name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### deleteruleconfiguration

# PCB\_Drc.deleteRuleConfiguration() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Delete Design rule configuration

## Signature

```typescript
function deleteRuleConfiguration(configurationName: string): Promise<boolean>;
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

configurationName

</td><td>

string

</td><td>

Configuration name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Delete Whether Successful

## Remarks

The system configuration does not allow deletion

### getalldifferentialpairs

# PCB\_Drc.getAllDifferentialPairs() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the detailed properties of all differential pairs

## Signature

```typescript
function getAllDifferentialPairs(): Promise<
	Array<IPCB_DifferentialPairItem> | { [key: string]: any }
>;
```

## Returns

Promise&lt;Array&lt;[IPCB\_DifferentialPairItem](../interfaces/IPCB_DifferentialPairItem.md)<!-- -->&gt; \| { \[key: string\]: any }&gt;

Detailed properties of all differential pairs

## Remarks

- The return value type is changed to an object BREAKING CHANGE since EDA v3.4

### getallequallengthnetgroups

# PCB\_Drc.getAllEqualLengthNetGroups() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the detailed properties of all equal-length net groups

## Signature

```typescript
function getAllEqualLengthNetGroups(): Promise<Array<IPCB_EqualLengthNetGroupItem>>;
```

## Returns

Promise&lt;Array&lt;[IPCB\_EqualLengthNetGroupItem](../interfaces/IPCB_EqualLengthNetGroupItem.md)<!-- -->&gt;&gt;

Detailed properties of all equal-length net groups

### getallnetclasses

# PCB\_Drc.getAllNetClasses() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all Net class detailed properties of

## Signature

```typescript
function getAllNetClasses(): Promise<Array<IPCB_NetClassItem>>;
```

## Returns

Promise&lt;Array&lt;[IPCB\_NetClassItem](../interfaces/IPCB_NetClassItem.md)<!-- -->&gt;&gt;

Detailed properties of all net classes

### getallpadpairgroups

# PCB\_Drc.getAllPadPairGroups() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the detailed properties of all pad pair groups

## Signature

```typescript
function getAllPadPairGroups(): Promise<Array<IPCB_PadPairGroupItem>>;
```

## Returns

Promise&lt;Array&lt;[IPCB\_PadPairGroupItem](../interfaces/IPCB_PadPairGroupItem.md)<!-- -->&gt;&gt;

Detailed properties of all pad pair groups

### getallruleconfigurations

# PCB\_Drc.getAllRuleConfigurations() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get all Design rule configuration

## Signature

```typescript
function getAllRuleConfigurations(includeSystem?: boolean): Promise<Array<{ [key: string]: any }>>;
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

_(Optional)_ Whether Get System design rule configuration

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;{ \[key: string\]: any }&gt;&gt;

All design rule configurations

### getcurrentruleconfiguration

# PCB\_Drc.getCurrentRuleConfiguration() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Current design rule configuration

## Signature

```typescript
function getCurrentRuleConfiguration(): Promise<{ [key: string]: any } | undefined>;
```

## Returns

Promise&lt;{ \[key: string\]: any } \| undefined&gt;

Current design rule configuration; `undefined` indicates that the retrieval failed

### getcurrentruleconfigurationname

# PCB\_Drc.getCurrentRuleConfigurationName() method

Get Current design rule configuration name

## Signature

```typescript
function getCurrentRuleConfigurationName(): Promise<string | undefined>;
```

## Returns

Promise&lt;string \| undefined&gt;

Current design rule configuration name; `undefined` indicates that the retrieval failed

### getdefaultruleconfigurationname

# PCB\_Drc.getDefaultRuleConfigurationName() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the name of the default design rule configuration for new PCBs

## Signature

```typescript
function getDefaultRuleConfigurationName(): Promise<string | undefined>;
```

## Returns

Promise&lt;string \| undefined&gt;

Default design rule configuration name of; `undefined` indicates that the retrieval failed

### getnetbynetrules

# PCB\_Drc.getNetByNetRules() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Net - net rules

## Signature

```typescript
function getNetByNetRules(): Promise<{ [key: string]: any }>;
```

## Returns

Promise&lt;{ \[key: string\]: any }&gt;

All net-by-net rules of the current PCB

### getnetrules

# PCB\_Drc.getNetRules() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Net rules

## Signature

```typescript
function getNetRules(): Promise<Array<{ [key: string]: any }>>;
```

## Returns

Promise&lt;Array&lt;{ \[key: string\]: any }&gt;&gt;

All net rules of the current PCB

### getpadpairgroupminwirelength

# PCB\_Drc.getPadPairGroupMinWireLength() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the minimum wire length of a pad pair group

## Signature

```typescript
function getPadPairGroupMinWireLength(
	padPairGroupName: string,
): Promise<Array<IPCB_PadPairMinWireLengthItem>>;
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

padPairGroupName

</td><td>

string

</td><td>

Pad pair group name

</td></tr>
</tbody></table>

## Returns

Promise&lt;Array&lt;[IPCB\_PadPairMinWireLengthItem](../interfaces/IPCB_PadPairMinWireLengthItem.md)<!-- -->&gt;&gt;

The minimum wire lengths of all pad pairs

### getregionrules

# PCB\_Drc.getRegionRules() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get region rules

## Signature

```typescript
function getRegionRules(): Promise<Array<{ [key: string]: any }>>;
```

## Returns

Promise&lt;Array&lt;{ \[key: string\]: any }&gt;&gt;

- All region rules of the current PCB

### getruleconfiguration

# PCB\_Drc.getRuleConfiguration() method

Get Specify design rule configuration

## Signature

```typescript
function getRuleConfiguration(
	configurationName: string,
): Promise<{ [key: string]: any } | undefined>;
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

configurationName

</td><td>

string

</td><td>

Configuration name

</td></tr>
</tbody></table>

## Returns

Promise&lt;{ \[key: string\]: any } \| undefined&gt;

Design rule configuration, `undefined` is does not exist this design rules

### modifydifferentialpairname

# PCB\_Drc.modifyDifferentialPairName() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify the name of the differential pair

## Signature

```typescript
function modifyDifferentialPairName(
	originalDifferentialPairName: string,
	differentialPairName: string,
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

originalDifferentialPairName

</td><td>

string

</td><td>

Original differential pair name

</td></tr>
<tr><td>

differentialPairName

</td><td>

string

</td><td>

New differential pair name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### modifydifferentialpairnegativenet

# PCB\_Drc.modifyDifferentialPairNegativeNet() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify the negative net of the differential pair

## Signature

```typescript
function modifyDifferentialPairNegativeNet(
	differentialPairName: string,
	negativeNet: string,
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

differentialPairName

</td><td>

string

</td><td>

Differential pair name

</td></tr>
<tr><td>

negativeNet

</td><td>

string

</td><td>

Negative net name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### modifydifferentialpairpositivenet

# PCB\_Drc.modifyDifferentialPairPositiveNet() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify the positive net of the differential pair

## Signature

```typescript
function modifyDifferentialPairPositiveNet(
	differentialPairName: string,
	positiveNet: string,
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

differentialPairName

</td><td>

string

</td><td>

Differential pair name

</td></tr>
<tr><td>

positiveNet

</td><td>

string

</td><td>

Positive net name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### modifyequallengthnetgroupname

# PCB\_Drc.modifyEqualLengthNetGroupName() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify the name of the equal-length net group

## Signature

```typescript
function modifyEqualLengthNetGroupName(
	originalEqualLengthNetGroupName: string,
	equalLengthNetGroupName: string,
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

originalEqualLengthNetGroupName

</td><td>

string

</td><td>

Original equal-length net group name

</td></tr>
<tr><td>

equalLengthNetGroupName

</td><td>

string

</td><td>

New equal-length net group name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### modifynetclassname

# PCB\_Drc.modifyNetClassName() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Net class name of

## Signature

```typescript
function modifyNetClassName(originalNetClassName: string, netClassName: string): Promise<boolean>;
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

originalNetClassName

</td><td>

string

</td><td>

Original net class name

</td></tr>
<tr><td>

netClassName

</td><td>

string

</td><td>

New net class name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### modifypadpairgroupname

# PCB\_Drc.modifyPadPairGroupName() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify the name of the pad pair group

## Signature

```typescript
function modifyPadPairGroupName(
	originalPadPairGroupName: string,
	padPairGroupName: string,
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

originalPadPairGroupName

</td><td>

string

</td><td>

Original pad pair group name

</td></tr>
<tr><td>

padPairGroupName

</td><td>

string

</td><td>

New pad pair group name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### overwritecurrentruleconfiguration

# PCB\_Drc.overwriteCurrentRuleConfiguration() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Overwrite current design rule configuration

## Signature

```typescript
function overwriteCurrentRuleConfiguration(ruleConfiguration: {
	[key: string]: any;
}): Promise<boolean>;
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

ruleConfiguration

</td><td>

\{ \[key: string\]: any \}

</td><td>

Design rule configuration

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Overwrite whether it is successful

## Remarks

It will overwrite the current design rule configuration of the PCB. Please note the risk of data loss

### overwritenetbynetrules

# PCB\_Drc.overwriteNetByNetRules() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Overwrite net - net rules

## Signature

```typescript
function overwriteNetByNetRules(netByNetRules: { [key: string]: any }): Promise<boolean>;
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

netByNetRules

</td><td>

\{ \[key: string\]: any \}

</td><td>

Net - net rules

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Overwrite whether it is successful

## Remarks

It will overwrite all net-by-net rules of the current PCB. Please note the risk of data loss

### overwritenetrules

# PCB\_Drc.overwriteNetRules() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Overwrite net rules

## Signature

```typescript
function overwriteNetRules(netRules: Array<{ [key: string]: any }>): Promise<boolean>;
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

netRules

</td><td>

Array&lt;{ \[key: string\]: any }&gt;

</td><td>

Net rules

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Overwrite whether it is successful

## Remarks

It will overwrite all net rules of the current PCB. Please note the risk of data loss

### overwriteregionrules

# PCB\_Drc.overwriteRegionRules() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Overwrite region rules

## Signature

```typescript
function overwriteRegionRules(regionRules: Array<{ [key: string]: any }>): Promise<boolean>;
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

regionRules

</td><td>

Array&lt;{ \[key: string\]: any }&gt;

</td><td>

Region rules

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Overwrite whether it is successful

## Remarks

It will overwrite all region rules of the current PCB. Please note the risk of data loss

### removenetfromequallengthnetgroup

# PCB\_Drc.removeNetFromEqualLengthNetGroup() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Remove a net from an equal-length net group

## Signature

```typescript
function removeNetFromEqualLengthNetGroup(
	equalLengthNetGroupName: string,
	net: string | Array<string>,
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

equalLengthNetGroupName

</td><td>

string

</td><td>

Equal-length net group name

</td></tr>
<tr><td>

net

</td><td>

string \| Array&lt;string&gt;

</td><td>

Net name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### removenetfromnetclass

# PCB\_Drc.removeNetFromNetClass() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

From net class in remove net

## Signature

```typescript
function removeNetFromNetClass(netClassName: string, net: string | Array<string>): Promise<boolean>;
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

netClassName

</td><td>

string

</td><td>

Net class name

</td></tr>
<tr><td>

net

</td><td>

string \| Array&lt;string&gt;

</td><td>

Net name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### removepadpairfrompadpairgroup

# PCB\_Drc.removePadPairFromPadPairGroup() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Remove a pad pair from a pad pair group

## Signature

```typescript
function removePadPairFromPadPairGroup(
	padPairGroupName: string,
	padPair: [string, string] | Array<[string, string]>,
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

padPairGroupName

</td><td>

string

</td><td>

Pad pair group name

</td></tr>
<tr><td>

padPair

</td><td>

\[string, string\] \| Array&lt;\[string, string\]&gt;

</td><td>

Pad for

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Example

There are three different usages, and make sure the corresponding pads already exist on the canvas. They are: 1. Free pad - free pad; 2. Device pad - device pad; 3. Device pad - free pad await eda.pcb\_Drc.removePadPairFromPadPairGroup('test',\['e0','e1'\]) // 游离焊盘-游离焊盘 await eda.pcb\_Drc.removePadPairFromPadPairGroup('test',\['R1:1','R1:2'\]) // 器件焊盘 - 器件焊盘 await eda.pcb\_Drc.removePadPairFromPadPairGroup('test',\['R1:2','e1'\]) // 器件焊盘 - 游离焊盘

### renameruleconfiguration

# PCB\_Drc.renameRuleConfiguration() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Rename the design rule configuration

## Signature

```typescript
function renameRuleConfiguration(
	originalConfigurationName: string,
	configurationName: string,
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

originalConfigurationName

</td><td>

string

</td><td>

Original design rule configuration name

</td></tr>
<tr><td>

configurationName

</td><td>

string

</td><td>

New design rule configuration name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the rename was successful

## Remarks

Only custom configurations can be renamed. System configurations cannot be renamed

### saveruleconfiguration

# PCB\_Drc.saveRuleConfiguration() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Save Design rule configuration

## Signature

```typescript
function saveRuleConfiguration(
	ruleConfiguration: { [key: string]: any },
	configurationName: string,
	allowOverwrite?: boolean,
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

ruleConfiguration

</td><td>

\{ \[key: string\]: any \}

</td><td>

Design rule configuration

</td></tr>
<tr><td>

configurationName

</td><td>

string

</td><td>

Configuration name

</td></tr>
<tr><td>

allowOverwrite

</td><td>

boolean

</td><td>

_(Optional)_ Whether to allow overwriting a design rule configuration with the same name. If `false`<!-- -->, `false` will be returned when a configuration with the same name is encountered. Please note the possible risk of data loss

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Save Whether Successful

## Remarks

Only custom configurations can be overwritten and saved. System configurations cannot be modified or overwritten

### setasdefaultruleconfiguration

# PCB\_Drc.setAsDefaultRuleConfiguration() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set as the default design rule configuration for new PCBs

## Signature

```typescript
function setAsDefaultRuleConfiguration(configurationName: string): Promise<boolean>;
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

configurationName

</td><td>

string

</td><td>

Configuration name

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Set Whether Successful

## Remarks

The return value is result-oriented. Repeatedly setting the same design rule as the default will also return `true`

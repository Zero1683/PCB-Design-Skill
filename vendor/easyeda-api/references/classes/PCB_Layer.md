# PCB\_Layer class

PCB &amp; footprint / layer operation class

## Signature

```typescript
class PCB_Layer
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

[addCustomLayer()](./PCB_Layer.md)

</td><td>

</td><td>

**_(BETA)_** Add a custom layer

</td></tr>
<tr><td>

[getAllLayers()](./PCB_Layer.md)

</td><td>

</td><td>

**_(BETA)_** Get the detailed properties of all layers

</td></tr>
<tr><td>

[lockLayer(layer)](./PCB_Layer.md)

</td><td>

</td><td>

**_(BETA)_** Lock the layer

</td></tr>
<tr><td>

[modifyLayer(layer, property)](./PCB_Layer.md)

</td><td>

</td><td>

**_(BETA)_** Modify Layer properties

</td></tr>
<tr><td>

[removeLayer(layer)](./PCB_Layer.md)

</td><td>

</td><td>

**_(BETA)_** Remove Layer

</td></tr>
<tr><td>

[selectLayer(layer)](./PCB_Layer.md)

</td><td>

</td><td>

Select a layer

</td></tr>
<tr><td>

[setInactiveLayerDisplayMode(displayMode)](./PCB_Layer.md)

</td><td>

</td><td>

**_(BETA)_** Set Inactive layer display mode

</td></tr>
<tr><td>

[setInactiveLayerTransparency(transparency)](./PCB_Layer.md)

</td><td>

</td><td>

**_(BETA)_** Set the inactive layer transparency

</td></tr>
<tr><td>

[setLayerColorConfiguration(colorConfiguration)](./PCB_Layer.md)

</td><td>

</td><td>

**_(BETA)_** Set the layer color configuration

</td></tr>
<tr><td>

[setLayerInvisible(layer, setOtherLayerVisible)](./PCB_Layer.md)

</td><td>

</td><td>

**_(BETA)_** Set the layer to invisible

</td></tr>
<tr><td>

[setLayerVisible(layer, setOtherLayerInvisible)](./PCB_Layer.md)

</td><td>

</td><td>

**_(BETA)_** Set the layer to visible

</td></tr>
<tr><td>

[setPcbType(pcbType)](./PCB_Layer.md)

</td><td>

</td><td>

**_(BETA)_** Set PCB type

</td></tr>
<tr><td>

[setTheNumberOfCopperLayers(numberOfLayers)](./PCB_Layer.md)

</td><td>

</td><td>

**_(BETA)_** Set Number of copper layers

</td></tr>
<tr><td>

[unlockLayer(layer)](./PCB_Layer.md)

</td><td>

</td><td>

**_(BETA)_** Unlock the layer

</td></tr>
</tbody></table>

---

## 方法详情

### addcustomlayer

# PCB\_Layer.addCustomLayer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Add a custom layer

## Signature

```typescript
function addCustomLayer(): Promise<TPCB_LayersOfCustom | undefined>;
```

## Returns

Promise&lt;[TPCB\_LayersOfCustom](../types/TPCB_LayersOfCustom.md) \| undefined&gt;

The layer ID of the newly added custom layer. If it is `undefined`<!-- -->, the addition failed, possibly because the number of custom layers has reached the upper limit

### getalllayers

# PCB\_Layer.getAllLayers() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get the detailed properties of all layers

## Signature

```typescript
function getAllLayers(): Promise<Array<IPCB_LayerItem>>;
```

## Returns

Promise&lt;Array&lt;[IPCB\_LayerItem](../interfaces/IPCB_LayerItem.md)<!-- -->&gt;&gt;

Detailed properties of all layers

### locklayer

# PCB\_Layer.lockLayer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Lock the layer

## Signature

```typescript
function lockLayer(
	layer?: TPCB_LayersInTheSelectable | Array<TPCB_LayersInTheSelectable>,
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

layer

</td><td>

[TPCB\_LayersInTheSelectable](../types/TPCB_LayersInTheSelectable.md) \| Array&lt;[TPCB\_LayersInTheSelectable](../types/TPCB_LayersInTheSelectable.md)<!-- -->&gt;

</td><td>

_(Optional)_ Layer. If no layer is specified, all layers are used by default

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### modifylayer

# PCB\_Layer.modifyLayer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Modify Layer properties

## Signature

```typescript
function modifyLayer(
	layer: TPCB_LayersInTheSelectable,
	property: {
		name?: string;
		type?: TPCB_LayerTypesOfInnerLayer;
		color?: string;
		transparency?: number;
	},
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

layer

</td><td>

[TPCB\_LayersInTheSelectable](../types/TPCB_LayersInTheSelectable.md)

</td><td>

Layer

</td></tr>
<tr><td>

property

</td><td>

{ name?: string; type?: [TPCB\_LayerTypesOfInnerLayer](../types/TPCB_LayerTypesOfInnerLayer.md)<!-- -->; color?: string; transparency?: number }

</td><td>

Property

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

The modified layer properties. If it is `undefined`<!-- -->, the modification failed or the layer does not exist

## Remarks

Only inner layers and custom layers can have their names modified; only inner layers can have their types modified. Transparency only supports values between 0-100

### removelayer

# PCB\_Layer.removeLayer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Remove Layer

## Signature

```typescript
function removeLayer(layer: TPCB_LayersOfCustom): Promise<boolean>;
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

layer

</td><td>

[TPCB\_LayersOfCustom](../types/TPCB_LayersOfCustom.md)

</td><td>

Layer

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

Currently only custom layers can be removed

### selectlayer

# PCB\_Layer.selectLayer() method

Select a layer

## Signature

```typescript
function selectLayer(layer: TPCB_LayersInTheSelectable): Promise<boolean>;
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

layer

</td><td>

[TPCB\_LayersInTheSelectable](../types/TPCB_LayersInTheSelectable.md)

</td><td>

Layer

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation was successful. `false` is returned if the specified layer does not exist

### setinactivelayerdisplaymode

# PCB\_Layer.setInactiveLayerDisplayMode() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set Inactive layer display mode

## Signature

```typescript
function setInactiveLayerDisplayMode(displayMode?: EPCB_InactiveLayerDisplayMode): Promise<boolean>;
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

displayMode

</td><td>

[EPCB\_InactiveLayerDisplayMode](../enums/EPCB_InactiveLayerDisplayMode.md)

</td><td>

_(Optional)_ Display mode

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether Set Successful

### setinactivelayertransparency

# PCB\_Layer.setInactiveLayerTransparency() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the inactive layer transparency

## Signature

```typescript
function setInactiveLayerTransparency(transparency: number): Promise<boolean>;
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

transparency

</td><td>

number

</td><td>

Transparency, range `0-100`

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### setlayercolorconfiguration

# PCB\_Layer.setLayerColorConfiguration() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the layer color configuration

## Signature

```typescript
function setLayerColorConfiguration(
	colorConfiguration: EPCB_LayerColorConfiguration,
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

colorConfiguration

</td><td>

[EPCB\_LayerColorConfiguration](../enums/EPCB_LayerColorConfiguration.md)

</td><td>

Color configuration

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### setlayerinvisible

# PCB\_Layer.setLayerInvisible() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the layer to invisible

## Signature

```typescript
function setLayerInvisible(
	layer?: TPCB_LayersInTheSelectable | Array<TPCB_LayersInTheSelectable>,
	setOtherLayerVisible?: boolean,
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

layer

</td><td>

[TPCB\_LayersInTheSelectable](../types/TPCB_LayersInTheSelectable.md) \| Array&lt;[TPCB\_LayersInTheSelectable](../types/TPCB_LayersInTheSelectable.md)<!-- -->&gt;

</td><td>

_(Optional)_ Layer. If no layer is specified, all layers are used by default

</td></tr>
<tr><td>

setOtherLayerVisible

</td><td>

boolean

</td><td>

_(Optional)_ Whether to set other layers to visible

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### setlayervisible

# PCB\_Layer.setLayerVisible() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set the layer to visible

## Signature

```typescript
function setLayerVisible(
	layer?: TPCB_LayersInTheSelectable | Array<TPCB_LayersInTheSelectable>,
	setOtherLayerInvisible?: boolean,
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

layer

</td><td>

[TPCB\_LayersInTheSelectable](../types/TPCB_LayersInTheSelectable.md) \| Array&lt;[TPCB\_LayersInTheSelectable](../types/TPCB_LayersInTheSelectable.md)<!-- -->&gt;

</td><td>

_(Optional)_ Layer. If no layer is specified, all layers are used by default

</td></tr>
<tr><td>

setOtherLayerInvisible

</td><td>

boolean

</td><td>

_(Optional)_ Whether to set other layers to invisible

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

### setpcbtype

# PCB\_Layer.setPcbType() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set PCB type

## Signature

```typescript
function setPcbType(pcbType: EPCB_PcbPlateType): Promise<boolean>;
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

pcbType

</td><td>

[EPCB\_PcbPlateType](../enums/EPCB_PcbPlateType.md)

</td><td>

PCB type

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

This is mainly to support FPC flexible board design. If the PCB type is set to FPC flexible board, an FPC stiffener layer will be added.

Please note:

1. EasyEDA does not yet support FPC flexible board production with more than 2 copper layers;

2. When switching the PCB type from FPC flexible board to ordinary board, any primitives on the FPC stiffener layer must be deleted in advance; otherwise, the switch will fail and `false` will be returned.

### setthenumberofcopperlayers

# PCB\_Layer.setTheNumberOfCopperLayers() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Set Number of copper layers

## Signature

```typescript
function setTheNumberOfCopperLayers(
	numberOfLayers: 2 | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 18 | 20 | 22 | 24 | 26 | 28 | 30 | 32,
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

numberOfLayers

</td><td>

2 \| 4 \| 6 \| 8 \| 10 \| 12 \| 14 \| 16 \| 18 \| 20 \| 22 \| 24 \| 26 \| 28 \| 30 \| 32

</td><td>

Number of copper layers

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

## Remarks

A newly created PCB document has two copper layers by default

### unlocklayer

# PCB\_Layer.unlockLayer() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Unlock the layer

## Signature

```typescript
function unlockLayer(
	layer?: TPCB_LayersInTheSelectable | Array<TPCB_LayersInTheSelectable>,
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

layer

</td><td>

[TPCB\_LayersInTheSelectable](../types/TPCB_LayersInTheSelectable.md) \| Array&lt;[TPCB\_LayersInTheSelectable](../types/TPCB_LayersInTheSelectable.md)<!-- -->&gt;

</td><td>

_(Optional)_ Layer. If no layer is specified, all layers are used by default

</td></tr>
</tbody></table>

## Returns

Promise&lt;boolean&gt;

Whether the operation is successful

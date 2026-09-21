# IPCB\_Polygon class

Single polygon

## Signature

```typescript
class IPCB_Polygon
```

## Remarks

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[discretize(options)](./IPCB_Polygon.md)

</td><td>

</td><td>

**_(BETA)_** Discretize a single polygon into point data

</td></tr>
<tr><td>

[getCenter()](./IPCB_Polygon.md)

</td><td>

</td><td>

**_(BETA)_** Get Single polygon center point

</td></tr>
<tr><td>

[getSource()](./IPCB_Polygon.md)

</td><td>

</td><td>

Get Single polygon data

</td></tr>
</tbody></table>

---

## 方法详情

### discretize

# IPCB\_Polygon.discretize() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Discretize a single polygon into point data

## Signature

```typescript
function discretize(options?: IPCB_DiscretizeOptions): Array<IPCB_DiscretizedPoint>;
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

options

</td><td>

[IPCB\_DiscretizeOptions](../interfaces/IPCB_DiscretizeOptions.md)

</td><td>

_(Optional)_ Discretization options

</td></tr>
</tbody></table>

## Returns

Array&lt;[IPCB\_DiscretizedPoint](../interfaces/IPCB_DiscretizedPoint.md)<!-- -->&gt;

Discretized point data

## Remarks

Discretize the boundary of a single polygon into a series of points

### getcenter

# IPCB\_Polygon.getCenter() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Single polygon center point

## Signature

```typescript
function getCenter(): Promise<{ x: number; y: number }>;
```

## Returns

Promise&lt;{ x: number; y: number }&gt;

Single polygon center point

### getsource

# IPCB\_Polygon.getSource() method

Get Single polygon data

## Signature

```typescript
function getSource(): TPCB_PolygonSourceArray;
```

## Returns

[TPCB\_PolygonSourceArray](../types/TPCB_PolygonSourceArray.md)

Single polygon data

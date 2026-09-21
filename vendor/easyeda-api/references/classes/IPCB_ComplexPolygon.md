# IPCB\_ComplexPolygon class

Complex polygon

## Signature

```typescript
class IPCB_ComplexPolygon
```

## Remarks

developer.mozilla.org/zh-CN/docs/Web/SVG/Attribute/fill-rule \| fill-rule<!-- -->} to combine them to achieve Boolean operations on polygons.

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[addSource(complexPolygon)](./IPCB_ComplexPolygon.md)

</td><td>

</td><td>

Add Polygon data

</td></tr>
<tr><td>

[getCenter()](./IPCB_ComplexPolygon.md)

</td><td>

</td><td>

**_(BETA)_** Get Complex polygon center point

</td></tr>
<tr><td>

[getSource()](./IPCB_ComplexPolygon.md)

</td><td>

</td><td>

Get Polygon data

</td></tr>
<tr><td>

[getSourceStrictComplex()](./IPCB_ComplexPolygon.md)

</td><td>

</td><td>

Get Complex polygon data

</td></tr>
<tr><td>

[toPolygon()](./IPCB_ComplexPolygon.md)

</td><td>

</td><td>

Split is single polygon array

</td></tr>
</tbody></table>

---

## 方法详情

### addsource

# IPCB\_ComplexPolygon.addSource() method

Add Polygon data

## Signature

```typescript
function addSource(
	complexPolygon:
		| TPCB_PolygonSourceArray
		| Array<TPCB_PolygonSourceArray>
		| IPCB_Polygon
		| Array<IPCB_Polygon>,
): IPCB_ComplexPolygon;
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

complexPolygon

</td><td>

[TPCB\_PolygonSourceArray](../types/TPCB_PolygonSourceArray.md) \| Array&lt;[TPCB\_PolygonSourceArray](../types/TPCB_PolygonSourceArray.md)<!-- -->&gt; \| [IPCB\_Polygon](./IPCB_Polygon.md) \| Array&lt;[IPCB\_Polygon](./IPCB_Polygon.md)<!-- -->&gt;

</td><td>

Complex polygon data

</td></tr>
</tbody></table>

## Returns

[IPCB\_ComplexPolygon](./IPCB_ComplexPolygon.md)

Complex polygon object

### getcenter

# IPCB\_ComplexPolygon.getCenter() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Get Complex polygon center point

## Signature

```typescript
function getCenter(): { x: number; y: number };
```

## Returns

\{ x: number; y: number \}

Complex polygon center point

### getsource

# IPCB\_ComplexPolygon.getSource() method

Get Polygon data

## Signature

```typescript
function getSource(): TPCB_PolygonSourceArray | Array<TPCB_PolygonSourceArray>;
```

## Returns

[TPCB\_PolygonSourceArray](../types/TPCB_PolygonSourceArray.md) \| Array&lt;[TPCB\_PolygonSourceArray](../types/TPCB_PolygonSourceArray.md)<!-- -->&gt;

Single polygon or complex polygon data

## Remarks

If it only contains a single polygon, the outermost array will be simplified

### getsourcestrictcomplex

# IPCB\_ComplexPolygon.getSourceStrictComplex() method

Get Complex polygon data

## Signature

```typescript
function getSourceStrictComplex(): Array<TPCB_PolygonSourceArray>;
```

## Returns

Array&lt;[TPCB\_PolygonSourceArray](../types/TPCB_PolygonSourceArray.md)<!-- -->&gt;

Complex polygon data

## Remarks

Forcibly return data in complex polygon format, even if it only contains a single polygon

### topolygon

# IPCB\_ComplexPolygon.toPolygon() method

Split is single polygon array

## Signature

```typescript
function toPolygon(): Array<IPCB_Polygon>;
```

## Returns

Array&lt;[IPCB\_Polygon](./IPCB_Polygon.md)<!-- -->&gt;

Single polygon array

## Remarks

Will complex polygon split is single polygon array of objects

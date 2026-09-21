# ISCH\_PrimitiveComponentPin class

Device pin primitive

## Signature

```typescript
class ISCH_PrimitiveComponentPin extends ISCH_PrimitivePin
```
**Extends:** [ISCH\_PrimitivePin](./ISCH_PrimitivePin.md)

## Remarks

A device pin primitive is a special primitive. It refers to the pin associated with a symbol on the schematic canvas

For a device pin primitive, only the `pinNumber` and `noConnected` properties can be changed; all other properties are read-only. And you can only obtain a device pin primitive through [the getAllPinsByPrimitiveId method of the device class](./SCH_PrimitiveComponent.md) or [the getAllPins method of the device primitive](./ISCH_PrimitiveComponent.md)

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[primitiveType](./ISCH_PrimitiveComponentPin.md)

</td><td>

`protected`

`readonly`

</td><td>

[ESCH\_PrimitiveType.COMPONENT\_PIN](../enums/ESCH_PrimitiveType.md)

</td><td>

图元类型

</td></tr>
</tbody></table>

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

[done()](./ISCH_PrimitiveComponentPin.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
</tbody></table>

---

## 属性详情

### primitivetype

# ISCH\_PrimitiveComponentPin.primitiveType property

图元类型

## Signature

```typescript
function readonly primitiveType: ESCH_PrimitiveType.COMPONENT_PIN;
```


---

## 方法详情

### done

# ISCH\_PrimitiveComponentPin.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<ISCH_PrimitiveComponentPin>;
```

## Returns

Promise&lt;[ISCH\_PrimitiveComponentPin](./ISCH_PrimitiveComponentPin.md)<!-- -->&gt;

Device pin primitive object

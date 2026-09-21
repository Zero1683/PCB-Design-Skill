# ISCH\_PrimitiveCbbSymbolComponent class

Reuse block symbol primitive

## Signature

```typescript
class ISCH_PrimitiveCbbSymbolComponent extends ISCH_PrimitiveComponent
```
**Extends:** [ISCH\_PrimitiveComponent](./ISCH_PrimitiveComponent.md)

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

[done()](./ISCH_PrimitiveCbbSymbolComponent.md)

</td><td>

</td><td>

**_(BETA)_** Apply the changes to the primitives to the canvas

</td></tr>
<tr><td>

[getState\_Cbb()](./ISCH_PrimitiveCbbSymbolComponent.md)

</td><td>

</td><td>

Get the property state: associate reuse block

</td></tr>
<tr><td>

[getState\_CbbSymbol()](./ISCH_PrimitiveCbbSymbolComponent.md)

</td><td>

</td><td>

Get the property state: associate reuse block symbol

</td></tr>
<tr><td>

[reset()](./ISCH_PrimitiveCbbSymbolComponent.md)

</td><td>

</td><td>

**_(BETA)_** Reset the async primitive to the current canvas state

</td></tr>
</tbody></table>

---

## 方法详情

### done

# ISCH\_PrimitiveCbbSymbolComponent.done() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Apply the changes to the primitives to the canvas

## Signature

```typescript
function done(): Promise<ISCH_PrimitiveCbbSymbolComponent>;
```

## Returns

Promise&lt;[ISCH\_PrimitiveCbbSymbolComponent](./ISCH_PrimitiveCbbSymbolComponent.md)<!-- -->&gt;

Reuse block symbol primitive object

### getstate_cbb

# ISCH\_PrimitiveCbbSymbolComponent.getState\_Cbb() method

Get the property state: associate reuse block

## Signature

```typescript
function getState_Cbb(): { libraryUuid: string; uuid: string };
```

## Returns

\{ libraryUuid: string; uuid: string \}

Associate reuse block

### getstate_cbbsymbol

# ISCH\_PrimitiveCbbSymbolComponent.getState\_CbbSymbol() method

Get the property state: associate reuse block symbol

## Signature

```typescript
function getState_CbbSymbol(): {
	libraryUuid: string;
	cbbUuid: string;
	uuid?: string;
	name?: string;
};
```

## Returns

\{ libraryUuid: string; cbbUuid: string; uuid?: string; name?: string \}

Associate reuse block symbol

### reset

# ISCH\_PrimitiveCbbSymbolComponent.reset() method

> This API is provided as a beta preview for developers and may change based on feedback that we receive. Do not use this API in a production environment.

Reset the async primitive to the current canvas state

## Signature

```typescript
function reset(): Promise<ISCH_PrimitiveCbbSymbolComponent>;
```

## Returns

Promise&lt;[ISCH\_PrimitiveCbbSymbolComponent](./ISCH_PrimitiveCbbSymbolComponent.md)<!-- -->&gt;

Reuse block symbol primitive object

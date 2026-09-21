# DMT\_Team class

Document tree / Team class

## Signature

```typescript
class DMT_Team
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

[getAllInvolvedTeamInfo()](./DMT_Team.md)

</td><td>

</td><td>

Get the detailed properties of all involved teams

</td></tr>
<tr><td>

[getAllTeamsInfo()](./DMT_Team.md)

</td><td>

</td><td>

Get the detailed properties of all direct teams

</td></tr>
<tr><td>

[getCurrentTeamInfo()](./DMT_Team.md)

</td><td>

</td><td>

Get the detailed properties of the current team

</td></tr>
</tbody></table>

---

## 方法详情

### getallinvolvedteaminfo

# DMT\_Team.getAllInvolvedTeamInfo() method

Get the detailed properties of all involved teams

## Signature

```typescript
function getAllInvolvedTeamInfo(): Promise<Array<IDMT_TeamItem>>;
```

## Returns

Promise&lt;Array&lt;[IDMT\_TeamItem](../interfaces/IDMT_TeamItem.md)<!-- -->&gt;&gt;

Detailed properties of all involved teams

### getallteamsinfo

# DMT\_Team.getAllTeamsInfo() method

Get the detailed properties of all direct teams

## Signature

```typescript
function getAllTeamsInfo(): Promise<Array<IDMT_TeamItem>>;
```

## Returns

Promise&lt;Array&lt;[IDMT\_TeamItem](../interfaces/IDMT_TeamItem.md)<!-- -->&gt;&gt;

Detailed properties of all teams

## Remarks

A personal space is essentially a team named \*\*Personal\*\*

### getcurrentteaminfo

# DMT\_Team.getCurrentTeamInfo() method

Get the detailed properties of the current team

## Signature

```typescript
function getCurrentTeamInfo(): Promise<IDMT_TeamItem | undefined>;
```

## Returns

Promise&lt;[IDMT\_TeamItem](../interfaces/IDMT_TeamItem.md) \| undefined&gt;

Detailed properties of the team. If it is `undefined`<!-- -->, the retrieval failed

## Remarks

It will get the detailed properties of the team that the project belongs to, associated with the currently open schematic, PCB, or panel that has the last input focus

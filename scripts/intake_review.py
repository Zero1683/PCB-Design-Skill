"""Check beginner decisions and approval bindings; not proof of user intent or hardware correctness."""
import argparse
from datetime import datetime
from pathlib import Path
import workflow_io as io
from evidence_binding import reference

TOPICS = ('purpose', 'carrier', 'board_size', 'power', 'controls_connectors', 'assembly')
STATES = {'confirmed', 'delegated', 'proposed', 'unknown', 'not_applicable'}


def template(project, baseline):
    return {'schema': 1, 'project_id': project, 'baseline_id': baseline,
            'topics': {name: {'state': 'unknown', 'value': '', 'source': None} for name in TOPICS},
            'proposal': None, 'decision': None}


def stamp(value):
    io.text(value, 'timestamp')
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None: raise ValueError('Timestamp needs timezone')
    return result


def evaluate(root, data, baseline, through='design'):
    root = io.no_link(root).resolve(strict=True)
    if through not in ('brief', 'design'): raise ValueError('Unknown intake stage')
    if not isinstance(data, dict) or type(data.get('schema')) is not int or data['schema'] != 1:
        raise ValueError('Intake schema=1 required')
    io.text(baseline, 'baseline'); io.text(data.get('project_id'), 'project ID')
    if data.get('baseline_id') != baseline: raise ValueError('Intake baseline changed')
    topics = data.get('topics')
    if not isinstance(topics, dict) or set(topics) != set(TOPICS):
        raise ValueError('All six beginner topics required')
    pending = []
    for name, item in topics.items():
        if not isinstance(item, dict) or item.get('state') not in STATES:
            raise ValueError('Invalid topic state: ' + name)
        state = item['state']
        if state in ('confirmed', 'delegated', 'not_applicable'):
            io.text(item.get('value'), name + ' decision')
            reference(root, item.get('source'))
            if state == 'not_applicable' and name in ('purpose', 'carrier', 'board_size', 'power', 'assembly'):
                raise ValueError('Core topic cannot be omitted: ' + name)
        else:
            pending.append(name)
    result = {'schema': 1, 'project_id': data['project_id'], 'baseline_id': baseline,
              'state': 'NEEDS_INPUT' if pending else 'BRIEF_RECORDED', 'pending_topics': pending,
              'detailed_design_allowed': False, 'scope': 'decision records and file integrity',
              'intake_digest': io.digest(data),
              'user_intent_authenticity': 'REQUIRES_CONVERSATION_REVIEW'}
    if through == 'brief': return result
    proposal, decision = data.get('proposal'), data.get('decision')
    if proposal is None or decision is None:
        result['state'] = 'NEEDS_INPUT' if pending else 'NEEDS_PLAN_DECISION'
        return result
    if not isinstance(proposal, dict) or not isinstance(decision, dict):
        raise ValueError('Proposal and decision must be objects')
    if proposal.get('topics_digest') != io.digest(topics): raise ValueError('Topics changed after proposal')
    reference(root, proposal.get('document'))
    if not isinstance(proposal.get('choices'), dict) or set(proposal['choices']) != set(TOPICS):
        raise ValueError('Proposal must explain every beginner topic')
    for name, choice in proposal['choices'].items(): io.text(choice, name + ' proposed choice')
    size = proposal.get('assembly_envelope_mm')
    if not isinstance(size, dict) or set(size) != {'board_length', 'board_width', 'assembled_height'}:
        raise ValueError('Explicit board length/width and assembled height required')
    for name, value in size.items():
        if io.finite(value, name) <= 0: raise ValueError('Assembly dimensions must be positive')
    created = stamp(proposal.get('created_at'))
    if decision.get('proposal_digest') != io.digest(proposal): raise ValueError('Proposal changed after decision')
    if decision.get('status') not in ('accepted', 'delegated', 'rejected'):
        raise ValueError('Invalid plan decision')
    reference(root, decision.get('source'))
    if stamp(decision.get('recorded_at')) < created: raise ValueError('Decision predates proposal')
    # An accepted proposal resolves proposed/unknown choices; it must be a real user response.
    # Delegation resolves only topics with explicit delegation, never an unanswered question.
    if decision['status'] == 'delegated' and pending:
        result['state'] = 'NEEDS_INPUT'
        return result
    result['state'] = 'PLAN_RECORDED' if decision['status'] in ('accepted', 'delegated') else 'PLAN_REJECTED'
    result['detailed_design_allowed'] = result['state'] == 'PLAN_RECORDED'
    if result['detailed_design_allowed']: result['pending_topics'] = []
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--baseline', required=True)
    parser.add_argument('--through', choices=('brief', 'design'), default='design')
    args = parser.parse_args()
    try:
        result = evaluate(args.root, io.read(io.no_link(args.root / 'intake.json')), args.baseline, args.through)
        print(io.encoded(result).decode())
        return 0 if result['state'] in ('BRIEF_RECORDED', 'PLAN_RECORDED') else 1
    except (ValueError, TypeError, KeyError, OSError) as exc:
        parser.exit(2, 'ERROR: ' + str(exc) + '\n')


if __name__ == '__main__': raise SystemExit(main())

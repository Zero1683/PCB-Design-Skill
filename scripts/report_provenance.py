"""Hash the exact bytes parsed by a checker; validate declared source identities."""
import hashlib
import json
from pathlib import Path
import workflow_io as io


def read_source(path, role):
    raw = Path(path).read_bytes()
    def bad(value): raise ValueError('Nonfinite JSON number: ' + value)
    data = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=io.pairs, parse_constant=bad)
    return data, {'role': role, 'sha256': hashlib.sha256(raw).hexdigest()}


def identity(data, current):
    if not isinstance(data, dict) or data.get('baseline_id') != current['baseline_id']:
        raise ValueError('Report/input baseline mismatch')
    for key in ('project_id', 'projectId'):
        if key in data and data[key] != current['project_id']:
            raise ValueError('Report/input project mismatch')
    for key in ('document_id', 'documentId'):
        if key in data and data[key] not in current['document_ids']:
            raise ValueError('Report/input document mismatch')
    if 'document_ids' in data:
        docs = data['document_ids']
        if not isinstance(docs, list) or not docs or any(not isinstance(d, str) or d not in current['document_ids'] for d in docs) or len(set(docs)) != len(docs):
            raise ValueError('Report/input document list mismatch')

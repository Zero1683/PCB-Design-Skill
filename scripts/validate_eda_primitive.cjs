#!/usr/bin/env node
'use strict';
// Validate one typed primitive. Never infer whole-document or circuit acceptance.
const fs = require('node:fs');
const upstream = require('../vendor/easyeda-pro-format-skill/validate.js');
const own = (obj, key) => Object.prototype.hasOwnProperty.call(obj, key);
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);

function validate(input) {
  const result = {valid: false, coverage: 'single-primitive-schema-only',
    not_checked: ['document-completeness', 'reference-integrity', 'native-import',
      'connectivity', 'geometry', 'electrical-correctness'], errors: []};
  const reject = message => { result.errors.push({message}); return result; };
  if (!object(input)) return reject('Input must be an object');
  if (Object.keys(input).some(key => !['docType','primitiveType','outer','data'].includes(key)))
    return reject('Unknown input field');
  const {docType, primitiveType, data} = input;
  if (typeof docType !== 'string' || !own(upstream.DOC_TYPES, docType))
    return reject('Unknown or noncanonical document type');
  if (typeof primitiveType !== 'string' || !/^[A-Z][A-Z0-9_-]*$/.test(primitiveType))
    return reject('Use the canonical bare primitive type, e.g. LINE');
  if (!object(data)) return reject('data must be a primitive payload object');
  const key = `${docType.toLowerCase()}_${primitiveType.toLowerCase()}`;
  const schema = primitiveType === 'DOCHEAD' ? 't-doc-head' :
    own(upstream.DOC_TYPE_MAP, key) ? upstream.DOC_TYPE_MAP[key] : null;
  if (!schema) return reject('Unregistered document/primitive pair; no fallback is allowed');
  Object.assign(result, {docType, primitiveType, schema, outer_checked: own(input, 'outer')});
  if (primitiveType === 'DOCHEAD' && data.docType !== docType)
    return reject('DOCHEAD payload docType does not match requested document');
  if (own(input, 'outer')) {
    if (!object(input.outer) || input.outer.type !== primitiveType)
      return reject('Outer type must match primitiveType');
    const checked = upstream.validateOuter(input.outer);
    result.errors.push(...checked.errors);
  }
  const checked = upstream.validateFormat(schema, data);
  result.errors.push(...checked.errors);
  result.valid = result.errors.length === 0 && checked.valid;
  return result;
}

if (require.main === module) {
  try {
    if (process.argv.length !== 3) throw new Error('Usage: node scripts/validate_eda_primitive.cjs <input.json>');
    const result = validate(JSON.parse(fs.readFileSync(process.argv[2], 'utf8')));
    console.log(JSON.stringify(result, null, 2));
    process.exitCode = result.valid ? 0 : 1;
  } catch (error) {
    console.log(JSON.stringify({valid: false, coverage: 'single-primitive-schema-only', errors: [{message: error.message}]}));
    process.exitCode = 1;
  }
}
module.exports = {validate};

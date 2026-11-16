// Render display formulas locally. No network or scientific model execution.
const fs = require('fs');
const path = require('path');
const katex = require(path.join(__dirname, '../vendor/katex/dist/katex.js'));
const formulas = JSON.parse(fs.readFileSync(0, 'utf8'));
const rendered = formulas.map(value => katex.renderToString(value, {
  displayMode: true,
  throwOnError: true,
  output: 'htmlAndMathml',
  strict: 'warn'
}));
process.stdout.write(JSON.stringify(rendered));

cp /home/claude/heuss75/cr-ation-web/worker/worker.js worker.mjs
echo 'globalThis.__schemaReset = () => { SCHEMA_OK = false; };' >> worker.mjs

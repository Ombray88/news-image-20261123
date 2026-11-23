import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const srcFile = join(__dirname, 'entry.png');
const dstFile = join(outDir, 'entry.png');

try {
    mkdirSync(outDir, { recursive: true });
    copyFileSync(srcFile, dstFile);
    const stats = statSync(dstFile);
    console.log(`Copied ${srcFile} to ${dstFile} (${stats.size} bytes)`);
} catch (err) {
    console.error(`Error copying file: ${err.message}`);
    process.exit(1);
}

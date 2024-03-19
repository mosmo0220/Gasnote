import init from "./gasnote_engine.js";

async function main() {
    const { initialize } = await init();
    initialize();
}

document.addEventListener('DOMContentLoaded', main);
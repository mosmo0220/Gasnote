import init from "./gasnote_engine.js";

async function main() {
    const { greet } = await init();
    greet();
}

main();
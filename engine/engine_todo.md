# Engine Todo List for Gasnote Project

## Engine will be based on rust loaded via WebAssembly

Current stage: 0
## Key futures to handle:
1. Elements base schema:
    >> Metadata
    > Description
    > Created at
    > Last time modified
    > Used fonts
    > Used blocks (for example, table) (block htmx base)
    > Used graphics (name, path, relative_name)
    >> Blocks
    > Block uid
    > Block styles
    > Block content
    > Block external (for example: pictures, links)
    >> Encryption public key
    >> Notebook uid (not from DB)
    >> Content SHA256 (for validation)
2. Metadata engine
3. Blocks engine
4. Encryption engine
5. SHA256 validation engine
6. Packing and Unpacking engine
7. WASM integration
8. Creation of the first blocks
9. Integrating with the website
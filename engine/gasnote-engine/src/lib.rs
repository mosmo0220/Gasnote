mod utils;
extern crate wasm_bindgen;
extern crate js_sys;
extern crate web_sys;
extern crate uuid;

use wasm_bindgen::prelude::*;
use js_sys::Reflect;
use std::collections::HashMap;
use uuid::Uuid;

#[wasm_bindgen]
struct Element {
    html: String,
    css: String,
    js: String,
    name: String,
    uuid: Uuid,
}

#[wasm_bindgen]
impl Element {
    #[wasm_bindgen(constructor)]
    pub fn new(html: &str, css: &str, js: &str, name: &str) -> Self {
        Element {
            html: html.to_string(),
            css: css.to_string(),
            js: js.to_string(),
            name: name.to_string(),
            uuid: Uuid::new_v4()
        }
    }

    #[wasm_bindgen]
    pub fn name(&self) -> String {
        self.name.clone()
    }

    #[wasm_bindgen]
    pub fn uuid(&self) -> String {
        self.uuid.to_string()
    }

    #[wasm_bindgen(js_name = intoJsValueArray)]
    pub fn into_js_value_array(&self) -> Box<[JsValue]> {
        let html_value = JsValue::from_str(&self.html);
        let css_value = JsValue::from_str(&self.css);
        let js_value = JsValue::from_str(&self.js);
        let name_value = JsValue::from_str(&self.name);
        let uuid_value = JsValue::from_str(&self.uuid.to_string());

        vec![html_value, css_value, js_value, name_value, uuid_value].into_boxed_slice()
    }
}

#[wasm_bindgen]
pub struct Elements {
    schematics: HashMap<String, Element>,
    name_to_uuid: HashMap<String, String>,
}

#[wasm_bindgen]
impl Elements {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        Elements {
            schematics: HashMap::new(),
            name_to_uuid: HashMap::new(),
        }
    }

    pub fn add_schematic(&mut self, html: &str, css: &str, js: &str, name: &str) -> String {
        let element = Element::new(html, css, js, name);
        let uuid = element.uuid.to_string();
        self.schematics.insert(uuid.clone(), element);
        self.name_to_uuid.insert(name.to_string(), uuid.clone());
        uuid
    }

    #[wasm_bindgen]
    pub fn get_html_content(&self, uuid: &str, content: &str) -> Option<String> {
        if let Some(element) = self.schematics.get(uuid) {
            Some(element.html.replace("{{content}}", content))
        } else {
            None
        }
    }

    #[wasm_bindgen]
    pub fn get_css_js_from_block(&self, uuid: &str) -> JsValue {
        if let Some(element) = self.schematics.get(uuid) {
            let mut obj = js_sys::Object::new();
            Reflect::set(&mut obj, &JsValue::from_str("css"), &JsValue::from_str(&element.css)).unwrap();
            Reflect::set(&mut obj, &JsValue::from_str("js"), &JsValue::from_str(&element.js)).unwrap();
            JsValue::from(obj)
        } else {
            JsValue::NULL
        }
    }

    #[wasm_bindgen]
    pub fn get_uuid_by_name(&self, name: &str) -> Option<String> {
        self.name_to_uuid.get(name).cloned()
    }

    #[wasm_bindgen(js_name = intoJsValueArray)]
    pub fn into_js_value_array(&self) -> Box<[JsValue]> {
        let schematics_array: Vec<JsValue> = self
            .schematics
            .values()
            .map(|element| {
                let mut map = js_sys::Object::new();
                Reflect::set(
                    &mut map,
                    &JsValue::from_str("html"),
                    &JsValue::from_str(&element.html),
                )
                .unwrap();
                Reflect::set(
                    &mut map,
                    &JsValue::from_str("css"),
                    &JsValue::from_str(&element.css),
                )
                .unwrap();
                Reflect::set(
                    &mut map,
                    &JsValue::from_str("js"),
                    &JsValue::from_str(&element.js),
                )
                .unwrap();
                Reflect::set(
                    &mut map,
                    &JsValue::from_str("name"),
                    &JsValue::from_str(&element.name),
                )
                .unwrap();
                Reflect::set(
                    &mut map,
                    &JsValue::from_str("uuid"),
                    &JsValue::from_str(&element.uuid.to_string()),
                )
                .unwrap();
                JsValue::from(map)
            })
            .collect();

        schematics_array.into_boxed_slice()
    }
}

// Function to initialize console log for Rust
#[wasm_bindgen(start)]
pub fn initialize() {
    utils::set_panic_hook();
    
    let mut elements = Elements::new();
    let uuid = elements.add_schematic(
        "<div>{{content}}</div>",
        "div { color: red; }",
        "console.log('Hello from JavaScript!')",
        "example_schematic",
    );

    log(&format!("UUID for 'example_schematic': {:?}", elements.get_uuid_by_name("example_schematic")));
    log(&format!("HTML content for UUID {:?}: {:?}", uuid, elements.get_html_content(&uuid, "Hello, World!")));
    log(&format!("CSS and JS for UUID {:?}: {:?}", uuid, elements.get_css_js_from_block(&uuid)));
}

#[wasm_bindgen]
extern "C" {
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
}

#[wasm_bindgen]
pub fn console_log_from_rust(message: &str) {
    log(&format!("Log from Rust: {}", message));
}
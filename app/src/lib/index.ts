// place files you want to import through the `$lib` alias in this folder.

import { writable, type Writable } from "svelte/store";

export const uploadingStateStore: Writable<boolean> = writable(false);

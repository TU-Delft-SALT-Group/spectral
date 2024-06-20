import { writable } from 'svelte/store';

export const menubarOverrides = writable<{ [id: string]: string }>({});

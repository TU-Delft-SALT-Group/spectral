import { writable } from 'svelte/store';

// now, if the segment looks like an internal ID of the session
// just replace it with the actual name of the session, and in the snippet
export const menubarOverrides = writable<{ [id: string]: string }>({});

import { z } from 'zod';
import { fileState } from '../file-state';
import type { ModeValidator } from '..';

export { default as Transcription } from './Transcription.svelte';
export { default as TranscriptionIcon } from './TranscriptionIcon.svelte';

export const transcriptionData = {
	computedFileData: z.null(),

	fileState: fileState
		.pick({
			id: true,
			name: true,
			transcriptions: true,
			frame: true
		})
		.default({}),

	modeState: z.object({}).default({})
} satisfies ModeValidator;

export function doubleClick(event: MouseEvent) {
	const element = event.target! as HTMLElement;
	element.contentEditable = 'true';
	element.focus();
}

export function focusOut(event: FocusEvent, toChange: { name: string } | { value: string }) {
	const element = event.target! as HTMLElement;
	if (!element.isContentEditable) return;
	element.contentEditable = 'false';

	if ('name' in toChange) {
		toChange.name = element.innerText ?? '';
		element.textContent = toChange.name;
	} else {
		toChange.value = element.innerText ?? '';
		element.textContent = toChange.value;
	}
}

export function keyDown(event: KeyboardEvent, toChange: { name: string } | { value: string }) {
	const element = event.target! as HTMLElement;

	if (!element.isContentEditable) {
		return;
	}

	if (event.key === 'Escape') {
		element.contentEditable = 'false';
		element.textContent = 'name' in toChange ? toChange.name : toChange.value;
	} else if (event.key === 'Enter') {
		element.contentEditable = 'false';

		if ('name' in toChange) {
			toChange.name = element.innerText ?? '';
			element.textContent = toChange.name;
		} else {
			toChange.value = element.innerText ?? '';
			element.textContent = toChange.value;
		}
	}
}

export type Caption = {
	start: number;
	end: number;
	value: string;
};

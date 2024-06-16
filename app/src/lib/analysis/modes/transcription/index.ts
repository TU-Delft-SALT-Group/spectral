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
			transcriptions: true
		})
		.default({}),

	modeState: z.object({}).default({})
} satisfies ModeValidator;

export function doubleClick(event: MouseEvent) {
	const element = event.target! as HTMLElement;
	element.contentEditable = 'true';
}

export function focusOut(event: FocusEvent, toChange: { name: string } | { value: string }) {
	const element = event.target! as HTMLElement;
	element.contentEditable = 'false';

	if ('name' in toChange) {
		toChange.name = element.textContent ?? '';
	} else {
		toChange.value = element.textContent ?? '';
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
			toChange.name = element.textContent ?? '';
		} else {
			toChange.value = element.textContent ?? '';
		}
	}
}

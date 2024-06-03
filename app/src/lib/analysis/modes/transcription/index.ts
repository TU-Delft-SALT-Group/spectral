import { z } from 'zod';
import { fileState } from '../file-state';
import type { ModeValidator } from '..';

export { default as Transcription } from './Transcription.svelte';
export { default as TranscriptionIcon } from './TranscriptionIcon.svelte';

export const transcriptionData = {
	computedFileData: z.null(),

	fileState: fileState
		.pick({
			id: true
		})
		.default({}),

	modeState: z.object({}).default({})
} satisfies ModeValidator;

export type Caption = {
	startPos: number;
	endPos: number;
	content: string;
};

export type Track = {
	id: string;
	name: string;
	captions: Caption[];
};

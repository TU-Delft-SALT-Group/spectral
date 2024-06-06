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
			transcriptions: true
		})
		.default({}),

	modeState: z.object({}).default({})
} satisfies ModeValidator;

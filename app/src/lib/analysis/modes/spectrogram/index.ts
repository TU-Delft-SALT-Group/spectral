import { z } from 'zod';
import type { ModeValidator } from '..';
import { fileState } from '../file-state';

export const spectrogramData = {
	computedFileData: z.object({ formants: z.array(z.array(z.number().nullable())).nullable() }),

	fileState: fileState
		.pick({
			id: true,
			name: true
		})
		.default({}),

	modeState: z.object({}).default({})
} satisfies ModeValidator;

export { default as Spectrogram } from './Spectrogram.svelte';
export { default as SpectrogramIcon } from './SpectrogramIcon.svelte';
export { default as SpectrogramPlugin } from './SpectrogramPlugin.svelte';

import { z } from 'zod';
import type { ModeValidator } from '..';
import { fileState } from '../file-state';

export { default as Waveform } from './Waveform.svelte';
export { default as WaveformPlugin } from './WaveformPlugin.svelte';

export const waveformData = {
	computedFileData: z.null(),

	fileState: fileState
		.pick({
			id: true,
			name: true,
			frame: true,
			transcriptions: true,
			matchStrings: true
		})
		.default({}),

	modeState: z.object({}).default({})
} satisfies ModeValidator;

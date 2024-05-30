import { z } from 'zod';
import type { ModeValidator } from '..';
import { fileState } from '../file-state';

export const waveformData = {
	computedFileData: z.null(),

	fileState: fileState
		.pick({
			id: true,
			name: true,
			frame: true
		})
		.default({}),

	modeState: z.object({}).default({})
} satisfies ModeValidator;

export { default as Waveform } from './Waveform.svelte';
export { default as WaveformPlugin } from './WaveformPlugin.svelte';

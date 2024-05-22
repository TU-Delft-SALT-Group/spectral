import { z } from 'zod';

import type { ModeValidator } from '..';
import { fileState } from '../file-state';

export const vowelSpaceData = {
	computedFileData: z.object({
		/**
		 * First formant
		 */
		f1: z.number(),

		/**
		 * Second formant
		 */
		f2: z.number()
	}),

	fileState: fileState
		.pick({
			filename: true,
			vowelSpace: true
		})
		.default({}),
	modeState: z.object({}).default({})
} satisfies ModeValidator;

export { default as VowelSpace } from './VowelSpace.svelte';
export { default as VowelSpaceIcon } from './VowelSpaceIcon.svelte';

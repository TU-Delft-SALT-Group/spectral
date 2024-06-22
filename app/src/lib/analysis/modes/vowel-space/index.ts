import { z } from 'zod';

import type { ModeValidator } from '..';
import { fileState } from '../file-state';

export const vowelSpaceData = {
	computedFileData: z
		.object({
			formants: z.array(
				z.object({
					/**
					 * First formant
					 */
					f1: z.number(),

					/**
					 * Second formant
					 */
					f2: z.number(),

					start: z.number(),

					end: z.number(),

					matchString: z.string().nullable()
				})
			)
		})
		.nullable(),

	fileState: fileState
		.pick({
			name: true,
			id: true,
			matchStrings: true
		})
		.default({}),

	modeState: z
		.object({
			showLegend: z.boolean().default(true)
		})
		.default({})
} satisfies ModeValidator;

export { default as VowelSpace } from './VowelSpace.svelte';
export { default as VowelSpaceIcon } from './VowelSpaceIcon.svelte';

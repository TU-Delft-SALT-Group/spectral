import { z } from 'zod';

export const vowelSpaceData = z.object({
	mode: z.literal('vowel-space'),

	/**
	 * First formant
	 */
	f1: z.number(),

	/**
	 * Second formant
	 */
	f2: z.number()
});

export { default as VowelSpace } from './VowelSpace.svelte';
export { default as VowelSpaceIcon } from './VowelSpaceIcon.svelte';

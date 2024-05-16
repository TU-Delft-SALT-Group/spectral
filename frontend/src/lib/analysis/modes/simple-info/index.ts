import { z } from 'zod';

export const simpleInfoData = z.object({
	mode: z.literal('simple-info'),

	/**
	 * Duration of the file, in seconds
	 */
	duration: z.number(),

	/**
	 * Average of pitch of frames present in file
	 */
	averagePitch: z.number(),

	/**
	 * The size of the file, in bytes
	 */
	fileSize: z.number(),

	/**
	 * Postgres timestamp of when the file was created
	 */
	fileCreationDate: z.date(),

	frame: z.object({
		duration: z.number(),
		pitch: z.union([z.number(), z.null()]),
		f1: z.union([z.number(), z.null()]),
		f2: z.union([z.number(), z.null()])
	})
});

export { default as SimpleInfo } from './SimpleInfo.svelte';

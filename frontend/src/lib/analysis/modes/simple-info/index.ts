import { z } from 'zod';
import { type ModeValidator } from '..';
import { fileState } from '../file-state';

export const simpleInfoData = {
	computedFileData: z.object({
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
		fileCreationDate: z.string().pipe(z.coerce.date()),

		frameData: z
			.object({
				duration: z.number(),
				pitch: z.number().optional(),
				f1: z.number().optional(),
				f2: z.number().optional()
			})
			.nullable()
	}),

	fileState: fileState
		.pick({
			fileId: true,
			filename: true,
			frame: true
		})
		.default({}),

	modeState: z.object({}).optional().default({})
} satisfies ModeValidator;

export { default as SimpleInfo } from './SimpleInfo.svelte';

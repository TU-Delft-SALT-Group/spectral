import { z } from 'zod';
import { frame } from '../kernel/framing';

export const transcription = z
	.object({
		id: z.string().default('broken-track-id'),
		name: z.string().default('broken-track-name'),
		captions: z
			.array(
				z.object({
					value: z.string(),
					start: z.number(),
					end: z.number()
				})
			)
			.default([])
	})
	.default({});

export const fileState = z.object({
	id: z.string().default('broken-file-id'),
	name: z.string().default('broken-filename'),
	frame: frame.nullable().optional(),
	cycleEnabled: z.boolean().default(false),
	transcriptions: z.array(transcription).default([])
});

export type FileState = z.infer<typeof fileState>;
export type Transcription = z.infer<typeof transcription>;

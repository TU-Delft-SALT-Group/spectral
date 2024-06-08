import { z } from 'zod';
import { frame } from '../kernel/framing';

export const caption = z
	.object({
		value: z.string().default('broken-value'),
		start: z.number().default(0),
		end: z.number().default(0)
	})
	.default({});

export const transcription = z
	.object({
		id: z.string().default('broken-track-id'),
		name: z.string().default('broken-track-name'),
		captions: z.array(caption).default([])
	})
	.default({});

export const fileState = z.object({
	id: z.string().default('broken-file-id'),
	name: z.string().default('broken-filename'),
	frame: frame.nullable().default(null),
	cycleEnabled: z.boolean().default(false),
	transcriptions: z.array(transcription).default([]),
	reference: z.array(caption).default([]),
	hypothesis: z.array(caption).default([])
});

export type FileState = z.infer<typeof fileState>;
export type Transcription = z.infer<typeof transcription>;

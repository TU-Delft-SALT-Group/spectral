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
		selected: z.boolean().default(true),
		captions: z.array(caption).default([])
	})
	.default({});

export const fileState = z.object({
	id: z.string().default('broken-file-id'),
	name: z.string().default('broken-filename'),
	frame: frame.nullable().default(null),
	cycleEnabled: z.boolean().default(false),
	transcriptions: z.array(transcription).default([]),
	matchStrings: z
		.array(z.object({ id: z.string(), matchString: z.string(), selected: z.boolean() }))
		.default([]),
	reference: z
		.object({
			id: z.string(),
			name: z.string(),
			captions: z.array(caption)
		})
		.nullable()
		.default(null),
	hypothesis: z
		.object({
			id: z.string(),
			name: z.string(),
			captions: z.array(caption)
		})
		.nullable()
		.default(null)
});

export type FileState = z.infer<typeof fileState>;
export type Transcription = z.infer<typeof transcription>;

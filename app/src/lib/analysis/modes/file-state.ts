import { z } from 'zod';
import { frame } from '../kernel/framing';

export const fileState = z.object({
	id: z.string().default('broken-file-id'),
	name: z.string().default('broken-filename'),
	frame: frame.nullable().default(null),
	cycleEnabled: z.boolean().default(false),
	transcriptions: z
		.array(
			z.array(
				z.object({
					value: z.string(),
					start: z.number().nullable(),
					end: z.number().nullable()
				})
			)
		)
		.default([])
});

export type FileState = z.infer<typeof fileState>;

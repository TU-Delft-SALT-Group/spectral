import { z } from 'zod';
import { frame } from '../kernel/framing';

export const fileState = z.object({
	fileId: z.string().default('broken-file-id'),
	filename: z.string().default('broken-filename'),
	frame: frame.nullable().default(null),
	cycleEnabled: z.boolean().default(false),

	vowelSpace: z
		.object({
			showLegend: z.boolean().default(false)
		})
		.default({})
});

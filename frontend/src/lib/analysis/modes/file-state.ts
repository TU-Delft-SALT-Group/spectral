import { z } from 'zod';
import { frame } from '../engine/framing';

export const fileState = z.object({
	fileId: z.string().default('broken-file-id'),
	filename: z.string().default('broken-filename'),
	frame: frame.nullable().default(null),
	cycleEnabled: z.boolean().default(false)
});

import { z } from 'zod';

/**
 * Frame represents a range of indices in a data array.
 */
export type Frame = z.infer<typeof frame>;

export const frame = z.object({
	startIndex: z.number(),
	endIndex: z.number()
});

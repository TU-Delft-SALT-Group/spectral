import { z } from 'zod';

export type Frame = z.infer<typeof frame>;

/**
 * Frame represents a range of indices in a data array.
 */
export const frame = z.object({
	startIndex: z.number(),
	endIndex: z.number()
});

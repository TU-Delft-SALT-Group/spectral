import { z } from 'zod';
import { type ModeValidator } from '..';
import { fileState } from '../file-state';

export const alignment = z.object({
	/**
	 * String literal describing the type of alignment
	 * either 'insert', 'substitute', 'delete' or 'equal'
	 */
	type: z.enum(['insert', 'substitute', 'delete', 'equal']),

	/**
	 * start index of the slice of the reference array
	 */
	referenceStartIndex: z.number().int(),

	/**
	 * end index of the slice of the reference array
	 */
	referenceEndIndex: z.number().int(),

	/**
	 * start index of the slice of the hypothesis array
	 */
	hypothesisStartIndex: z.number().int(),

	/**
	 * end index of the slice of the hypothesis array
	 */
	hypothesisEndIndex: z.number().int()
});

const common = z.object({
	/**
	 * The number of correct matches on character level
	 */
	hits: z.number().int(),

	/**
	 * The number of character level substitutions
	 */
	substitutions: z.number().int(),

	/**
	 * The number of character level deletions
	 */
	deletions: z.number().int(),

	/**
	 * The number of character level insertions
	 */
	insertions: z.number().int(),

	/**
	 * Array of characters representing the ground-truth
	 */
	reference: z.array(z.string()),

	/**
	 * Array of characters representing the hypothesis
	 * Which is based on the transcription for the file
	 */
	hypothesis: z.array(z.string()),

	/**
	 * An array of Objects containing information about matching slices of the
	 * the reference and hypothesis arrays
	 */
	alignments: z.array(alignment)
});

export type Common = z.infer<typeof common>;
export const errorRateData = {
	computedFileData: z
		.object({
			/**
			 * Error related information for a file based on its ground truth and transcriptions
			 */

			wordLevel: z
				.object({
					/**
					 * The word error rate, still has to be converted to percentages
					 */
					wer: z.number(),

					/**
					 * The match error rate, still has to be converted to percentages
					 */
					mer: z.number(),

					/**
					 * The word information lost, still has to be converted to percentages
					 */
					wil: z.number(),

					/**
					 * The word information preserved, still has to be converted to percentages
					 */
					wip: z.number(),

					/**
					 * bert score
					 */
					bert: z.number(),

					/**
					 * jaroWinkler score
					 */
					jaroWinkler: z.number()
				})
				.merge(common),

			/**
			 * Error rate information on the character level
			 */
			characterLevel: z
				.object({
					/**
					 * The character error rate, still has to be converted to percentages
					 */
					cer: z.number()
				})
				.merge(common)
		})
		.nullable(),

	fileState: fileState
		.pick({
			id: true,
			name: true,
			transcriptions: true,
			reference: true,
			hypothesis: true
		})
		.default({}),

	modeState: z.object({}).optional().default({})
} satisfies ModeValidator;

export { default as ErrorRate } from './ErrorRate.svelte';
export { default as ErrorRateIcon } from './ErrorRateIcon.svelte';

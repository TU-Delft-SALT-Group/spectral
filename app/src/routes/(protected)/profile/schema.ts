import { z } from 'zod';

export const formSchema = z.object({
	name: z.string(),
	model: z.string(),
	key: z.string()
});

export const deleteFormSchema = z.object({
	name: z.string()
});

export type FormSchema = typeof formSchema;
